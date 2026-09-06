#!/usr/bin/env python3
"""
5-Step Prompt Evaluation Pipeline:
1. Draft: Write 2+ prompt versions
2. Dataset: Create eval dataset
3. Run: Execute prompts on all questions
4. Grade: Use Claude as grader (1-10 scale)
5. Iterate: Compare and improve
"""

import os
from anthropic import Anthropic

client = Anthropic()

# STEP 1: Define two prompt versions
# V1 is simple and minimal
PROMPT_V1 = "Please answer the user's question: {question}"

# V2 has additional instruction for detailed responses
PROMPT_V2 = """Please answer the user's question with ample detail and clarity.
Provide thorough explanations and relevant context where applicable.
Question: {question}"""

# STEP 2: Define eval dataset - questions that test different domains
EVAL_QUESTIONS = [
    "What's 2+2?",
    "How do I make oatmeal?",
    "How far away is the Moon?",
    "What are the benefits of exercise?",
    "Explain photosynthesis briefly.",
]

# STEP 4: Grader system prompt
# This prompt tells Claude to act as an evaluator
GRADER_SYSTEM = """You are an expert evaluator. Grade the response to the given question on a scale of 1-10 based on:
- Correctness: Is the answer accurate?
- Completeness: Does it cover the key points?
- Clarity: Is it well-explained?

Respond with ONLY a single number from 1 to 10. No explanation."""


def extract_text(response):
    """Helper: Extract text from Claude response."""
    for block in response.content:
        if hasattr(block, 'text'):
            return block.text
    return ""


def run_prompt(prompt_template, questions):
    """STEP 3: Run prompt template on all questions.

    For each question:
    1. Interpolate the template with the question
    2. Call Claude
    3. Collect the response
    """
    responses = []

    for question in questions:
        # Interpolate: "Please answer..." becomes "Please answer: What's 2+2?"
        prompt = prompt_template.format(question=question)

        # Call Claude with the interpolated prompt
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = extract_text(message)
        responses.append(answer)

    return responses


def grade_response(question, answer):
    """STEP 4: Use Claude as grader to score the response.

    This is KEY: we make a SECOND call to Claude, this time asking it to
    evaluate the response from the first call. This gives us objective scoring.

    Returns: integer from 1-10
    """
    # Build the grading prompt
    grading_prompt = f"""Question: {question}

Response: {answer}

Grade this response (1-10 only):"""

    # Call Claude as grader
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=5,  # Only need 1-2 chars for a number
        system=GRADER_SYSTEM,
        messages=[{"role": "user", "content": grading_prompt}]
    )

    # Extract the score
    score_text = extract_text(message).strip().lower()

    # Parse: look for any digit in the response
    for char in score_text:
        if char.isdigit():
            return int(char)

    return 5  # Default if parsing fails


def evaluate_prompt(prompt_name, prompt_template, questions):
    """STEP 5: Orchestrate the full pipeline.

    This is the main workflow:
    1. Generate responses using run_prompt()
    2. Grade each response using grade_response()
    3. Calculate average score
    4. Print detailed report
    5. Return results for comparison
    """
    print(f"\n{'='*80}")
    print(f"📊 Evaluating: {prompt_name}")
    print(f"{'='*80}\n")

    # Step 3: Generate all responses
    print("🔄 Generating responses...")
    responses = run_prompt(prompt_template, questions)

    # Step 4: Grade each response
    print("📈 Grading responses...\n")
    scores = []

    for i, (question, answer) in enumerate(zip(questions, responses), 1):
        score = grade_response(question, answer)
        scores.append(score)

        # Print detailed report for each question
        print(f"Q{i}: {question}")
        print(f"   Answer: {answer[:100]}{'...' if len(answer) > 100 else ''}")
        print(f"   Score: {score}/10")
        print()

    # Calculate and display average
    average_score = sum(scores) / len(scores)

    print(f"{'='*80}")
    print(f"📊 Results for {prompt_name}")
    print(f"{'='*80}")
    print(f"Average Score: {average_score:.1f}/10")
    print(f"Total Questions: {len(questions)}")
    print()

    return average_score, scores


def main():
    # Verify API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    print("="*80)
    print("DEMO: 5-Step Prompt Evaluation Pipeline")
    print("="*80)
    print("""
STEP 1: Draft prompts (V1 vs V2)
STEP 2: Define eval dataset
STEP 3: Run prompts on questions
STEP 4: Grade responses with Claude
STEP 5: Iterate and compare
""")

    # Evaluate both versions
    v1_score, v1_scores = evaluate_prompt("PROMPT V1 (Simple)", PROMPT_V1, EVAL_QUESTIONS)
    v2_score, v2_scores = evaluate_prompt("PROMPT V2 (Detailed)", PROMPT_V2, EVAL_QUESTIONS)

    # Display comparison
    print("="*80)
    print("🏆 COMPARISON")
    print("="*80)
    print(f"Prompt V1 (Simple):     {v1_score:.1f}/10")
    print(f"Prompt V2 (Detailed):   {v2_score:.1f}/10")
    print(f"Improvement:            +{v2_score - v1_score:.1f} points")
    print(f"Winner: {'V2 (Detailed)' if v2_score > v1_score else 'V1 (Simple)' if v1_score > v2_score else 'Tie'}")
    print()

    print("="*80)
    print("💡 INSIGHTS")
    print("="*80)
    print(f"""
Prompt V2 had {sum(1 for s in v2_scores if s > 7)} questions scored > 7/10
Prompt V1 had {sum(1 for s in v1_scores if s > 7)} questions scored > 7/10

This shows objectively which version produces better responses!
Now you can ITERATE on the winning version to improve it further.
""")


if __name__ == "__main__":
    main()

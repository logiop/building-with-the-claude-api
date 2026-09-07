#!/usr/bin/env python3

import os
import json
import statistics
from anthropic import Anthropic

client = Anthropic()

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system=None, stop_sequences=[]):
    params = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1000,
        "messages": messages,
    }
    if system is not None:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    return client.messages.create(**params)

def extract_text(response):
    for block in response.content:
        if hasattr(block, 'text'):
            return block.text
    return ""

def run_prompt(test_case):
    prompt = f"Please solve the following task: {test_case['task']}"
    messages = []
    add_user_message(messages, prompt)
    response = chat(messages)
    return extract_text(response)

def grade_by_model(test_case, output):
    """Expert code reviewer model-based grader."""
    eval_prompt = f"""You are an expert code reviewer. Evaluate this solution:

Task: {test_case['task']}

Solution: {output[:1000]}

Provide evaluation as JSON with:
- strengths: [list 1-3 strengths]
- weaknesses: [list 1-3 weaknesses]
- reasoning: brief explanation
- score: integer 1-10

Return ONLY valid JSON."""

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")

    response = chat(messages, stop_sequences=["```"])
    json_text = extract_text(response).strip()

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return {
            "strengths": ["Unable to parse"],
            "weaknesses": ["Parsing error"],
            "reasoning": "JSON parse failed",
            "score": 5
        }

def run_test_case(test_case):
    output = run_prompt(test_case)
    grading = grade_by_model(test_case, output)

    return {
        "task": test_case['task'],
        "output": output[:200],
        "score": grading.get('score', 5),
        "reasoning": grading.get('reasoning', ''),
        "strengths": grading.get('strengths', []),
        "weaknesses": grading.get('weaknesses', []),
    }

def run_eval(dataset):
    results = []
    for i, test_case in enumerate(dataset, 1):
        print(f"  [{i}/{len(dataset)}] Evaluating: {test_case['task'][:50]}...")
        result = run_test_case(test_case)
        results.append(result)
    return results

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    print("="*80)
    print("EVAL PIPELINE: Model-Based Grading")
    print("="*80)
    print()

    if not os.path.exists("dataset.json"):
        print("❌ dataset.json not found!")
        exit(1)

    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    print(f"📂 Loaded {len(dataset)} test cases\n")
    print("🔄 Running evaluation with model-based grading...\n")

    results = run_eval(dataset)

    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80)

    scores = []
    for i, result in enumerate(results, 1):
        scores.append(result['score'])
        print(f"\n[Test {i}] Score: {result['score']}/10")
        print(f"Task: {result['task']}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Strengths: {', '.join(result['strengths'])}")
        print(f"Weaknesses: {', '.join(result['weaknesses'])}")

    avg_score = statistics.mean(scores)
    print("\n" + "="*80)
    print(f"📈 Average Score: {avg_score:.1f}/10")
    print("="*80)

    # Save results
    with open("results.json", "w") as f:
        json.dump({
            "dataset_size": len(dataset),
            "average_score": avg_score,
            "results": results
        }, f, indent=2)

    print("✅ Results saved to results.json")

if __name__ == "__main__":
    main()

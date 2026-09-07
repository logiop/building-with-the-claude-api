#!/usr/bin/env python3

import os
import json
import ast
import re
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

# ============================================================================
# SYNTAX VALIDATORS (Tier 1: Fast, Objective)
# ============================================================================

def validate_json(text):
    """Validate JSON syntax. Returns 10 if valid, 0 if invalid."""
    try:
        json.loads(text)
        return 10
    except (json.JSONDecodeError, ValueError):
        return 0

def validate_python(text):
    """Validate Python syntax. Returns 10 if valid, 0 if invalid."""
    try:
        ast.parse(text)
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    """Validate regex pattern syntax. Returns 10 if valid, 0 if invalid."""
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def grade_syntax(output, test_case):
    """Apply syntax validator based on test_case["format"] field."""
    output = output.strip()
    format_type = test_case.get("format", "python")

    if format_type == "json":
        return validate_json(output)
    elif format_type == "python":
        return validate_python(output)
    elif format_type == "regex":
        return validate_regex(output)
    else:
        return 0

# ============================================================================
# MODEL GRADER (Tier 2: Slow, Intelligent)
# ============================================================================

def run_prompt(test_case):
    """Run test case with format-agnostic prefill.

    Uses "```code" as generic prefix (not "```python", "```json", etc.)
    because we don't know the exact format until runtime, and Claude
    will infer the right format from context and fill in accordingly.
    """
    prompt = f"Please solve the following task. Respond only with Python, JSON, or a plain Regex. Do not add any comments or commentary or explanation.\n\nTask: {test_case['task']}"

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")

    response = chat(messages)
    output = extract_text(response)

    return output

def grade_by_model(test_case, output):
    """Expert code reviewer model-based grader (Tier 2)."""
    eval_prompt = f"""You are an expert code reviewer. Evaluate this solution:

Task: {test_case['task']}

Solution: {output[:1000]}

Provide evaluation as JSON with:
- strengths: [list 1-2 strengths]
- weaknesses: [list 1-2 weaknesses]
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

# ============================================================================
# COMBINED EVALUATION
# ============================================================================

def run_test_case(test_case):
    """Run test case with both syntax (Tier 1) and model (Tier 2) grading."""
    output = run_prompt(test_case)

    # Tier 1: Fast syntax validation
    syntax_score = grade_syntax(output, test_case)

    # Tier 2: Slow but intelligent model grading
    grading = grade_by_model(test_case, output)
    model_score = grading.get('score', 5)

    # Combine scores: average of syntax + semantic
    combined_score = (syntax_score + model_score) / 2

    return {
        "task": test_case['task'],
        "format": test_case.get('format', 'unknown'),
        "output": output[:200],
        "syntax_score": syntax_score,
        "model_score": model_score,
        "score": combined_score,
        "reasoning": grading.get('reasoning', ''),
        "strengths": grading.get('strengths', []),
        "weaknesses": grading.get('weaknesses', []),
    }

def run_eval(dataset):
    """Run evaluation on entire dataset."""
    results = []
    for i, test_case in enumerate(dataset, 1):
        print(f"  [{i}/{len(dataset)}] Evaluating [{test_case.get('format', '?')}]: {test_case['task'][:45]}...")
        result = run_test_case(test_case)
        results.append(result)
    return results

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    print("="*80)
    print("TWO-TIER GRADING: Syntax (Fast) + Model (Intelligent)")
    print("="*80)
    print()

    if not os.path.exists("dataset.json"):
        print("❌ dataset.json not found!")
        exit(1)

    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    print(f"📂 Loaded {len(dataset)} test cases\n")
    print("🔄 Running evaluation pipeline...\n")

    results = run_eval(dataset)

    print("\n" + "="*80)
    print("📊 DETAILED RESULTS")
    print("="*80)

    syntax_scores = []
    model_scores = []
    combined_scores = []

    for i, result in enumerate(results, 1):
        syntax_scores.append(result['syntax_score'])
        model_scores.append(result['model_score'])
        combined_scores.append(result['score'])

        print(f"\n[Test {i}] Format: {result['format'].upper()}")
        print(f"Task: {result['task']}")
        print(f"  Syntax Score:  {result['syntax_score']}/10 (valid format: {'✅' if result['syntax_score'] == 10 else '❌'})")
        print(f"  Model Score:   {result['model_score']}/10 (semantic quality)")
        print(f"  Combined:      {result['score']:.1f}/10")
        print(f"  Reasoning: {result['reasoning']}")
        print(f"  Strengths: {', '.join(result['strengths'])}")
        print(f"  Weaknesses: {', '.join(result['weaknesses'])}")

    # Summary statistics
    print("\n" + "="*80)
    print("📈 SUMMARY STATISTICS")
    print("="*80)
    print(f"Average Syntax Score:   {statistics.mean(syntax_scores):.1f}/10")
    print(f"Average Model Score:    {statistics.mean(model_scores):.1f}/10")
    print(f"Average Combined Score: {statistics.mean(combined_scores):.1f}/10")
    print("="*80)

    # Save results
    with open("results.json", "w") as f:
        json.dump({
            "dataset_size": len(dataset),
            "average_syntax_score": statistics.mean(syntax_scores),
            "average_model_score": statistics.mean(model_scores),
            "average_combined_score": statistics.mean(combined_scores),
            "results": results
        }, f, indent=2)

    print("✅ Results saved to results.json")

if __name__ == "__main__":
    main()

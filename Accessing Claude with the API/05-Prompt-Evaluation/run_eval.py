#!/usr/bin/env python3

import os
import json
from anthropic import Anthropic

client = Anthropic()

# Helper functions (from generate_dataset.py)
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system=None, stop_sequences=[]):
    params = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 500,
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
    """Run a single test case through Claude.

    Takes the task description and sends it to Claude for execution.
    Returns the raw output without any formatting requirements.
    """
    prompt = f"Please solve the following task: {test_case['task']}"

    messages = []
    add_user_message(messages, prompt)

    response = chat(messages)
    output = extract_text(response)

    return output

def run_test_case(test_case):
    """Execute one test case and collect results.

    Calls run_prompt() and assigns a placeholder score (always 10).
    TODO: Replace score placeholder with actual grading in next step.
    """
    output = run_prompt(test_case)

    # TODO - grading reale nel prossimo step
    score = 10

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
    }

def run_eval(dataset):
    """Run evaluation on entire dataset.

    Iterates through all test cases, executes each one,
    and collects results in a list.
    """
    results = []

    for i, test_case in enumerate(dataset, 1):
        print(f"  [{i}/{len(dataset)}] Running: {test_case['task'][:60]}...")
        result = run_test_case(test_case)
        results.append(result)

    return results

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    print("="*80)
    print("DEMO: Eval Pipeline - Run Phase")
    print("="*80)
    print()

    # Load dataset
    print("📂 Loading dataset.json...")
    if not os.path.exists("dataset.json"):
        print("❌ dataset.json not found!")
        print("   Run generate_dataset.py first to create it.")
        exit(1)

    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    print(f"✅ Loaded {len(dataset)} test cases\n")

    # Run evaluation
    print("🔄 Running evaluation pipeline...\n")
    results = run_eval(dataset)

    # Print results
    print("\n" + "="*80)
    print("📊 Results")
    print("="*80)

    for i, result in enumerate(results, 1):
        print(f"\n[Test {i}]")
        print(f"Task: {result['test_case']['task']}")
        print(f"Output: {result['output'][:150]}{'...' if len(result['output']) > 150 else ''}")
        print(f"Score: {result['score']}/10 (placeholder)")

    # Summary
    print("\n" + "="*80)
    print(f"📈 Summary: {len(results)} tests executed")
    print("⚠️  Note: Scores are placeholder (always 10)")
    print("💡 Next step: Implement real grading function")
    print("="*80)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import json
from anthropic import Anthropic

client = Anthropic()

# Prompt v1 (basic, we'll use later for evaluation)
PROMPT_V1 = "Please provide a solution to the following task: {task}"

# Helper functions
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

def generate_dataset(n=5):
    """Generate an evaluation dataset of AWS-related tasks with format field.

    Uses Claude to generate N diverse tasks that require:
    - Writing a single Python function (format: "python")
    - Creating a single JSON config (format: "json")
    - Writing a single regex (format: "regex")

    All tasks are AWS-specific and avoid large code requirements.
    """

    print(f"🔄 Generating {n} AWS tasks using Claude...\n")

    # Prompt to generate the dataset
    generation_prompt = f"""Generate a JSON array of exactly {n} AWS-related code/config tasks.
Each task should require writing ONE small piece of code/config:
- A single Python function (lambda, parser, validator) → format: "python"
- A single JSON config object (EventBridge rule, IAM policy snippet) → format: "json"
- A single regex pattern → format: "regex"

Make tasks realistic and diverse (different AWS services: Lambda, S3, IAM, EventBridge, CloudWatch, etc).
Avoid tasks requiring more than 20 lines of code.

Return ONLY valid JSON array with format: [{{"task": "description", "format": "python|json|regex"}}]
No explanation, just JSON."""

    messages = []
    add_user_message(messages, generation_prompt)

    # Use prefill technique to get clean JSON
    add_assistant_message(messages, "```json")

    # Call Claude with stop_sequences to halt at closing ```
    response = chat(
        messages,
        stop_sequences=["```"]
    )

    json_text = extract_text(response).strip()

    # Parse the JSON
    try:
        dataset = json.loads(json_text)
        print(f"✅ Successfully generated {len(dataset)} tasks\n")
        return dataset
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
        print(f"Raw text: {json_text}")
        return []

def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    print("="*80)
    print("DEMO: Automatic Eval Dataset Generation")
    print("="*80)
    print()

    # Generate dataset
    dataset = generate_dataset(n=5)

    if not dataset:
        print("Failed to generate dataset")
        exit(1)

    # Print the dataset
    print("="*80)
    print("📊 Generated Dataset:")
    print("="*80)
    for i, item in enumerate(dataset, 1):
        print(f"\n{i}. Task: {item['task']}")

    # Save to file
    output_file = "dataset.json"
    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"\n✅ Dataset saved to {output_file}")
    print(f"📈 Total tasks: {len(dataset)}")

if __name__ == "__main__":
    main()

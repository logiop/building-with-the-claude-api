#!/usr/bin/env python3

import os
from anthropic import Anthropic

client = Anthropic()

REVIEW_CLASSIFIER_SYSTEM = """You are a sentiment classifier for customer reviews.
Your task is to classify each review as exactly one of:
- positive
- negative
- neutral

Respond with ONLY the classification word, nothing else. No explanation, no punctuation."""

TEST_CASES = [
    {
        "input": "This product is amazing! I love it so much.",
        "expected": "positive"
    },
    {
        "input": "Terrible quality. Broke after one day. Do not buy.",
        "expected": "negative"
    },
    {
        "input": "It's a product. It works fine.",
        "expected": "neutral"
    },
    {
        "input": "Not bad, but could be better for the price.",
        "expected": "neutral"
    },
    {
        "input": "BEST PURCHASE EVER!!! Highly recommend!!!",
        "expected": "positive"
    },
    {
        "input": "Waste of money. I'm returning it immediately.",
        "expected": "negative"
    },
    {
        "input": "It's okay I guess. Some good parts, some bad parts.",
        "expected": "neutral"
    },
    {
        "input": "Sure it works but it's so overpriced and the customer service was rude.",
        "expected": "negative"
    },
    {
        "input": "Oh wow, AMAZING quality... said no one ever. Total garbage.",
        "expected": "negative"
    },
    {
        "input": "Good value for money. Would buy again.",
        "expected": "positive"
    },
]


def extract_text(response):
    for block in response.content:
        if hasattr(block, 'text'):
            return block.text
    return ""


def run_eval(prompt_system, test_cases):
    passed = 0
    failed_cases = []

    for i, test_case in enumerate(test_cases, 1):
        messages = [
            {"role": "user", "content": test_case["input"]}
        ]

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            system=prompt_system,
            messages=messages,
        )

        actual = extract_text(response).strip().lower()
        expected = test_case["expected"].strip().lower()

        if actual == expected:
            passed += 1
        else:
            failed_cases.append({
                "test_num": i,
                "input": test_case["input"],
                "expected": expected,
                "actual": actual,
            })

    accuracy = (passed / len(test_cases)) * 100
    return {
        "passed": passed,
        "total": len(test_cases),
        "accuracy": accuracy,
        "failed": failed_cases,
    }


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    print("=" * 80)
    print("DEMO: Prompt Evaluation Pipeline")
    print("=" * 80)
    print(f"\n📝 Sistema: Classificatore di Sentimento")
    print(f"📊 Test Cases: {len(TEST_CASES)}\n")

    results = run_eval(REVIEW_CLASSIFIER_SYSTEM, TEST_CASES)

    print("=" * 80)
    print("📊 RISULTATI")
    print("=" * 80)
    print(f"\n✅ Test Passati: {results['passed']}/{results['total']}")
    print(f"📈 Accuratezza: {results['accuracy']:.1f}%\n")

    if results["failed"]:
        print("=" * 80)
        print("❌ TEST FALLITI")
        print("=" * 80)
        for failed in results["failed"]:
            print(f"\n🔴 Test #{failed['test_num']}:")
            print(f"   Input:    \"{failed['input']}\"")
            print(f"   Expected: {failed['expected']}")
            print(f"   Got:      {failed['actual']}")
    else:
        print("🎉 Tutti i test passati!")

    print("\n" + "=" * 80)
    print("💡 ANALISI")
    print("=" * 80)
    print(f"""
Se avessimo testato il prompt "a occhio":
  - Avremmo provato 2-3 esempi e pensato "funziona!"
  - Ma il vero accuracy è solo {results['accuracy']:.0f}%

I test falliti mostrano ESATTAMENTE dove il prompt è debole:
  - Casi sarcastici: {sum(1 for f in results['failed'] if 'never' in f['input'].lower())}
  - Recensioni miste: {sum(1 for f in results['failed'] if 'and' in f['input'].lower())}

Ora sappiamo COSA migliorare, non solo che "non funziona".
""")


if __name__ == "__main__":
    main()

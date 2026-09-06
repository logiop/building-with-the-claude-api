#!/usr/bin/env python3

import os
from anthropic import Anthropic

client = Anthropic()

# Questo è un prompt DEBOLE - è vago e senza istruzioni chiare
WEAK_REVIEW_CLASSIFIER = """Classify this customer review."""

TEST_CASES = [
    {"input": "This product is amazing! I love it so much.", "expected": "positive"},
    {"input": "Terrible quality. Broke after one day. Do not buy.", "expected": "negative"},
    {"input": "It's a product. It works fine.", "expected": "neutral"},
    {"input": "Not bad, but could be better for the price.", "expected": "neutral"},
    {"input": "BEST PURCHASE EVER!!! Highly recommend!!!", "expected": "positive"},
    {"input": "Waste of money. I'm returning it immediately.", "expected": "negative"},
    {"input": "It's okay I guess. Some good parts, some bad parts.", "expected": "neutral"},
    {"input": "Sure it works but it's so overpriced and the customer service was rude.", "expected": "negative"},
    {"input": "Oh wow, AMAZING quality... said no one ever. Total garbage.", "expected": "negative"},
    {"input": "Good value for money. Would buy again.", "expected": "positive"},
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
        messages = [{"role": "user", "content": test_case["input"]}]

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=50,
            system=prompt_system,
            messages=messages,
        )

        actual_raw = extract_text(response).strip().lower()
        expected = test_case["expected"].strip().lower()

        # Cerca se la risposta contiene la categoria attesa (il prompt debole dà risposte lunghe)
        actual = None
        for category in ["positive", "negative", "neutral"]:
            if category in actual_raw:
                actual = category
                break

        if actual == expected:
            passed += 1
        else:
            failed_cases.append({
                "test_num": i,
                "input": test_case["input"],
                "expected": expected,
                "actual": actual if actual else f"(non riconosciuto: '{actual_raw[:30]}...')",
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
    print("DEMO: Prompt Evaluation - Comparing STRONG vs WEAK Prompt")
    print("=" * 80)

    print("\n⚠️  NOTA: Questo demo usa un prompt DEBOLE per mostrare i fallimenti\n")

    results = run_eval(WEAK_REVIEW_CLASSIFIER, TEST_CASES)

    print("=" * 80)
    print("📊 RISULTATI DEL PROMPT DEBOLE")
    print("=" * 80)
    print(f"\n✅ Test Passati: {results['passed']}/{results['total']}")
    print(f"📈 Accuratezza: {results['accuracy']:.1f}%\n")

    if results["failed"]:
        print("=" * 80)
        print("❌ TEST FALLITI - Dove il Prompt Fallisce")
        print("=" * 80)
        for failed in results["failed"]:
            print(f"\n🔴 Test #{failed['test_num']}:")
            print(f"   Input:    \"{failed['input']}\"")
            print(f"   Expected: {failed['expected']}")
            print(f"   Got:      {failed['actual']}")

    print("\n" + "=" * 80)
    print("💡 LEZIONE CHIAVE")
    print("=" * 80)
    print(f"""
TESTING "A OCCHIO" vs EVALUATION OGGETTIVA:

Scenario A: Testing "A Occhio"
  ❌ Provo il prompt su 2-3 esempi a mano
  ❌ Funziona su quelli → penso "Great!"
  ❌ Lo metto in produzione
  ❌ Scopro solo dopo che fallisce su altri input
  ⏰ Tempo perso: TANTO

Scenario B: Evaluation Oggettiva
  ✅ Crei {len(TEST_CASES)} test case diversificati
  ✅ Lo esegui e scopri accuracy reale: {results['accuracy']:.0f}%
  ✅ Vedi ESATTAMENTE quali test falliscono
  ✅ Sai COSA migliorare PRIMA di mettere live
  ⏰ Tempo risparmiato: TANTO

Questo prompt debole fallisce su:
  - Riconoscimento dell'output (non risponde con "positive/negative/neutral")
  - Non ha istruzioni chiare su come formattare la risposta

Con evaluation, saprei IMMEDIATAMENTE che il prompt non funziona!
""")


if __name__ == "__main__":
    main()

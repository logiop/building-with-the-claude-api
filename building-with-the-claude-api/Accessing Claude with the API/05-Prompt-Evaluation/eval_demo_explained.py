#!/usr/bin/env python3
"""
Demo di una Mini Pipeline di Prompt Evaluation.
Dimostra il valore di testare i prompt in modo OGGETTIVO invece che "a occhio".
"""

# Importa il modulo os per accedere alle variabili d'ambiente
import os

# Importa la classe Anthropic per comunicare con l'API di Claude
from anthropic import Anthropic

# Crea un'istanza del client Anthropic
client = Anthropic()

# System prompt per il classificatore di sentimento
# Notiamo che il prompt è MOLTO specifico: "Respond with ONLY the classification word"
# Questo rende facile verificare se la risposta è corretta
REVIEW_CLASSIFIER_SYSTEM = """You are a sentiment classifier for customer reviews.
Your task is to classify each review as exactly one of:
- positive
- negative
- neutral

Respond with ONLY the classification word, nothing else. No explanation, no punctuation."""

# Dataset di test: una lista di dizionari con input e risultato atteso
# Includiamo 10 test cases, alcuni facili e alcuni con casi limite
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
        "expected": "negative"  # Questo è sarcasmo - un caso limite difficile!
    },
    {
        "input": "Good value for money. Would buy again.",
        "expected": "positive"
    },
]


# FUNZIONE: extract_text
# Scopo: Estrarre il testo dalla risposta di Claude
def extract_text(response):
    """Estrae il primo blocco di testo dalla risposta di Claude."""
    for block in response.content:
        if hasattr(block, 'text'):
            return block.text
    return ""


# FUNZIONE: run_eval
# Scopo: Eseguire la evaluation del prompt su tutti i test case
# IMPORTANTE: Questa è la "pipeline di evaluation" - il cuore della lezione!
def run_eval(prompt_system, test_cases):
    """
    Valuta un prompt su una serie di test cases.

    Returns: dizionario con:
        - passed: numero di test passati
        - total: numero totale di test
        - accuracy: percentuale di accuratezza
        - failed: lista dei test falliti (per debug)
    """
    # Contatori per i risultati
    passed = 0
    failed_cases = []

    # Itera su ogni test case
    for i, test_case in enumerate(test_cases, 1):
        # Costruisci il messaggio con l'input di test
        messages = [
            {"role": "user", "content": test_case["input"]}
        ]

        # Chiama Claude con il prompt che stiamo valutando
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,  # Bastano pochi token per una sola parola
            system=prompt_system,  # Questo è il prompt che stiamo testando
            messages=messages,
        )

        # Estrai la risposta e normalizzala (minuscole, senza spazi)
        actual = extract_text(response).strip().lower()
        expected = test_case["expected"].strip().lower()

        # Confronta la risposta con l'atteso
        if actual == expected:
            # ✅ Test passato
            passed += 1
        else:
            # ❌ Test fallito - salva per il report
            failed_cases.append({
                "test_num": i,
                "input": test_case["input"],
                "expected": expected,
                "actual": actual,
            })

    # Calcola l'accuratezza percentuale
    accuracy = (passed / len(test_cases)) * 100

    # Ritorna i risultati
    return {
        "passed": passed,
        "total": len(test_cases),
        "accuracy": accuracy,
        "failed": failed_cases,
    }


# FUNZIONE: main
# Scopo: Eseguire la demo e stampare il report
def main():
    # Verifica che la chiave API sia disponibile
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    # Stampa l'intestazione della demo
    print("=" * 80)
    print("DEMO: Prompt Evaluation Pipeline")
    print("=" * 80)
    print(f"\n📝 Sistema: Classificatore di Sentimento")
    print(f"📊 Test Cases: {len(TEST_CASES)}\n")

    # Esegui la evaluation
    # QUESTO è il momento cruciale - stiamo valutando il prompt OGGETTIVAMENTE
    results = run_eval(REVIEW_CLASSIFIER_SYSTEM, TEST_CASES)

    # Stampa i risultati
    print("=" * 80)
    print("📊 RISULTATI")
    print("=" * 80)
    print(f"\n✅ Test Passati: {results['passed']}/{results['total']}")
    print(f"📈 Accuratezza: {results['accuracy']:.1f}%\n")

    # Se ci sono test falliti, stampa il dettaglio
    if results["failed"]:
        print("=" * 80)
        print("❌ TEST FALLITI")
        print("=" * 80)
        for failed in results["failed"]:
            print(f"\n🔴 Test #{failed['test_num']}:")
            print(f"   Input:    \"{failed['input']}\"")
            print(f"   Expected: {failed['expected']}")
            print(f"   Got:      {failed['actual']}")
            print(f"   → Insight: Qui il prompt ha sbagliato!")
    else:
        print("🎉 Tutti i test passati!")

    # Analisi finale
    print("\n" + "=" * 80)
    print("💡 ANALISI: Perché L'Evaluation Oggettiva È Superiore")
    print("=" * 80)
    print(f"""
SCENARIO 1: Testing "a occhio" (❌ Sbagliato)
  - Testi il prompt su 2-3 esempi a mano
  - Vedi che funziona per i casi semplici
  - Pensi: "Great! Il prompt funziona!"
  - Ma il vero accuracy è solo {results['accuracy']:.0f}%
  - Scopri il problema solo in produzione 😱

SCENARIO 2: Evaluation Oggettiva (✅ Corretto)
  - Crei un dataset di test case diversificati
  - Esegui automaticamente su tutti
  - Scopri l'accuratezza reale: {results['accuracy']:.0f}%
  - VEDI ESATTAMENTE quali test falliscono
  - Sai COSA migliorare nel prompt

I test falliti ti dicono:
""")
    if results["failed"]:
        print(f"  - Sarcasmo: {sum(1 for f in results['failed'] if 'never' in f['input'].lower())} casi")
        print(f"  - Sentimenti misti: {sum(1 for f in results['failed'] if 'and' in f['input'].lower())} casi")
    print("""
Ora puoi ITERARE: modifica il prompt, rirun, vedi se accuracy migliora!
""")


# Verifica che il file sia eseguito direttamente
if __name__ == "__main__":
    main()

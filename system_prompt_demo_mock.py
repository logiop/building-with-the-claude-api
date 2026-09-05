#!/usr/bin/env python3
"""
Demo MOCK per imparare la differenza tra usare e NON usare un system prompt.
Questa versione non ha bisogno di una vera chiave API.
"""

# System prompt del tutor di matematica
MATH_TUTOR_SYSTEM = """You are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step."""

# Risposte simulate per illustrare le differenze
RESPONSE_WITHOUT_SYSTEM = """
The solution to 5x + 2 = 3 for x is:

5x + 2 = 3
5x = 3 - 2
5x = 1
x = 1/5 = 0.2

So x = 0.2 or 1/5.
"""

RESPONSE_WITH_SYSTEM = """
Great question! Let's work through this step by step.

First, I want you to think about what we're trying to do. We have the equation:
5x + 2 = 3

Here's my first question for you: What do you think we should do first to isolate the terms with 'x'?
(Hint: Think about moving the +2 to the other side of the equation. What operation would you use?)

Once you answer that, we can continue to the next step!
"""


def main():
    student_question = "How do I solve 5x + 2 = 3 for x?"

    print("=" * 70)
    print("DEMO: System Prompt vs. No System Prompt")
    print("=" * 70)
    print(f"\n📚 Domanda dello studente: {student_question}\n")

    # ===== PRIMA RISPOSTA: SENZA SYSTEM PROMPT =====
    print("-" * 70)
    print("1️⃣  RISPOSTA SENZA SYSTEM PROMPT (Claude agisce normalmente)")
    print("-" * 70)
    print("Comportamento: Claude risponde direttamente, fornendo la soluzione completa.")
    print()
    print(RESPONSE_WITHOUT_SYSTEM)

    # ===== SECONDA RISPOSTA: CON SYSTEM PROMPT =====
    print("-" * 70)
    print("2️⃣  RISPOSTA CON SYSTEM PROMPT (Tutor di matematica)")
    print("-" * 70)
    print("Comportamento: Claude guida lo studente passo passo, NON risponde direttamente.")
    print()
    print(RESPONSE_WITH_SYSTEM)

    print("=" * 70)
    print("🔍 ANALISI DELLE DIFFERENZE")
    print("=" * 70)
    print("""
1. SENZA SYSTEM PROMPT:
   - Claude fornisce direttamente la risposta finale
   - Spiega il processo matematico
   - Lo studente ottiene la soluzione subito

2. CON SYSTEM PROMPT:
   - Claude fa domande guida
   - Aiuta lo studente a pensare autonomamente
   - Non svela la risposta, ma guida verso la soluzione
   - Promuove l'apprendimento attivo

📌 CONCETTO CHIAVE: Lo stesso modello, stessa domanda, ma il system prompt
   cambia COMPLETAMENTE il comportamento e lo stile di risposta!
""")


if __name__ == "__main__":
    main()

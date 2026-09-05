#!/usr/bin/env python3
"""
Demo per imparare la differenza tra usare e NON usare un system prompt.
Confronto: stessa domanda, risposte completamente diverse!
"""

import os
from anthropic import Anthropic

client = Anthropic()

# System prompt del tutor di matematica
MATH_TUTOR_SYSTEM = """You are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step."""


def chat(messages, system=None):
    """
    Costruisce una chiamata all'API con i parametri corretti.

    IMPORTANTE: Il parametro 'system' NON deve essere passato se è None!
    L'API di Anthropic non accetta esplicitamente system=None.
    Se vogliamo omettere il system prompt, semplicemente non lo includiamo nel dizionario.
    """
    params = {
        "model": "claude-opus-5",
        "max_tokens": 1024,
        "messages": messages,
    }

    # Aggiungi 'system' ai parametri SOLO se è stato fornito
    if system is not None:
        params["system"] = system

    return client.messages.create(**params)


def main():
    # Verifica che la chiave API sia disponibile
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: La variabile d'ambiente ANTHROPIC_API_KEY non è impostata!")
        print("\nPer eseguire questo script:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...' (inserisci la tua chiave)")
        print("  python3 system_prompt_demo.py")
        print("\nOttieni una chiave API gratuitamente da: https://console.anthropic.com/account/keys")
        exit(1)

    student_question = "How do I solve 5x + 2 = 3 for x?"

    print("=" * 70)
    print("DEMO: System Prompt vs. No System Prompt")
    print("=" * 70)
    print(f"\nDomanda dello studente: {student_question}\n")

    # ===== PRIMA RISPOSTA: SENZA SYSTEM PROMPT =====
    print("-" * 70)
    print("1️⃣  RISPOSTA SENZA SYSTEM PROMPT (Claude agisce normalmente)")
    print("-" * 70)

    response_without_system = chat(
        messages=[{"role": "user", "content": student_question}],
        system=None  # Nessun system prompt
    )

    answer_without = response_without_system.content[0].text
    print(answer_without)
    print()

    # ===== SECONDA RISPOSTA: CON SYSTEM PROMPT =====
    print("-" * 70)
    print("2️⃣  RISPOSTA CON SYSTEM PROMPT (Tutor di matematica)")
    print("-" * 70)

    response_with_system = chat(
        messages=[{"role": "user", "content": student_question}],
        system=MATH_TUTOR_SYSTEM  # Con system prompt del tutor
    )

    answer_with = response_with_system.content[0].text
    print(answer_with)
    print()

    print("=" * 70)
    print("ANALISI DELLE DIFFERENZE")
    print("=" * 70)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
from anthropic import Anthropic

client = Anthropic()

MATH_TUTOR_SYSTEM = """You are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step."""


def chat(messages, system=None):
    params = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "messages": messages,
    }

    if system is not None:
        params["system"] = system

    return client.messages.create(**params)


def main():
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

    print("-" * 70)
    print("1️⃣  RISPOSTA SENZA SYSTEM PROMPT (Claude agisce normalmente)")
    print("-" * 70)

    response_without_system = chat(
        messages=[{"role": "user", "content": student_question}],
        system=None
    )

    answer_without = next((block.text for block in response_without_system.content if hasattr(block, 'text')), "")
    print(answer_without)
    print()

    print("-" * 70)
    print("2️⃣  RISPOSTA CON SYSTEM PROMPT (Tutor di matematica)")
    print("-" * 70)

    response_with_system = chat(
        messages=[{"role": "user", "content": student_question}],
        system=MATH_TUTOR_SYSTEM
    )

    answer_with = next((block.text for block in response_with_system.content if hasattr(block, 'text')), "")
    print(answer_with)
    print()

    print("=" * 70)
    print("ANALISI DELLE DIFFERENZE")
    print("=" * 70)


if __name__ == "__main__":
    main()

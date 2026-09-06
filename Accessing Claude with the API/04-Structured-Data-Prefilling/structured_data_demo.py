#!/usr/bin/env python3

import os
import json
from anthropic import Anthropic

client = Anthropic()
model = "claude-haiku-4-5-20251001"


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat(messages, system=None, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": 500,
        "messages": messages,
    }

    if system is not None:
        params["system"] = system

    if stop_sequences is not None:
        params["stop_sequences"] = stop_sequences

    return client.messages.create(**params)


def extract_text(response):
    for block in response.content:
        if hasattr(block, 'text'):
            return block.text
    return ""


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    print("=" * 80)
    print("DEMO: Structured Data con Prefilling + Stop Sequences")
    print("=" * 80)

    # ===== ESEMPIO 1: RISPOSTA DI DEFAULT (SPORCA) =====
    print("\n" + "=" * 80)
    print("1️⃣  SENZA TRUCCHI - Risposta di Default (Sporca)")
    print("=" * 80)

    messages_1 = []
    add_user_message(
        messages_1,
        "Generate an AWS EventBridge rule in JSON format that triggers a Lambda when an EC2 instance starts. Include the exact JSON only."
    )

    response_1 = chat(messages_1)
    raw_response_1 = extract_text(response_1)

    print("\n📋 Risposta Grezza:")
    print(raw_response_1)

    print("\n⚠️  PROBLEMA:")
    print("   - Ha ```json intorno")
    print("   - Ha testo spiegativo prima e dopo")
    print("   - Non è facile da parsare direttamente")

    # ===== ESEMPIO 2: CON PREFILL + STOP SEQUENCE (PULITA) =====
    print("\n" + "=" * 80)
    print("2️⃣  CON PREFILL + STOP SEQUENCES - Risposta Pulita")
    print("=" * 80)

    messages_2 = []
    add_user_message(
        messages_2,
        "Generate an AWS EventBridge rule in JSON format that triggers a Lambda when an EC2 instance starts."
    )

    add_assistant_message(messages_2, "```json")

    response_2 = chat(messages_2, stop_sequences=["```"])
    raw_response_2 = extract_text(response_2)

    print("\n📋 Risposta Grezza (con prefill):")
    print("```json" + raw_response_2 + "```")

    print("\n✅ VANTAGGIO:")
    print("   - Solo JSON puro")
    print("   - Niente testo extra")
    print("   - Facile da parsare")

    json_string = raw_response_2.strip()
    try:
        parsed_json = json.loads(json_string)
        print("\n✨ JSON Parsato Correttamente:")
        print(json.dumps(parsed_json, indent=2))
    except json.JSONDecodeError as e:
        print(f"\n❌ Errore parsing JSON: {e}")

    # ===== ESEMPIO 3: LISTA PUNTATA CON LA STESSA TECNICA =====
    print("\n" + "=" * 80)
    print("3️⃣  BONUS - Snippet di Codice Python (Stessa Tecnica)")
    print("=" * 80)

    messages_3 = []
    add_user_message(
        messages_3,
        "Write a Python function to validate an email address. Just the code."
    )

    add_assistant_message(messages_3, "```python")

    response_3 = chat(messages_3, stop_sequences=["```"])
    raw_response_3 = extract_text(response_3)

    print("\n📋 Risposta (Codice Python):")
    print("```python")
    print(raw_response_3)
    print("```")

    print("\n✅ Anche qui:")
    print("   - Prefill: '```python\\n' (inizia il blocco codice)")
    print("   - Stop: '```' (ferma dopo il codice)")
    print("   - Output pulito e copiabile")

    print("\n" + "=" * 80)
    print("🎯 CONCLUSIONI")
    print("=" * 80)
    print("""
PREFILL + STOP SEQUENCES permette di:
  ✅ Generare output strutturato PULITO
  ✅ Eliminare il testo spiegativo
  ✅ Parsare direttamente in JSON/CSV/ecc
  ✅ Integrare l'output in app senza cleaning

QUANDO USARE:
  ✅ Generare JSON, CSV, XML
  ✅ Code snippets
  ✅ Liste strutturate
  ✅ Output che va direttamente in un database
  ✅ API che deve ritornare dati puliti
""")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
from anthropic import Anthropic

client = Anthropic()

MOVIE_GENERATOR_SYSTEM = """You are a creative movie pitch generator.
Generate short, unique, and imaginative movie plot ideas. Be creative and diverse in your suggestions."""


def chat(messages, system=None):
    params = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 150,
        "messages": messages,
    }

    if system is not None:
        params["system"] = system

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

    movie_prompt = "Give me a one-sentence idea for a movie plot."

    print("=" * 80)
    print("DEMO: Temperature Parameter (Creatività vs Determinismo)")
    print("=" * 80)
    print(f"\n📽️  Domanda: {movie_prompt}\n")

    print("=" * 80)
    print("🎯 3 Risposte Successive (Mostra la Variabilità Naturale)")
    print("=" * 80)
    print("Facciamo 3 chiamate identiche alla stessa domanda.")
    print("Vedrai che le risposte variano naturalmente - questo è il \"sampling\"!\n")

    responses = []
    for i in range(1, 4):
        response = chat(
            messages=[{"role": "user", "content": movie_prompt}],
            system=MOVIE_GENERATOR_SYSTEM
        )
        answer = extract_text(response)
        responses.append(answer)
        print(f"📌 Risposta {i}:")
        print(f"   {answer}\n")

    print("=" * 80)
    print("🔍 ANALISI: Guarda Come Variano le Risposte")
    print("=" * 80)
    print("\nTutte e tre le risposte sono diverse, anche se abbiamo fatto la stessa domanda!")
    print("Questo succede perché Claude usa sampling probabilistico per generare il testo.")
    print("\nSe potessimo usare un parametro 'temperature' basso (come 0.0), le risposte")
    print("sarebbero più simili tra loro. Con 'temperature' alto (come 1.0 o 2.0),")
    print("sarebbero ancora più diverse e creative.")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

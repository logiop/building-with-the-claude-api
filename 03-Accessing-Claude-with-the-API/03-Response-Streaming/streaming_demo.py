#!/usr/bin/env python3

import os
import time
from anthropic import Anthropic

client = Anthropic()

DEMO_SYSTEM = "You are a helpful assistant. Provide clear and detailed responses."


def chat_blocking(messages):
    print("\n⏳ Versione BLOCCANTE (aspetta tutto il messaggio)")
    print("-" * 80)

    start_time = time.time()
    print(f"[{time.time() - start_time:.3f}s] Inizio richiesta...")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=DEMO_SYSTEM,
        messages=messages,
    )

    first_byte_time = time.time() - start_time
    print(f"[{first_byte_time:.3f}s] ⚠️ PRIMO TESTO APPARE ORA:")
    print()

    answer = response.content[0].text
    print(answer)

    total_time = time.time() - start_time
    print()
    print(f"📊 Tempo totale: {total_time:.3f}s")
    print(f"⏱️  Attesa prima di vedere qualcosa: {first_byte_time:.3f}s")

    return answer


def chat_streaming(messages):
    print("\n📡 Versione STREAMING (vedi il testo man mano)")
    print("-" * 80)

    start_time = time.time()
    print(f"[{time.time() - start_time:.3f}s] Inizio richiesta...")

    first_chunk_time = None
    full_text = ""

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=DEMO_SYSTEM,
        messages=messages,
    ) as stream:
        print(f"[{time.time() - start_time:.3f}s] ✅ PRIMO CHUNK APPARE ORA:")
        print()

        for text in stream.text_stream:
            if first_chunk_time is None:
                first_chunk_time = time.time() - start_time

            print(text, end="", flush=True)
            full_text += text

        final_message = stream.get_final_message()

    print("\n")
    total_time = time.time() - start_time
    print(f"📊 Tempo totale: {total_time:.3f}s")
    print(f"⏱️  Attesa prima di vedere il primo chunk: {first_chunk_time:.3f}s")

    return full_text


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    prompt = "Write a short paragraph describing a fictional database engine. Make it detailed and technical."

    print("=" * 80)
    print("DEMO: Response Streaming")
    print("=" * 80)
    print(f"\n📝 Domanda: {prompt}\n")

    messages = [{"role": "user", "content": prompt}]

    print("\n" + "=" * 80)
    print("CONFRONTO: Bloccante vs Streaming")
    print("=" * 80)

    blocking_response = chat_blocking(messages)

    time.sleep(1)

    streaming_response = chat_streaming(messages)

    print("\n" + "=" * 80)
    print("📌 CONCLUSIONI")
    print("=" * 80)
    print("""
STREAMING è MEGLIO quando:
  ✅ Vuoi mostrare il testo man mano (UX migliore)
  ✅ L'utente vede qualcosa subito (time-to-first-byte)
  ✅ Risposte lunghe (non aspetti tutto in silenzio)
  ✅ Chatbot interattivo (senti che "respira")

BLOCCANTE è MEGLIO quando:
  ✅ Devi processare la risposta completa prima
  ✅ Non hai bisogno di mostrare il testo
  ✅ Scrivi tutto a un database
  ✅ Risposte corte (la differenza è minima)
""")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Demo dello Streaming: come mostrare le risposte di Claude man mano che arrivano.
"""

# Importa il modulo os per accedere alle variabili d'ambiente
import os

# Importa il modulo time per misurare il tempo di esecuzione
import time

# Importa la classe Anthropic per comunicare con l'API di Claude
from anthropic import Anthropic

# Crea un'istanza del client Anthropic
client = Anthropic()

# System prompt per il demo
DEMO_SYSTEM = "You are a helpful assistant. Provide clear and detailed responses."


# FUNZIONE: chat_blocking
# Scopo: Dimostrare come funziona una richiesta SENZA streaming
# Differenza: Aspetti tutto il messaggio prima di vederlo
def chat_blocking(messages):
    """
    Invia una richiesta senza streaming e stampa il tempo di attesa totale.
    """
    print("\n⏳ Versione BLOCCANTE (aspetta tutto il messaggio)")
    print("-" * 80)

    # Registra il tempo di inizio
    start_time = time.time()
    print(f"[{time.time() - start_time:.3f}s] Inizio richiesta...")

    # Chiama l'API SENZA streaming
    # client.messages.create() è "bloccante": aspetta la risposta completa
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=DEMO_SYSTEM,
        messages=messages,
    )

    # Calcola il tempo trascorso fino a quando la risposta è arrivata completamente
    # In realtà, senza streaming, devi aspettare TUTTO prima di vederlo
    first_byte_time = time.time() - start_time
    print(f"[{first_byte_time:.3f}s] ⚠️ PRIMO TESTO APPARE ORA:")
    print()

    # Estrai il testo dalla risposta
    answer = response.content[0].text
    print(answer)

    # Calcola il tempo totale
    total_time = time.time() - start_time
    print()
    print(f"📊 Tempo totale: {total_time:.3f}s")
    print(f"⏱️  Attesa prima di vedere qualcosa: {first_byte_time:.3f}s")

    return answer


# FUNZIONE: chat_streaming
# Scopo: Dimostrare come funziona una richiesta CON streaming
# Differenza: Vedi il testo man mano che arriva (migliore UX)
def chat_streaming(messages):
    """
    Invia una richiesta CON streaming e stampa il testo man mano che arriva.
    Misura il tempo prima che appaia il PRIMO chunk.
    """
    print("\n📡 Versione STREAMING (vedi il testo man mano)")
    print("-" * 80)

    # Registra il tempo di inizio
    start_time = time.time()
    print(f"[{time.time() - start_time:.3f}s] Inizio richiesta...")

    # Variabile per tracciare il tempo del primo chunk
    first_chunk_time = None
    # Variabile per accumulare il testo completo
    full_text = ""

    # IMPORTANTE: Usa client.messages.stream() invece di client.messages.create()
    # Questo abilita lo streaming delle risposte
    # Il "with" statement è un context manager che gestisce il flusso
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=DEMO_SYSTEM,
        messages=messages,
    ) as stream:
        print(f"[{time.time() - start_time:.3f}s] ✅ PRIMO CHUNK APPARE ORA:")
        print()

        # stream.text_stream è un iteratore che restituisce chunks di testo
        # Ogni volta che Claude genera un pezzo, lo ricevi subito
        for text in stream.text_stream:
            # Registra il tempo del primo chunk
            if first_chunk_time is None:
                first_chunk_time = time.time() - start_time

            # Stampa il testo man mano che arriva (senza andare a capo)
            # flush=True forza Python a mostrare il testo subito (non aspettare)
            print(text, end="", flush=True)

            # Accumula il testo per recuperarlo dopo
            full_text += text

        # Dopo lo streaming, recupera il messaggio finale completo
        # Questo contiene metadati come stop_reason, usage, ecc.
        final_message = stream.get_final_message()

    print("\n")
    total_time = time.time() - start_time
    print(f"📊 Tempo totale: {total_time:.3f}s")
    print(f"⏱️  Attesa prima di vedere il primo chunk: {first_chunk_time:.3f}s")

    return full_text


# FUNZIONE: main
# Scopo: Eseguire il demo e confrontare i due approcci
def main():
    # Verifica che la chiave API sia disponibile
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    # Prompt che genererà una risposta lunga (per vedere bene lo streaming)
    prompt = "Write a short paragraph describing a fictional database engine. Make it detailed and technical."

    print("=" * 80)
    print("DEMO: Response Streaming")
    print("=" * 80)
    print(f"\n📝 Domanda: {prompt}\n")

    # Prepara il messaggio
    messages = [{"role": "user", "content": prompt}]

    print("\n" + "=" * 80)
    print("CONFRONTO: Bloccante vs Streaming")
    print("=" * 80)

    # ===== PARTE 1: VERSIONE BLOCCANTE =====
    blocking_response = chat_blocking(messages)

    # Aspetta un po' prima di fare la seconda richiesta
    time.sleep(1)

    # ===== PARTE 2: VERSIONE STREAMING =====
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


# Verifica che il file sia eseguito direttamente
if __name__ == "__main__":
    main()

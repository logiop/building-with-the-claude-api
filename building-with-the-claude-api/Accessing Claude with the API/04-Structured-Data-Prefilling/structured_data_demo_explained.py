#!/usr/bin/env python3
"""
Demo di Structured Data con Prefilling + Stop Sequences.
Come generare JSON pulito, CSV, liste, ecc senza testo spiegativo.
"""

# Importa il modulo os per accedere alle variabili d'ambiente
import os

# Importa il modulo json per parsare le risposte JSON
import json

# Importa la classe Anthropic per comunicare con l'API di Claude
from anthropic import Anthropic

# Crea un'istanza del client Anthropic
client = Anthropic()

# Specifica il modello da usare
model = "claude-haiku-4-5-20251001"


# FUNZIONE: add_user_message
# Scopo: Aggiungere un messaggio utente alla lista messages
def add_user_message(messages, text):
    """
    Aggiunge un messaggio dell'utente alla cronologia della conversazione.
    """
    messages.append({"role": "user", "content": text})


# FUNZIONE: add_assistant_message
# Scopo: Aggiungere un messaggio assistente (pre-riempito) alla lista messages
# IMPORTANTE: Questa funzione è usata per il "prefill" technique!
def add_assistant_message(messages, text):
    """
    Aggiunge un messaggio dell'assistente (Claude) alla cronologia.
    Usato per il PREFILLING: facciamo credere a Claude che ha già iniziato a scrivere.
    """
    messages.append({"role": "assistant", "content": text})


# FUNZIONE: chat
# Scopo: Inviare messaggi a Claude con opzione per stop_sequences
def chat(messages, system=None, stop_sequences=None):
    """
    Chiama l'API di Claude con support per stop_sequences.

    Args:
        messages: la cronologia della conversazione
        system: system prompt opzionale
        stop_sequences: lista di stringhe che interrompono la generazione
                       Es: ["```"] ferma quando Claude scrive ```
    """
    # Crea il dizionario dei parametri
    params = {
        "model": model,
        "max_tokens": 500,
        "messages": messages,
    }

    # Aggiungi il system prompt se fornito
    if system is not None:
        params["system"] = system

    # IMPORTANTE: Aggiungi stop_sequences se fornite
    # stop_sequences dice all'API: "Fermati quando vedi questa stringa"
    if stop_sequences is not None:
        params["stop_sequences"] = stop_sequences

    return client.messages.create(**params)


# FUNZIONE: extract_text
# Scopo: Estrarre il testo dalla risposta
def extract_text(response):
    """
    Estrae il primo blocco di testo dalla risposta di Claude.
    """
    for block in response.content:
        if hasattr(block, 'text'):
            return block.text
    return ""


# FUNZIONE: main
# Scopo: Dimostrare la differenza tra prefill e non-prefill
def main():
    # Verifica che la chiave API sia disponibile
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

    # Crea una lista messages vuota
    messages_1 = []

    # Aggiungi il messaggio dell'utente
    add_user_message(
        messages_1,
        "Generate an AWS EventBridge rule in JSON format that triggers a Lambda when an EC2 instance starts. Include the exact JSON only."
    )

    # Chiama Claude senza stop_sequences
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

    # Crea una nuova lista messages
    messages_2 = []

    # Aggiungi il messaggio dell'utente
    add_user_message(
        messages_2,
        "Generate an AWS EventBridge rule in JSON format that triggers a Lambda when an EC2 instance starts."
    )

    # TRUCCO DEL PREFILL: Aggiungi un messaggio "assistente" pre-riempito
    # Questo fa credere a Claude che ha già iniziato a scrivere ```json
    # Quindi continuerà da lì, senza aggiungere spiegazioni prima
    add_assistant_message(messages_2, "```json")

    # Chiama Claude con stop_sequences=["```"]
    # Questo dice: "Claude, fermati quando raggiungi ``` "
    # Così Claude non scriverà nulla dopo il JSON
    response_2 = chat(messages_2, stop_sequences=["```"])
    raw_response_2 = extract_text(response_2)

    print("\n📋 Risposta Grezza (con prefill):")
    print("```json" + raw_response_2 + "```")

    print("\n✅ VANTAGGIO:")
    print("   - Solo JSON puro (il testo che vedi tra il prefill e lo stop)")
    print("   - Niente testo extra")
    print("   - Facile da parsare")

    # Pulisci il JSON e parsalo
    json_string = raw_response_2.strip()
    try:
        # Prova a parsare come JSON
        parsed_json = json.loads(json_string)
        print("\n✨ JSON Parsato Correttamente:")
        print(json.dumps(parsed_json, indent=2))
        print("\n✅ Questo JSON è PRONTO all'uso! Puoi:")
        print("   - Salvarlo in un database")
        print("   - Inviarlo a un'API")
        print("   - Usarlo direttamente nel tuo codice")
    except json.JSONDecodeError as e:
        print(f"\n❌ Errore parsing JSON: {e}")

    # ===== ESEMPIO 3: LISTA PUNTATA CON LA STESSA TECNICA =====
    print("\n" + "=" * 80)
    print("3️⃣  BONUS - Lista Puntata (Stessa Tecnica)")
    print("=" * 80)

    # Crea una nuova lista messages
    messages_3 = []

    # Aggiungi il messaggio dell'utente
    add_user_message(
        messages_3,
        "Generate a detailed checklist for code review best practices. Format as a bullet list."
    )

    # PREFILL: Inizia con "• " per dire a Claude che deve continuare la lista
    add_assistant_message(messages_3, "• ")

    # STOP: Ferma quando Claude scrive due newline (segno che la lista è finita)
    response_3 = chat(messages_3, stop_sequences=["\n\n"])
    raw_response_3 = extract_text(response_3)

    print("\n📋 Risposta (Lista Puntata):")
    print("• " + raw_response_3)

    print("\n✅ Anche qui:")
    print("   - Prefill: '• ' (inizia la lista)")
    print("   - Stop: '\\n\\n' (ferma dopo la lista)")
    print("   - Output pulito e riutilizzabile")

    print("\n" + "=" * 80)
    print("🎯 CONCLUSIONI")
    print("=" * 80)
    print("""
COME FUNZIONA IL PREFILL + STOP SEQUENCES:

1. PREFILL (add_assistant_message):
   - Fai credere a Claude che ha già iniziato a scrivere
   - Es: "```json" o "• " o "def generate():"
   - Claude continua da lì, senza aggiungere spiegazioni prima

2. STOP SEQUENCES:
   - Dice all'API: "Fermati quando vedi questa stringa"
   - Es: ["```"] per JSON, ["\n\n"] per liste
   - Evita che Claude scriva testo dopo l'output strutturato

RISULTATO: Output PULITO, senza testo extra, pronto per parsare!
""")


# Verifica che il file sia eseguito direttamente
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Demo per imparare la differenza tra usare e NON usare un system prompt.
Confronto: stessa domanda, risposte completamente diverse!
"""

# Importa il modulo os per accedere alle variabili d'ambiente
import os

# Importa la classe Anthropic dal modulo anthropic
# Questa classe permette di comunicare con l'API di Claude
from anthropic import Anthropic

# Crea un'istanza del client Anthropic
# Utilizza automaticamente la variabile d'ambiente ANTHROPIC_API_KEY per autenticarsi
client = Anthropic()

# System prompt del tutor di matematica
# Questo prompt "modella" Claude per comportarsi come un insegnante paziente
# invece che fornire risposte dirette
MATH_TUTOR_SYSTEM = """You are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step."""


# FUNZIONE: chat
# Scopo: Costruisce una chiamata all'API con i parametri corretti
# IMPORTANTE: Il parametro 'system' NON deve essere passato se è None!
# L'API di Anthropic non accetta esplicitamente system=None.
# Se vogliamo omettere il system prompt, semplicemente non lo includiamo nel dizionario.
def chat(messages, system=None):
    """
    Costruisce una chiamata all'API con i parametri corretti.
    """
    # Crea un dizionario con i parametri di base per la richiesta API
    params = {
        "model": "claude-haiku-4-5-20251001",  # Specifica il modello da usare
        "max_tokens": 1024,  # Limita la lunghezza della risposta
        "messages": messages,  # Passa la cronologia della conversazione
    }

    # Aggiungi 'system' ai parametri SOLO se è stato fornito
    # Questo è importante perché vogliamo poter testare il comportamento CON e SENZA system prompt
    if system is not None:
        params["system"] = system

    # Invia la richiesta all'API e restituisce la risposta
    return client.messages.create(**params)


# FUNZIONE: main
# Scopo: Eseguire il demo completo mostrando la differenza tra system prompt e nessun system prompt
def main():
    # Verifica che la chiave API sia disponibile
    # Se non è impostata, il programma non può funzionare
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: La variabile d'ambiente ANTHROPIC_API_KEY non è impostata!")
        print("\nPer eseguire questo script:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...' (inserisci la tua chiave)")
        print("  python3 system_prompt_demo.py")
        print("\nOttieni una chiave API gratuitamente da: https://console.anthropic.com/account/keys")
        exit(1)

    # La domanda che chiediamo a Claude in entrambi i casi
    # Vogliamo vedere come risposte diverse a seconda del system prompt
    student_question = "How do I solve 5x + 2 = 3 for x?"

    # Stampa l'intestazione del demo
    print("=" * 70)
    print("DEMO: System Prompt vs. No System Prompt")
    print("=" * 70)
    print(f"\nDomanda dello studente: {student_question}\n")

    # ===== PRIMA RISPOSTA: SENZA SYSTEM PROMPT =====
    print("-" * 70)
    print("1️⃣  RISPOSTA SENZA SYSTEM PROMPT (Claude agisce normalmente)")
    print("-" * 70)

    # Chiama Claude SENZA un system prompt
    # Claude risponderà con il suo comportamento di default
    response_without_system = chat(
        messages=[{"role": "user", "content": student_question}],
        system=None  # Nessun system prompt
    )

    # Estrae il testo dalla risposta (gestisce i thinking blocks)
    # Cerca il primo blocco che ha l'attributo 'text'
    answer_without = next((block.text for block in response_without_system.content if hasattr(block, 'text')), "")
    print(answer_without)
    print()

    # ===== SECONDA RISPOSTA: CON SYSTEM PROMPT =====
    print("-" * 70)
    print("2️⃣  RISPOSTA CON SYSTEM PROMPT (Tutor di matematica)")
    print("-" * 70)

    # Chiama Claude CON un system prompt
    # Questa volta Claude si comporterà come un tutor paziente
    response_with_system = chat(
        messages=[{"role": "user", "content": student_question}],
        system=MATH_TUTOR_SYSTEM  # Con system prompt del tutor
    )

    # Estrae il testo dalla risposta
    answer_with = next((block.text for block in response_with_system.content if hasattr(block, 'text')), "")
    print(answer_with)
    print()

    # Stampa l'analisi delle differenze
    print("=" * 70)
    print("ANALISI DELLE DIFFERENZE")
    print("=" * 70)
    print("""
OSSERVAZIONI:

1. SENZA SYSTEM PROMPT:
   - Claude fornisce direttamente la risposta finale
   - Spiega il processo matematico
   - Lo studente ottiene la soluzione subito
   - Stile: veloce, diretto, orientato al risultato

2. CON SYSTEM PROMPT:
   - Claude fa domande guida
   - Aiuta lo studente a pensare autonomamente
   - Non svela la risposta, ma guida verso la soluzione
   - Promuove l'apprendimento attivo
   - Stile: pedagogico, interattivo, orientato all'apprendimento

🔑 CONCETTO CHIAVE:
   Lo stesso modello, stessa domanda, stessa API...
   Ma il system prompt cambia COMPLETAMENTE il comportamento e lo stile di risposta!

   Questo dimostra il POTERE dei system prompt nel "modellare" il comportamento dell'IA.
    """)


# Questo controllo verifica se il file viene eseguito direttamente
# "__main__" è il nome speciale dato al file principale quando viene eseguito
if __name__ == "__main__":

    # Chiama la funzione main() per avviare il demo
    main()

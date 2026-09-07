#!/usr/bin/env python3
"""
Demo del parametro Temperature: come Claude cambia comportamento
con temperature diverse (0.0 = deterministica vs 1.0 = creativa)
"""

# Importa il modulo os per accedere alle variabili d'ambiente
import os

# Importa la classe Anthropic per comunicare con l'API di Claude
from anthropic import Anthropic

# Crea un'istanza del client Anthropic
# Usa automaticamente ANTHROPIC_API_KEY dalla variabile d'ambiente
client = Anthropic()

# System prompt per generare idee di film creative
# Questo sistema prompt indica a Claude che deve essere creativo e proporre idee diverse
MOVIE_GENERATOR_SYSTEM = """You are a creative movie pitch generator.
Generate short, unique, and imaginative movie plot ideas. Be creative and diverse in your suggestions."""


# FUNZIONE: chat
# Scopo: inviare un messaggio a Claude con casualità controllabile
# IMPORTANTE: 'top_p' influenza la creatività della risposta
# - top_p=0.1 → sceglie solo dai token più probabili (deterministica)
# - top_p=1.0 → sceglie tra tutti i token probabili (creativa e casuale)
def chat(messages, system=None, top_p=1.0):
    """
    Costruisce e invia una richiesta all'API di Claude.

    Args:
        messages: lista di messaggi della conversazione
        system: system prompt opzionale (solo se passato)
        top_p: controllo della casualità (0.0-1.0, valori bassi = più deterministico)
    """
    # Crea il dizionario dei parametri per la richiesta API
    params = {
        "model": "claude-haiku-4-5-20251001",  # Modello da usare
        "max_tokens": 150,  # Limita la lunghezza della risposta
        "messages": messages,  # Cronologia della conversazione
        "top_p": top_p,  # ← PARAMETRO CHIAVE: controlla la casualità
    }

    # Aggiungi il system prompt SOLO se è stato passato
    # Non includiamo system=None perché l'API non lo accetta
    if system is not None:
        params["system"] = system

    # Invia la richiesta all'API e restituisce la risposta
    return client.messages.create(**params)


# FUNZIONE: extract_text
# Scopo: estrarre il testo dalla risposta di Claude
# (ignora i "thinking blocks" e altri tipi di blocchi)
def extract_text(response):
    """
    Estrae il primo blocco di testo dalla risposta di Claude.
    """
    # Cicla attraverso i blocchi della risposta
    for block in response.content:
        # Se il blocco ha l'attributo 'text', è un blocco di testo
        if hasattr(block, 'text'):
            # Restituisce il testo e esce
            return block.text
    # Se non trova nessun testo, restituisce una stringa vuota
    return ""


# FUNZIONE: main
# Scopo: eseguire il demo con temperature 0.0 e 1.0
def main():
    # Verifica che la chiave API sia disponibile
    # Se non è impostata, il programma non può funzionare
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRORE: ANTHROPIC_API_KEY non è impostata!")
        exit(1)

    # La domanda che faremo a Claude 6 volte (3 volte a temp 0.0, 3 a temp 1.0)
    movie_prompt = "Give me a one-sentence idea for a movie plot."

    # Stampa l'intestazione del demo
    print("=" * 80)
    print("DEMO: Temperature Parameter")
    print("=" * 80)
    print(f"\n📽️  Domanda: {movie_prompt}\n")

    # ===== PARTE 1: TOP_P 0.1 (DETERMINISTICA) =====
    print("=" * 80)
    print("🎯 TOP_P 0.1 (Deterministic - Risposte Identiche)")
    print("=" * 80)
    print("A top_p 0.1, Claude sceglie solo dai token più probabili.")
    print("Le risposte dovrebbero essere identiche o molto simili.\n")

    # Fa 3 chiamate identiche a top_p 0.1
    # Ci aspettiamo risposte uguali o molto simili
    for i in range(1, 4):
        response = chat(
            messages=[{"role": "user", "content": movie_prompt}],
            system=MOVIE_GENERATOR_SYSTEM,
            top_p=0.1  # ← DETERMINISTICA: sceglie solo dai token più probabili
        )
        answer = extract_text(response)
        print(f"📌 Top_P 0.1 - Run {i}:")
        print(f"   {answer}\n")

    # ===== PARTE 2: TOP_P 1.0 (CREATIVA) =====
    print("=" * 80)
    print("🎲 TOP_P 1.0 (Random - Risposte Diverse)")
    print("=" * 80)
    print("A top_p 1.0, Claude campiona tra tutti i token probabili.")
    print("Le risposte dovrebbero essere diverse e creative.\n")

    # Fa 3 chiamate identiche a top_p 1.0
    # Ci aspettiamo risposte diverse grazie alla casualità
    for i in range(1, 4):
        response = chat(
            messages=[{"role": "user", "content": movie_prompt}],
            system=MOVIE_GENERATOR_SYSTEM,
            top_p=1.0  # ← CREATIVA: sceglie tra tutti i token probabili (casuale)
        )
        answer = extract_text(response)
        print(f"🎬 Top_P 1.0 - Run {i}:")
        print(f"   {answer}\n")

    # Stampa l'intestazione finale
    print("=" * 80)


# Verifica che il file sia eseguito direttamente
if __name__ == "__main__":
    main()

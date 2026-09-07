# Accessing Claude with the API

Questo è il primo modulo del corso "Building with the Claude API".

## 📚 Argomenti

- Configurazione della API key
- Creazione di un client Anthropic
- Invio di messaggi a Claude
- Gestione delle risposte
- Conversazioni multiturno

## 🚀 Come usare

1. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

2. Crea un file `.env` con la tua API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

3. Avvia il programma:
```bash
python main.py
```

4. Scrivi i tuoi messaggi e parla con Claude! 💬

## 📝 Cosa fa il programma

- Crea una conversazione interattiva con Claude
- Mantiene lo storico della conversazione
- Gestisce i "thinking blocks" di Claude Sonnet 5
- Permette di uscire scrivendo "exit"

## 🔑 Note importanti

⚠️ **Non condividere mai la tua API key!** Tienila sempre nel file `.env` che non viene pushato su GitHub.


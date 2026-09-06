# Building with the Claude API 🤖

Questo repository contiene tutti i progetti e gli esercizi del corso "Building with the Claude API".

## 📚 Moduli del corso

Tutto il corso si trova in: `building-with-the-claude-api/`

### 1️⃣ [Accessing Claude with the API](./building-with-the-claude-api/01-Accessing-Claude-with-the-API/)
Impara come configurare il client Anthropic, autenticarsi con la API key e creare la tua prima conversazione con Claude.

- ✅ Configurazione API
- ✅ Client setup  
- ✅ Chat interattiva multiturno
- ✅ Gestione delle risposte

### 2️⃣ [System Prompt Demo](./building-with-the-claude-api/system_prompt_demo.py)
Scopri la potenza dei system prompt: stessa domanda, risposte diverse!

---

## 🚀 Quickstart

```bash
# Entra nella cartella del corso
cd building-with-the-claude-api

# Attiva la virtual environment
source venv/bin/activate

# Esegui il demo del system prompt
python3 system_prompt_demo.py

# O esegui il chat interattivo
python3 01-Accessing-Claude-with-the-API/main.py
```

## 🔑 Configurazione

La API key è nel file `.env` (non è versionato su git per sicurezza)

```
ANTHROPIC_API_KEY=sk-ant-...
```

## ⚠️ Sicurezza

- **Mai** condividere la tua API key
- Il file `.env` è già nel `.gitignore`
- Le variabili d'ambiente non verranno mai commitmate

## 📖 Struttura

Leggi [`building-with-the-claude-api/CODING_STRUCTURE.md`](./building-with-the-claude-api/CODING_STRUCTURE.md) per capire la differenza tra:
- **File puliti** (facili da leggere)
- **File spiegati** (con commenti dettagliati)

---

**Happy coding! 🎉**


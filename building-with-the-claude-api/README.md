# Building with the Claude API 🤖

Questo repository contiene tutti i progetti e gli esercizi del corso "Building with the Claude API".

## 📚 Moduli del Corso

Tutti i moduli si trovano nella cartella `Accessing Claude with the API/`

### 1️⃣ Module 01: Accessing Claude with the API
Impara come configurare il client Anthropic, autenticarsi con la API key e creare la tua prima conversazione con Claude.

- ✅ Configurazione API
- ✅ Client setup
- ✅ Chat interattiva multiturno
- ✅ Gestione delle risposte

**Accedi:** `Accessing Claude with the API/01-Accessing-Claude-with-the-API/`

---

### 2️⃣ Module 02: Temperature Parameter
Scopri come il parametro di temperatura/casualità influenza le risposte di Claude.

- ✅ Demo di sampling probabilistico
- ✅ Deterministic (0.1) vs Creative (1.0)
- ✅ Quando usare quale temperatura

**Accedi:** `Accessing Claude with the API/02-Temperature-Parameter/`

---

### 3️⃣ Module 03: Response Streaming
Vedi la differenza tra bloccare tutto e mostrare il testo man mano.

- ✅ Bloccante (4.3s) vs Streaming (0.6s)
- ✅ Time-to-first-byte
- ✅ Miglioramento dell'UX

**Accedi:** `Accessing Claude with the API/03-Response-Streaming/`

---

### 4️⃣ Module 04: Structured Data Prefilling
Genera JSON, CSV e codice pulito senza testo spiegativo.

- ✅ Prefill + Stop Sequences
- ✅ Output strutturato pronto da parsare
- ✅ Integrazione diretta nelle app

**Accedi:** `Accessing Claude with the API/04-Structured-Data-Prefilling/`

---

## 🔑 Configurazione

1. Naviga nella cartella del modulo:
```bash
cd "Accessing Claude with the API/01-Accessing-Claude-with-the-API"
```

2. Crea un file `.env` nella cartella del modulo:
```
ANTHROPIC_API_KEY=your_api_key_here
```

3. Installa le dipendenze (solo una volta):
```bash
pip install -r requirements.txt
```

## ⚠️ Sicurezza

- **Mai** condividere la tua API key
- Usa il file `.env` che è già nel `.gitignore`
- Le variabili d'ambiente non verranno mai commitmate

## 🚀 Come Avviare i Progetti

### Option 1: Dalla cartella del modulo
```bash
cd "Accessing Claude with the API/02-Temperature-Parameter"
python3 temperature_demo.py
```

### Option 2: Dalla root
```bash
cd building-with-the-claude-api
python3 "Accessing Claude with the API/03-Response-Streaming/streaming_demo.py"
```

## 📖 Struttura dei File

Ogni modulo contiene:

- **`module_demo.py`** - Versione pulita (codice leggibile senza commenti)
- **`module_demo_explained.py`** - Versione spiegata (commenti su ogni riga)
- **`README.md`** - Guida del modulo con esempi e casi d'uso

Leggi [CODING_STRUCTURE.md](./CODING_STRUCTURE.md) per approfondire!

---

**Happy coding! 🎉**

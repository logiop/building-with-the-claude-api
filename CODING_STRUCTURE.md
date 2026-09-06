# 📚 Struttura dei File di Codice

In questo progetto, ogni script Python ha **due versioni** per facilitare sia l'apprendimento che la lettura:

## 🎯 Come sono organizzati i file

### **Versione Pulita (Facile da Leggere)**
- **main.py** - Codice senza commenti, facile da leggere e veloce da eseguire
- **system_prompt_demo.py** - Demo del system prompt senza commenti

✅ **Usa questi quando:**
- Vuoi **leggere il codice velocemente**
- Vuoi **eseguire il programma**
- Il codice è **autoesplicativo** grazie ai nomi chiari

### **Versione Spiegata (Con Commenti)**
- **main_explained.py** - Codice con commenti dettagliati su OGNI riga
- **system_prompt_demo_explained.py** - Demo con spiegazioni complete

✅ **Usa questi quando:**
- Stai **imparando** come funziona il codice
- Vuoi capire il **perché** dietro ogni riga
- Sei **nuovo alla programmazione** e hai bisogno di aiuto

---

## 🚀 Come Usare

### **Se vuoi eseguire il programma:**
```bash
# Chat interattivo
python3 main.py

# Demo del system prompt
python3 system_prompt_demo.py
```

### **Se vuoi imparare come funziona:**
```bash
# Apri in un editor e leggi i commenti
cat main_explained.py
cat system_prompt_demo_explained.py
```

---

## 📖 Differenza tra le Due Versioni

### **main.py (24 righe di codice)**
```python
def get_text_content(response):
    for block in response.content:
        if block.type == "text":
            return block.text
    return ""
```

### **main_explained.py (Stessa funzione, con 20 righe di commenti)**
```python
# FUNZIONE: get_text_content
# Scopo: estrarre il testo dalla risposta di Claude
# Perché?: Claude Sonnet 5 può restituire diversi tipi di blocchi (text, thinking, etc.)
# Questa funzione estrae solo il testo, ignorando i "thinking blocks"
def get_text_content(response):
    # response è un oggetto che contiene la risposta di Claude

    # Cicla attraverso ogni blocco (block) nella risposta di Claude
    # response.content è una lista di blocchi che Claude ha inviato
    for block in response.content:

        # Controlla se il tipo di blocco è "text" (testo)
        # Ignora altri tipi come "thinking" (i pensieri interni di Claude)
        if block.type == "text":

            # Restituisce il testo del blocco e esce dalla funzione
            # Usiamo return perché vogliamo il primo blocco di testo trovato
            return block.text

    # Se non trova nessun blocco di tipo "text", restituisce una stringa vuota
    # Questo evita errori se la risposta non contiene testo
    return ""
```

---

## 💡 Flusso di Apprendimento Consigliato

1. **Primo Passo** → Leggi `main_explained.py` per capire la logica
2. **Secondo Passo** → Apri `main.py` in parallelo e capisci come i commenti scompaiono
3. **Terzo Passo** → Esegui `main.py` e interagisci con Claude
4. **Quarto Passo** → Modifica il codice e sperimenta!

---

## 🔄 Mantenersi in Sincronia

⚠️ **Importante:** Se modifichi uno dei file, ricordati di modificare anche l'altro per mantenerli sincronizzati!

Esempio: Se cambi il modello in `main.py` da "claude-sonnet-5" a "claude-haiku-4-5-20251001", fai lo stesso anche in `main_explained.py`.

---

## 📁 Struttura Completa

```
building-with-the-claude-api/
├── system_prompt_demo.py           ← Versione pulita (24 righe)
├── system_prompt_demo_explained.py ← Versione con commenti
├── system_prompt_demo_mock.py      ← Versione mock (senza API)
│
├── 01-Accessing-Claude-with-the-API/
│   ├── main.py                     ← Versione pulita (40 righe)
│   ├── main_explained.py           ← Versione con commenti
│   ├── test_functions.py           ← Test base
│   └── README.md
│
└── CODING_STRUCTURE.md             ← Questo file
```

---

## ✨ Vantaggi di Questa Struttura

✅ **Leggibilità** - Puoi leggere il codice senza distrazioni  
✅ **Apprendimento** - Hai i commenti disponibili quando serve  
✅ **Performance** - Nessun overhead dai commenti durante l'esecuzione  
✅ **Flessibilità** - Scegli la versione che serve al momento  

---

**Happy Learning! 🎓**

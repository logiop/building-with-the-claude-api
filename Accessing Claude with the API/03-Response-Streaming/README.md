# 03 - Response Streaming 📡

Scopri come mostrare le risposte di Claude man mano che arrivano, invece di aspettare tutto in silenzio.

## 🎯 Cosa Imparerai

- **Bloccante:** Aspetti tutto il messaggio prima di vederlo
- **Streaming:** Vedi il testo man mano che Claude lo genera
- Come misurare la differenza di esperienza
- Quando usare quale approccio

## 🚀 Come Usare

### Versione Pulita
```bash
python3 streaming_demo.py
```

### Versione Con Commenti
```bash
python3 streaming_demo_explained.py
```

## 📊 Cosa Vedrai

Il demo farà due richieste identiche:

1. **Versione Bloccante** - Aspetta tutto prima di stampare
2. **Versione Streaming** - Stampa il testo man mano

Noterai la differenza di tempo primo chunk vs tempo totale!

## 🔑 Concetti Chiave

### Bloccante (`client.messages.create()`)
```python
response = client.messages.create(...)
# ⏳ Aspetti qui finché non hai TUTTA la risposta
print(response.content[0].text)
```

**Tempo:** 2-3 secondi prima di vedere qualcosa  
**Uso:** Quando devi elaborare la risposta completa

---

### Streaming (`client.messages.stream()`)
```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)  # Appare subito!
    final_message = stream.get_final_message()
```

**Tempo:** 0.1-0.2 secondi per il primo chunk  
**Uso:** Chatbot, app interattive, UX migliore

---

## 💡 Quando Usare Quale

### Streaming (📡)
✅ Chatbot interattivo  
✅ App web che mostra risposte  
✅ Risposte lunghe (articoli, poesie, codice)  
✅ Quando vuoi "time-to-first-byte" basso  

### Bloccante (⏳)
✅ Script di elaborazione batch  
✅ Quando devi salvare tutto in DB  
✅ API che restituisce JSON  
✅ Risposte corte dove la differenza è minima  

---

## 📌 Eventi dello Streaming

Internamente, lo streaming invia vari eventi:

- `MessageStart` - La risposta inizia
- `ContentBlockStart` - Inizia un blocco (testo, thinking, ecc)
- `ContentBlockDelta` - Chunk di contenuto
- `ContentBlockStop` - Finisce un blocco
- `MessageDelta` - Info su stop reason
- `MessageStop` - Tutto finito

**Ma:** `stream.text_stream` raggruppa tutto e ti dà solo il testo! ✨

---

## 🛠️ Caso d'Uso Reale: Chatbot

```python
# ❌ SBAGLIATO: L'utente aspetta 3 secondi in silenzio
response = client.messages.create(...)
print(response.content[0].text)

# ✅ CORRETTO: L'utente vede il testo apparire
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

La differenza di UX è **enorme**!

---

**Esegui il demo e nota la differenza di tempo!** ⏱️

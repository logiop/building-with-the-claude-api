# 04 - Structured Data con Prefilling + Stop Sequences 📋

Scopri come generare JSON, CSV, liste e codice **pulito** senza testo spiegativo intorno.

## 🎯 Cosa Imparerai

- **Prefill:** Come far credere a Claude che ha già iniziato
- **Stop Sequences:** Come fermare Claude quando hai finito
- Generare JSON pronto da parsare
- Come usare questa tecnica con CSV, liste, codice, ecc.

## 🚀 Come Usare

### Versione Pulita
```bash
python3 structured_data_demo.py
```

### Versione Con Commenti
```bash
python3 structured_data_demo_explained.py
```

## 📊 Cosa Vedrai

Il demo mostra 3 esempi:

1. **Senza trucchi** - JSON sporco (con ```json e testo intorno)
2. **Con prefill + stop** - JSON pulito (pronto da parsare)
3. **Bonus** - Lista puntata (stessa tecnica)

## 🔑 Concetti Chiave

### Il Problema (Senza Prefill)
```python
messages = [{"role": "user", "content": "Generate JSON..."}]
response = client.messages.create(model=..., messages=messages)

# Risposta tipica:
"""
Here's a JSON rule for EventBridge:

```json
{
  "Name": "my-rule",
  ...
}
```

This rule triggers a Lambda function...
"""
# ❌ Testo spiegativo prima e dopo il JSON!
```

---

### La Soluzione (Con Prefill + Stop)
```python
messages = [
    {"role": "user", "content": "Generate JSON..."},
    {"role": "assistant", "content": "```json"}  # ← PREFILL!
]

response = client.messages.create(
    model=...,
    messages=messages,
    stop_sequences=["```"]  # ← STOP!
)

# Risposta:
"""
{
  "Name": "my-rule",
  ...
}
"""
# ✅ Solo JSON puro!
```

---

## 💡 Come Funziona il Prefill

### Senza Prefill
```
Tu:      "Generate JSON..."
Claude:  "Here's the JSON:\n\n```json\n{...}\n```\n\nThis is..."
```

Claude **decide** di aggiungere spiegazioni.

---

### Con Prefill
```
Tu:       "Generate JSON..."
Tu (finto): "```json"  ← Facciamo credere che Claude ha già scritto questo
Claude:   "{...}"      ← Claude continua da lì!
```

Claude **crede** di aver già iniziato, quindi continua dal prefill!

---

## 🛑 Perché Serve Stop Sequences

### Senza Stop Sequences
```python
response = client.messages.create(
    model=...,
    messages=messages,
    stop_sequences=["```"]  # ← Commentiamo questa riga
)

# Claude genera:
"""
{
  "Name": "my-rule",
  ...
}
```

This rule is useful for serverless applications...
"""
# ❌ Continua a scrivere testo dopo il JSON!
```

### Con Stop Sequences
```python
response = client.messages.create(
    model=...,
    messages=messages,
    stop_sequences=["```"]  # ← QUESTA RIGA È FONDAMENTALE!
)

# Claude genera:
"""
{
  "Name": "my-rule",
  ...
}
"""
# ✅ Si ferma quando vede ``` (che abbiamo aggiunto dopo il JSON nel prefill)
```

---

## 📝 Tecniche per Diversi Formati

### JSON
```python
add_assistant_message(messages, "```json")
response = chat(messages, stop_sequences=["```"])
```

### CSV
```python
add_assistant_message(messages, "name,age,city\n")
response = chat(messages, stop_sequences=["\n\n"])
```

### Lista Puntata
```python
add_assistant_message(messages, "• ")
response = chat(messages, stop_sequences=["\n\n"])
```

### Codice Python
```python
add_assistant_message(messages, "```python\n")
response = chat(messages, stop_sequences=["```"])
```

### XML
```python
add_assistant_message(messages, "<root>")
response = chat(messages, stop_sequences=["</root>"])
```

---

## 🛠️ Casi d'Uso Reali

### 1️⃣ Tool che Genera Config Files
```python
# Genera config.json automatico
prompt = "Generate a Kubernetes deployment config for a Node.js app"
add_assistant_message(messages, "```yaml")
response = chat(messages, stop_sequences=["```"])

# Salva direttamente:
with open("deployment.yaml", "w") as f:
    f.write(response_text)
```

### 2️⃣ API che Ritorna JSON Pulito
```python
@app.post("/generate-schema")
def generate_schema():
    prompt = f"Generate JSON schema for user model"
    messages = [{"role": "user", "content": prompt}]
    add_assistant_message(messages, "```json")
    
    response = chat(messages, stop_sequences=["```"])
    schema = json.loads(response_text)
    
    return {"schema": schema}  # JSON pronto!
```

### 3️⃣ Script che Estrae Dati in CSV
```python
# Estrai dati da PDF e genera CSV
prompt = "Extract names and emails from this PDF. Format as CSV."
add_assistant_message(messages, "name,email\n")
response = chat(messages, stop_sequences=["\n\n"])

# Scrivi su file:
import csv
reader = csv.reader(response_text.split("\n"))
for row in reader:
    save_to_database(row)
```

### 4️⃣ CLI Tool che Genera Codice
```python
# Genera uno snippet Python
prompt = f"Write a Python function to {user_request}"
add_assistant_message(messages, "```python\n")
response = chat(messages, stop_sequences=["```"])

print("Here's your code:")
print(response_text)
```

---

## 📊 Confronto: Con e Senza Prefill

| Aspetto | Senza Prefill | Con Prefill |
|---------|---------------|------------|
| **Output** | Sporca (testo + JSON) | Pulita (solo JSON) |
| **Parsing** | Devi estrarre il JSON dal testo | `json.loads(response)` diretto |
| **Complessità** | Semplice richiesta | Una riga extra di prefill |
| **Affidabilità** | Claude potrebbe dimenticare il JSON | Quasi garantito |
| **Integrabilità** | Devi pulire l'output | Pronto all'uso |

---

## ✨ Riassunto

```python
# PRIMA (❌ Output sporco):
response = client.messages.create(model=..., messages=messages)
# Ottieni: "Here's the JSON:\n\n```json\n{...}\n```"

# DOPO (✅ Output pulito):
messages.append({"role": "assistant", "content": "```json"})
response = client.messages.create(
    model=...,
    messages=messages,
    stop_sequences=["```"]
)
# Ottieni: "{...}"  (solo JSON puro!)
```

**Differenza?** 2 righe di codice, ma l'output è completamente diverso! 🚀

---

**Esegui il demo e vedi la differenza con i tuoi occhi!**

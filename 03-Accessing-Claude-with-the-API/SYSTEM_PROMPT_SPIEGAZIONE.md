# System Prompt: Spiegazione Semplice 🎓

## 🎯 Che cosa è un System Prompt?

Un **system prompt** è come un "ruolo" o una "personalità" che dai a Claude prima che risponda alle domande dell'utente.

Immagina di avere un amico che può essere:
- Un matematico che risolve i problemi direttamente
- Un insegnante che ti guida a pensare da solo
- Un medico che dà consigli
- Un poeta che scrive versi

**Lo stesso amico (Claude), con ruoli diversi, risponde in modi completamente diversi!**

---

## 📌 La Differenza Tra "System" e "Messages" nell'API

### Struttura della Chiamata API:

```
client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    system="...",          # ← SISTEMA (il ruolo/personalità)
    messages=[{            # ← CONVERSAZIONE (le domande/risposte)
        "role": "user",
        "content": "How do I solve 5x + 2 = 3?"
    }]
)
```

### Cosa è "System"?
- **Livello più alto**: Imposta il contesto GLOBALE
- **Vale per tutta la conversazione**: Influenza tutte le risposte
- **Opzionale**: Se non lo metti, Claude usa il suo comportamento di default
- **Non cambia con i turni**: Rimane uguale per tutti i messaggi

### Cosa sono "Messages"?
- **Livello di conversazione**: La storia della chat
- **Turni di dialogo**: Domande dell'utente e risposte di Claude
- **Memoria della conversazione**: Claude ricorda i turni precedenti
- **Obbligatorio**: Deve esserci almeno un messaggio

### Analogia:
- **System** = La trama di un film (impostata all'inizio)
- **Messages** = I dialoghi tra i personaggi (cambiano ogni scena)

---

## 🔑 Il Concetto Chiave Spiegato Semplicemente

### Scenario 1: SENZA System Prompt

**Domanda:** "How do I solve 5x + 2 = 3 for x?"

**Risposta di Claude (comportamento di default):**
```
The solution is:
5x + 2 = 3
5x = 1
x = 1/5 = 0.2
```

Claude risponde **direttamente**, fornendo la soluzione completa. È utile e veloce.

---

### Scenario 2: CON System Prompt

**System Prompt:** "You are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step."

**Stessa Domanda:** "How do I solve 5x + 2 = 3 for x?"

**Risposta di Claude (come tutor di matematica):**
```
Great question! Let's work through this step by step.

First, I want you to think about what we're trying to do. 
We have the equation: 5x + 2 = 3

Here's my first question for you: What do you think we should 
do first to isolate the terms with 'x'?
```

Claude risponde **in modo pedagogico**, guida lo studente. È lento ma efficace per l'apprendimento.

---

## 🤔 Perché il System Prompt Cambia Così Tanto il Comportamento?

### 1. **Definisce il contesto**
Il system prompt dice a Claude: "Non sei un risolutore di problemi, sei un insegnante"

### 2. **Crea vincoli** 
Il system prompt impone regole: "Non dare risposte dirette" / "Guida step by step"

### 3. **Modella lo stile di comunicazione**
Il system prompt cambia come Claude comunica:
- Con tutor: Domande, hint, pazienza
- Con diritto: Formale, legale, preciso
- Con amico: Informale, scherzoso, empatico

### 4. **Non cambia le capacità, cambia l'atteggiamento**
Claude sa risolvere matematica in entrambi i casi. Ma il system prompt decide *come* usare quella conoscenza.

---

## 💡 Quando Conviene Rendere il System Prompt Opzionale?

### ✅ Sistema Prompt Opzionale: BUONissimo

```python
def chat(messages, system=None):
    params = {
        "model": "claude-opus-5",
        "max_tokens": 1024,
        "messages": messages,
    }
    if system is not None:
        params["system"] = system
    return client.messages.create(**params)
```

**Vantaggi:**
- Puoi usare la funzione CON o SENZA system prompt
- Flessibilità: uno scenario richiede un tutor, un altro richiede un esperto diretto
- Riutilizzabilità: una funzione per tutti i casi
- Facile testare il comportamento di default

---

### ✅ Sistema Prompt Hardcodato: BONissimo in alcuni casi

```python
def math_tutor(messages):
    params = {
        "model": "claude-opus-5",
        "max_tokens": 1024,
        "messages": messages,
        "system": "You are a patient math tutor..."  # ← Hardcodato
    }
    return client.messages.create(**params)
```

**Vantaggi:**
- Specializzazione: sai sempre che avrai il comportamento del tutor
- Semplicità: meno parametri da preoccuparsi
- Coerenza: il system prompt non cambia mai

**Quando usarlo:**
- Quando il ruolo è SEMPRE uguale (es: "assistente legale")
- Quando non hai motivo di cambiar il system prompt
- Quando vuoi semplificare l'interfaccia

---

## 📊 Tabella di Riepilogo

| Aspetto | System Prompt | Messages |
|---------|---------------|----------|
| **Livello** | Context globale | Conversazione |
| **Obbligatorio?** | No (opzionale) | Sì (almeno uno) |
| **Quando impostarlo** | All'inizio della sessione | Ad ogni turno di conversazione |
| **Cambia il contenuto** | Cambia lo STILE | Cambia l'argomento |
| **Numero** | Uno solo per sessione | Molti (history di chat) |
| **API Parameter** | `system="..."` | `messages=[{...}]` |

---

## 🚀 Caso d'Uso Pratico

### Funzione Flessibile (Consigliato per App Reali):

```python
def chat_with_role(messages, role="default"):
    """Parla con Claude in un ruolo specifico."""
    
    roles = {
        "tutor": "You are a patient math tutor. Guide step by step.",
        "expert": "You are an expert. Give direct, precise answers.",
        "friend": "You are a helpful friend. Be casual and warm.",
    }
    
    params = {
        "model": "claude-opus-5",
        "max_tokens": 1024,
        "messages": messages,
    }
    
    if role in roles:
        params["system"] = roles[role]
    
    return client.messages.create(**params)

# Uso:
chat_with_role([{"role": "user", "content": "How do I solve 5x + 2 = 3?"}], 
               role="tutor")  # Risposta guidata

chat_with_role([{"role": "user", "content": "How do I solve 5x + 2 = 3?"}], 
               role="expert")  # Risposta diretta
```

---

## 🎓 Il Concetto Finale (Semplicissimo)

**System Prompt = Come Claude si comporta**  
**Messages = Di cosa parla Claude**

Se cambi il system prompt, la stessa domanda ha risposte diverse.  
Se cambi i messages, Claude cambia argomento ma con lo stesso stile.

> 💭 "Un system prompt senza messages è come un attore senza copione.  
> Messages senza system prompt è come un copione senza personaggio."

---

## 🔗 Risorse per Approfondire

- [Anthropic API Documentation](https://docs.anthropic.com)
- [System Prompt Best Practices](https://docs.anthropic.com/guides/system-prompts)
- Prova tu stesso! Cambia il system prompt e vedi come cambia la risposta.


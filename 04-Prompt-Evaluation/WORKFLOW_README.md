# 05b - 5-Step Prompt Evaluation Workflow 🔄

Implementa il workflow completo di prompt evaluation: draft → dataset → run → grade → iterate

## 🎯 I 5 Step della Pipeline

```
1. DRAFT      2. DATASET     3. RUN         4. GRADE       5. ITERATE
┌─────────┐  ┌──────────┐   ┌────────┐    ┌─────────┐    ┌──────────┐
│Prompt   │→ │Questions │→  │Claude  │→   │Claude   │→   │Compare & │
│V1 vs V2 │  │Test Set  │   │Answers │   │Grader   │   │Improve   │
└─────────┘  └──────────┘   └────────┘    └─────────┘    └──────────┘
                                          (1-10 score)
```

## 🚀 Come Usare

### Versione Pulita
```bash
python3 eval_workflow_demo.py
```

### Versione Con Commenti
```bash
python3 eval_workflow_demo_explained.py
```

## 📊 Cosa Succede Step by Step

### **STEP 1: Draft Prompts**
Scrivi 2+ versioni di prompt da testare:
```python
PROMPT_V1 = "Please answer the user's question: {question}"

PROMPT_V2 = """Please answer the user's question with ample detail and clarity.
Provide thorough explanations and relevant context where applicable.
Question: {question}"""
```

---

### **STEP 2: Define Dataset**
Crea domande rappresentative che testano diverse abilità:
```python
EVAL_QUESTIONS = [
    "What's 2+2?",                          # Simple math
    "How do I make oatmeal?",               # Instructions
    "How far away is the Moon?",            # Facts
    "What are the benefits of exercise?",   # Complex topic
    "Explain photosynthesis briefly.",      # Science
]
```

---

### **STEP 3: Run Prompts**
Esegui ogni versione del prompt su tutte le domande:
```python
def run_prompt(prompt_template, questions):
    responses = []
    for question in questions:
        # Interpolate template: "Please answer: What's 2+2?"
        prompt = prompt_template.format(question=question)
        
        # Call Claude
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            messages=[{"role": "user", "content": prompt}]
        )
        responses.append(response)
    return responses
```

---

### **STEP 4: Grade Responses**
Usa Claude come "giudice" per valutare le risposte 1-10:
```python
def grade_response(question, answer):
    # Seconda chiamata a Claude
    grading_prompt = f"""Question: {question}
Response: {answer}
Grade this response (1-10 only):"""
    
    # Claude valuta la risposta
    score = client.messages.create(
        system=GRADER_SYSTEM,  # Istruzioni per il giudice
        messages=[{"role": "user", "content": grading_prompt}]
    )
    return score  # Integer 1-10
```

**IMPORTANTE:** Questo è il cuore della pipeline!
- Niente opinioni soggettive
- Valutazione oggettiva e misurabile
- Ripetibile e tracciabile

---

### **STEP 5: Iterate**
Confronta i risultati e migliora il prompt vincente:
```python
v1_score = evaluate_prompt("V1", PROMPT_V1, questions)  # 7.4/10
v2_score = evaluate_prompt("V2", PROMPT_V2, questions)  # 7.4/10

if v2_score > v1_score:
    # Iterare su V2
    # Aggiungi istruzioni nuove
    # Rirun la pipeline
    # Vedi se score sale
```

## 📈 Output Reale del Demo

```
PROMPT V1 (Simple): 7.4/10
Q1: "What's 2+2?" → 1/10 (⚠️ Grader ha bias!)
Q2: "How do I make oatmeal?" → 9/10
Q3: "How far away is the Moon?" → 9/10
Q4: "What are the benefits of exercise?" → 9/10
Q5: "Explain photosynthesis briefly." → 9/10

PROMPT V2 (Detailed): 7.4/10
Q1: "What's 2+2?" → 1/10
Q2-Q5: 9/10 ciascuno

WINNER: TIE (entrambi 7.4/10)
```

## 🔍 Perché Usare un Grader Automatico?

### ❌ Senza Grader (Testing "A Occhio")
```
Tu leggi le risposte...
"Sì, entrambi sembrano buoni"
Non sai quale è VERAMENTE migliore
Non hai metriche per iterare
```

### ✅ Con Grader Automatico
```
Valuta OGNI risposta 1-10
Calcola medie matematiche
Vedi esattamente dove ogni prompt fallisce
Iterazione basata su DATI, non su intuito
```

## ⚠️ Limiti del Grader (Claude stesso)

| Limite | Impatto |
|--------|---------|
| **Bias verso risposte lunghe** | Potrebbe favorire verbose |
| **Costo doppio** | 2 chiamate per domanda |
| **Soggettività** | Claude giudica come Claude, non come esperto |
| **Variabilità** | Punteggi potrebbero variare tra richieste |

## 🛠️ Quando Usare Grader Diversi

| Grader | Use Case |
|--------|----------|
| **Claude** | Valutazioni generiche, budget generoso |
| **Regex + Metriche** | Risposte strutturate/esatte (JSON, date) |
| **Esperti umani** | Dominio critico (medicina, legale) |
| **Rubriche rigide** | Criteri numerici chiari ("lunghezza min", "parole chiave") |

## 💡 Adattare Questo ai Tuoi Progetti

### Esempio 1: Classificatore di Ospiti
```python
EVAL_DATASET = [
    {"guest_info": "50 bookings, 5-star avg", "expected": "VIP"},
    {"guest_info": "1 booking, cancelled", "expected": "At-Risk"},
    # ... 18+ altri casi ...
]

GRADER_SYSTEM = """Valuta se la classe è corretta.
Rules: VIP (30+ bookings), At-Risk (>50% cancellati), Regular (else).
Score 1-10."""

# Run pipeline
score_v1 = evaluate_prompt("v1", prompt_v1, EVAL_DATASET)
score_v2 = evaluate_prompt("v2", prompt_v2, EVAL_DATASET)

# Itera finché score >= 95%
```

### Esempio 2: Estrazione Strutturata
```python
EVAL_DATASET = [
    {
        "email": "Book 5 people, Sept 15",
        "expected": {"guests": 5, "date": "2026-09-15"}
    },
    # ... altri 14+ casi ...
]

GRADER_SYSTEM = """Valuta se l'estrazione è corretta.
Check: guest count (numero), date (YYYY-MM-DD), special requests.
Score 1-10 based on accuracy."""

# Loop fino a accuracy >= 95%
while accuracy < 95:
    score = evaluate_prompt("current", prompt, EVAL_DATASET)
    if score >= 95:
        break
    # Migliora il prompt
    prompt = improve_prompt(prompt)
```

## 🎯 Il Workflow di Iterazione Completo

```
1. Scrivi Prompt V1
     ↓
2. Esegui eval pipeline
     ↓
3. Score: 70%
     ↓
4. Vedi dove fallisce (Q1, Q3, Q5)
     ↓
5. Migliora il prompt (aggiungi istruzioni)
     ↓
6. Scrivi Prompt V2
     ↓
7. Esegui eval pipeline NUOVAMENTE
     ↓
8. Score: 85% (Migliorato!)
     ↓
9. Continua iterando finché score >= 95%
     ↓
10. DEPLOY con fiducia
```

## 📌 Riassunto

| Aspetto | "A Occhio" | Eval Pipeline |
|---------|-----------|---------------|
| **Obiettività** | Soggettivo | Numerico |
| **Tracciabilità** | Niente | Storico di scores |
| **Iterazione** | Guesswork | Data-driven |
| **Fiducia** | Falsa | Reale |
| **Time to Deploy** | Veloce ma rischioso | Più lento ma sicuro |

**Il tempo in più vale la pena:** Scopri i problemi PRIMA della produzione, non dopo!

---

**Esegui il demo e osserva come la pipeline misura il miglioramento del prompt!** 🚀

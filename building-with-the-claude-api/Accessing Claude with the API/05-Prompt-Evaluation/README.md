# 05 - Prompt Evaluation 📋

Scopri come valutare i prompt in modo OGGETTIVO invece di testarli "a occhio".

## 🎯 Cosa Imparerai

- **Il Problema:** Testare prompt solo su 2-3 esempi ti dà falsa sicurezza
- **La Soluzione:** Evaluation pipeline con dataset di test automatizzati
- **Il Valore:** Sapere ESATTAMENTE dove il prompt fallisce
- **L'Iterazione:** Misurare il miglioramento quando modifichi il prompt

## 🚀 Come Usare

### Versione Pulita
```bash
python3 eval_demo.py
```

### Versione Con Commenti
```bash
python3 eval_demo_explained.py
```

## 📊 Cosa Vedrai

Il demo esegue 10 test case su un classificatore di sentimento e stampa:

1. **Accuratezza totale** - Quanti test passano
2. **Test falliti** - Quali casi il prompt non riesce a classificare
3. **Insights** - Dove il prompt è debole (es. sarcasmo, sentimenti misti)

## 🔑 Concetti Chiave

### ❌ Testing "A Occhio" (Sbagliato)

```python
# Testo il prompt su 2-3 esempi
print("Prova 1: 'I love this!' →", claude("I love this!"))
# Output: "positive" ✅

print("Prova 2: 'Terrible product' →", claude("Terrible product"))
# Output: "negative" ✅

# Penso: "Funziona! Sono pronto per produzione!"
```

**Problema:** 2 test passati ≠ il prompt funziona bene. Scopri il problema solo quando lo usi in produzione con 1000 recensioni!

---

### ✅ Evaluation Oggettiva (Corretto)

```python
# Crei 10+ test case diversificati (inclusi casi limite)
test_cases = [
    {"input": "Amazing!", "expected": "positive"},
    {"input": "Terrible", "expected": "negative"},
    {"input": "It's okay I guess", "expected": "neutral"},
    # ... altri casi difficili ...
]

# Esegui automaticamente su TUTTI
accuracy = run_eval(prompt, test_cases)
print(f"Accuracy: {accuracy:.0f}%")

# Vedi i test falliti:
# Test 9 failed: "Oh wow, AMAZING quality... said no one ever"
#   Expected: negative
#   Got: positive
#   → Il prompt non capisce il sarcasmo!
```

**Vantaggio:** Sai ESATTAMENTE cosa migliorare!

---

## 📈 Quando Usare Quale Approccio

| Scenario | Testing A Occhio | Evaluation Obj. |
|----------|-----------------|-----------------|
| **Sviluppo iniziale** | ✅ Va bene | ❌ Overkill |
| **Prima release** | ❌ Rischiato | ✅ Essenziale |
| **Iterazione** | ❌ Non sai il progresso | ✅ Misuri i miglioramenti |
| **Produzione** | ❌ Scopri bug tardi | ✅ Niente sorprese |
| **Cambio del prompt** | ❌ Rompi senza saperlo | ✅ Vedi subito se degrada |

---

## 💡 Come Usare Questo Schema nei Tuoi Progetti

### Scenario 1: Classificatore di Ospiti

Se stai creando un tool che classifica ospiti come "VIP", "Regular", "At-Risk":

```python
test_cases = [
    {"input": "Ospite con 50 prenotazioni precedenti", "expected": "VIP"},
    {"input": "Ospite con 1 prenotazione", "expected": "Regular"},
    {"input": "Ospite che ha cancellato 5 volte", "expected": "At-Risk"},
    # ... altri 20+ casi ...
]

accuracy = run_eval(classification_prompt, test_cases)

# Se accuracy < 90%, non mettere in produzione!
# Modifica il prompt, rirun, vedi se migliora
```

---

### Scenario 2: Estrazione di Informazioni

Se stai creando un agent che estrae dati da email:

```python
test_cases = [
    {
        "input": "Email da Giorgio: 'Voglio prenotare per 5 persone il 15 settembre'",
        "expected": {
            "guest_count": 5,
            "date": "2026-09-15",
            ...
        }
    },
    # ... altri 15+ casi ...
]

accuracy = run_eval(extraction_prompt, test_cases)

# Scopri che il prompt sbaglia le date quando sono in formato "15 settembre"
# Migliora il prompt, rirun, vedi il miglioramento
```

---

## 🔧 Cosa Manca (Per Una "Vera" Eval Pipeline)

Questa mini-pipeline è semplicissima, ma una "vera" production eval pipeline include:

1. **Metriche avanzate** - Non solo accuracy, ma anche:
   - Precision / Recall / F1-score
   - Confusion matrix
   - Per-category accuracy

2. **Dataset stratificato** - Test case raggruppati per categoria:
   - X test facili
   - Y test medio-difficili
   - Z test casi limite

3. **Versioning** - Tenere traccia:
   - Quale prompt ottiene quale accuracy
   - Come è cambiato nel tempo
   - Quando è peggiorato

4. **Regression testing** - Quando aggiorni il prompt:
   - Assicurati di non rompere i test vecchi
   - Misura il miglioramento sui nuovi

5. **Golden dataset** - Un dataset "ufficiale" per:
   - Confrontare versioni di prompt
   - Decidere quando rilasciare

6. **A/B testing** - In produzione:
   - Testa due prompt su utenti reali
   - Vedi quale perfoma meglio
   - Migra gradualmente

---

## 📌 Riassunto

| Aspetto | "A Occhio" | Evaluation Obj. |
|---------|-----------|-----------------|
| **Tempo di setup** | 2 minuti | 30 minuti |
| **Fiducia nel prompt** | Falsa (90%) | Reale (basata su dati) |
| **Scoperta di bug** | In produzione | Prima di mettere live |
| **Iterazione** | Guesswork | Data-driven |
| **Rischio** | **ALTISSIMO** | Basso |

**Investire 30 minuti in evaluation ti salva ore di debug in produzione!** 🚀

---

**Esegui il demo e vedi dove il tuo prompt fallisce!**

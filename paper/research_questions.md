# Research Questions

## RQ1: Model Performance
**Can LLMs accurately classify logical errors in student code?**

Metrics:
- Success rate per model (valid category predictions)
- Error rate (parse failures, invalid responses)
- Distribution of predicted categories

Expected: Closed-source models (GPT-4o, Claude) > Open-source (Llama, Qwen)

---

## RQ2: Inter-Model Agreement
**Do different LLMs agree on error classifications?**

Metrics:
- Pairwise agreement rates
- Full agreement (all 6 models)
- Open-source vs Closed-source agreement

Expected: High agreement (>70%) for simple errors, low for complex

---

## RQ3: Error Category Difficulty
**Which error categories are hardest to classify consistently?**

Metrics:
- Agreement rate per category
- Confusion patterns (which categories get mixed up)
- Model-specific biases

Expected: STMT_INTEGRITY most common, DATA_TYPE/COMPUTATION hardest

---

## RQ4: Need for Human Validation
**Where do models most disagree, requiring human ground truth?**

Metrics:
- Conflict cases (0-1 agreement)
- Ambiguous cases (2-3 models agree)
- Consensus cases (5-6 models agree)

Expected: 20-30% need human review

---

## Hypotheses

**H1**: Closed-source models will have higher success rates (>85%) than open-source (<75%)

**H2**: Smaller models (Llama 3B) will show bias toward common categories (STMT_INTEGRITY)

**H3**: Inter-model agreement will be high (>75%) overall but vary by category

**H4**: At least 25% of samples will lack full consensus, requiring human validation

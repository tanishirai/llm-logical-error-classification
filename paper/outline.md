# Logical Error Classification Using Multiple LLMs

## Abstract (150 words)
- Problem: Logical errors hard to classify
- Method: Compare 6 LLMs (3 open, 3 closed-source)
- Dataset: 200 samples from 5 datasets
- Results: X% agreement, Y conflicts
- Conclusion: Need human validation

## 1. Introduction
- Program errors: syntax vs logical
- Challenge: No compiler feedback for logical errors
- Research question: Can LLMs classify logical errors?
- Contribution: Systematic comparison of 6 models

## 2. Related Work
- [Your paper reference]: 7 error categories
- DrRepair, DeepFix (syntax errors)
- Gap: Limited work on logical error classification

## 3. Methodology
### 3.1 Error Taxonomy
- 7 categories (Table 1 from paper)
- LOOP_COND, COND_BRANCH, etc.

### 3.2 Dataset
- 5 sources: PyPal, Yaksh, Codeforces, SPOC, DeepFix
- Total: 148,746 records
- Selected: 200 diverse samples

### 3.3 Models Tested
**Automated (API):**
- Qwen 2.5 Coder 7B (Alibaba)
- Llama 3.2 3B (Meta)

**Manual (Web Interface):**
- Gemini 2.5 Flash (Google)
- GPT-4o (OpenAI)
- Claude Sonnet 4.5 (Anthropic)
- DeepSeek R1 (DeepSeek)

### 3.4 Evaluation Process
- Phase 1: Automated predictions (200 samples)
- Phase 2: Manual testing (same 200)
- Phase 3: Agreement analysis

## 4. Results
### 4.1 Model Performance
- Success rates per model
- Common predictions
- Failure modes

### 4.2 Agreement Analysis
- Inter-model agreement
- Open vs Closed source comparison
- Conflict patterns

### 4.3 Error Category Distribution
- Most common: STMT_INTEGRITY, COND_BRANCH
- Hardest to classify: ...

## 5. Discussion
- Why models disagree
- Llama bias toward STMT_INTEGRITY
- Need for human ground truth

## 6. Conclusion
- LLMs can classify but disagree
- Human validation essential
- Future work: Fine-tuning on validated data

## References

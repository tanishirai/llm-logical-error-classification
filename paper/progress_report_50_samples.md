# LLM Logical Error Classification Study
## Progress Report: First 50 Samples

**Date:** December 31, 2024  
**Institution:** FOSSEE, IIT Bombay  
**Completion:** 25% (50/200 samples)

---

## 1. Executive Summary

We have completed manual testing of 50 diverse code samples across 4 state-of-the-art LLMs, comparing them against automated predictions from Qwen 2.5 Coder 7B. Early results show interesting agreement patterns and highlight challenges with automated API-based predictions.

---

## 2. Study Design

### 2.1 Dataset
- **Total unified dataset:** 148,746 buggy code samples
- **Test sample:** 200 carefully selected samples (stratified by language and error type)
- **Completed:** 50 samples (25%)

### 2.2 Models Evaluated

| Model | Access Method | Size/Type | Status |
|-------|--------------|-----------|--------|
| Qwen 2.5 Coder 7B | API (Automated) | 7B params | ✅ Complete |
| Gemini 2.5 Flash | Web (Manual) | Large | ✅ 50 samples |
| ChatGPT (GPT-4o) | Web (Manual) | Large | ✅ 50 samples |
| Claude Sonnet 4.5 | Web (Manual) | Large | ✅ 50 samples |
| DeepSeek R1 | Web (Manual) | Large | ✅ 50 samples |

**Note:** Initially included Llama 3.2 3B but excluded due to severe bias (79% predictions in single category STMT_INTEGRITY).

### 2.3 Error Taxonomy (7 Categories)

1. **LOOP_COND** - Incorrect loop condition
2. **COND_BRANCH** - Wrong if/else condition
3. **STMT_INTEGRITY** - Missing or incorrect statement
4. **IO_FORMAT** - Input/output format issues
5. **VAR_INIT** - Variable initialization errors
6. **DATA_TYPE** - Data type mismatches
7. **COMPUTATION** - Calculation/arithmetic errors

---

## 3. Current Findings (50 Samples)

### 3.1 API Reliability

**Qwen 2.5 Coder (Automated):**
- Valid predictions: ~38/50 (76%)
- Error cases: ~12/50 (24%)
- Errors due to: API timeouts, rate limiting, parsing failures

**Insight:** Automated predictions face reliability challenges that manual testing avoids.

### 3.2 Preliminary Agreement Patterns (Manual Models)

**High Agreement Examples:**
- Sample #2 (PYPAL_006556): All 4 models → LOOP_COND ✅
- Sample #4, #5, #14, #30, #31: All 4 models → STMT_INTEGRITY ✅

**Low Agreement Examples:**
- Sample #3 (YAK_096363): COMPUTATION (2), STMT_INTEGRITY (2) - 50% split
- Sample #6 (YAK_044300): COMPUTATION (3), IO_FORMAT (1) - diverse
- Sample #7 (YAK_029788): 4 different predictions! (COMPUTATION x2, DATA_TYPE, COND_BRANCH)

**Initial Observation:** Models show strong agreement on structural issues (loops, statements) but diverge on computational/logic errors.

### 3.3 Dataset Distribution (50 samples)

| Dataset | Count | Languages |
|---------|-------|-----------|
| Yaksh | 26 | Python |
| Codeforces | 10 | C++ |
| SPOC | 4 | C++ |
| PyPal | 7 | Python |
| DeepFix | 3 | C |


---

## 4. Challenges & Solutions

### 4.1 Challenge: API Reliability
- **Issue:** Qwen API shows 24% error rate
- **Solution:** Documented as finding; demonstrates automated vs manual trade-offs

### 4.2 Challenge: Model Bias
- **Issue:** Llama 3.2 3B showed 79% bias toward STMT_INTEGRITY
- **Solution:** Excluded from study; documented as size vs quality lesson

### 4.3 Challenge: Time Intensity
- **Issue:** Manual testing ~1.5 min per sample × 4 models = 200+ minutes total
- **Solution:** Parallel submission workflow; keyboard shortcuts; split sessions

---

## 5. Repository & Code

**GitHub:** https://github.com/tanishirai/llm-logical-error-classification

**Key Scripts:**
- `combine_datasets.py` - Unified 5 datasets
- `dataset_statistics.py` - Comprehensive dataset analysis
- `create_sample.py` - Stratified sampling (200 samples)
- `run_predictions_200.py` - Automated Qwen predictions
- `prepare_manual_testing.py` - Generated testing prompts

**Documentation:**
- README.md - Project overview
- data/README.md - Dataset documentation
- paper/*.md - Paper sections in progress

---

## 6. Preliminary Insights

### 6.1 Category Distribution (Qwen predictions, 50 samples)
- STMT_INTEGRITY: ~40% (most common)
- LOOP_COND: ~15%
- COND_BRANCH: ~12%
- COMPUTATION: ~10%
- Others: ~23%

### 6.2 Inter-Model Agreement (Observations)
- **Perfect agreement (all 4 match):** ~30% of samples
- **Majority agreement (3/4 match):** ~35% of samples
- **Split decision (2-2):** ~15% of samples
- **No agreement (all different):** ~5% of samples

*(Formal metrics to be calculated after 200 samples)*

---

## 7. Expected Contributions

1. **Comprehensive Benchmark:** First systematic comparison of 6 LLMs on logical error classification
2. **Real-World Dataset:** 148K samples from 5 diverse sources (academic + competitive)
3. **Automated vs Manual Insights:** API reliability vs accuracy trade-offs
4. **Error Taxonomy Validation:** Testing 7-category classification scheme
5. **Open Resources:** Dataset, code, and results publicly available

---

## 8. Conclusion

After 50 samples, we observe that:
1. Manual testing is more reliable but time-intensive
2. Models agree strongly on structural errors (loops, statements)
3. Computational/logic errors show more disagreement
4. Automated predictions face API reliability challenges

**Next milestone:** Complete 100 samples by January 3, 2025.

---

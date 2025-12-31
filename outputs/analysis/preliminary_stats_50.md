# Preliminary Statistics: First 50 Samples

## Sample Distribution

### By Dataset
- Yaksh (Python): 26 samples (52%)
- Codeforces (C++): 10 samples (20%)
- PyPal (Python): 7 samples (14%)
- SPOC (C++): 4 samples (8%)
- DeepFix (C): 3 samples (6%)

### By Language
- Python: 33 samples (66%)
- C++: 14 samples (28%)
- C: 3 samples (6%)

## Qwen Automated Predictions

### Validity
- Valid predictions: ~38/50 (76%)
- ERROR cases: ~12/50 (24%)

### Category Distribution (Valid only)
- STMT_INTEGRITY: ~15 (39%)
- COND_BRANCH: ~6 (16%)
- LOOP_COND: ~5 (13%)
- IO_FORMAT: ~4 (11%)
- COMPUTATION: ~3 (8%)
- VAR_INIT: ~3 (8%)
- DATA_TYPE: ~2 (5%)

## Manual Testing Observations

### Perfect Agreement (All 4 models match)
Sample #2, #4, #5, #14, #30, #31, and others (~15 samples, 30%)

### High Disagreement Samples
- Sample #3: Split 2-2 (COMPUTATION vs STMT_INTEGRITY)
- Sample #7: All 4 different predictions
- Sample #8: Split across 3 categories

### Most Common Manual Predictions
- STMT_INTEGRITY: Most frequent
- COMPUTATION: Second most common
- LOOP_COND: High agreement when predicted

## Time Metrics

- Average per sample: ~1.5 minutes (4 models)
- Total testing time (50 samples): ~75 minutes
- Projected total time (200 samples): ~300 minutes (5 hours)

---

*Generated: December 31, 2024*
*Status: 25% complete (50/200 samples)*

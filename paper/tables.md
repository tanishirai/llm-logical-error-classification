# Tables for Paper

## Table 1: Error Category Taxonomy

| Category | Code | Description | Example |
|----------|------|-------------|---------|
| Loop Condition | LOOP_COND | Incorrect loop termination or iteration | `while i < n` should be `while i <= n` |
| Conditional Branch | COND_BRANCH | Wrong if/else condition | `if x > 0` should be `if x >= 0` |
| Statement Integrity | STMT_INTEGRITY | Missing/extra statements | Missing `return` statement |
| I/O Format | IO_FORMAT | Incorrect input/output format | Wrong print format |
| Variable Initialization | VAR_INIT | Uninitialized or wrong initial value | `sum = 1` should be `sum = 0` |
| Data Type | DATA_TYPE | Type mismatch or conversion error | Integer instead of float |
| Computation | COMPUTATION | Wrong formula or operator | `+` instead of `*` |

---

## Table 2: Dataset Statistics

| Dataset | Records | Language | Problem Desc. | Execution Feedback |
|---------|---------|----------|---------------|-------------------|
| Yaksh | 62,806 (42.2%) | Python | ✓ | ✓ |
| Codeforces | 50,000 (33.6%) | C++ | ✓ | ✗ |
| SPOC | 14,558 (9.8%) | C++ | ✓ | ✗ |
| PyPal | 14,408 (9.7%) | Python | ✓ | ✓ (with hints) |
| DeepFix | 6,974 (4.7%) | C | ✓ | ✗ |
| **Total** | **148,746** | **3 languages** | **61.7%** | **51.9%** |

---

## Table 3: Models Under Evaluation

| Model | Version | Provider | Type | Access Method | Parameters |
|-------|---------|----------|------|---------------|------------|
| Qwen Coder | 2.5-7B | Alibaba | Open-source | API | 7B |
| Llama | 3.2-3B | Meta | Open-source | API | 3B |
| Gemini | 2.5 Flash | Google | Closed-source | Web Interface | N/A |
| ChatGPT | GPT-4o | OpenAI | Closed-source | Web Interface | N/A |
| Claude | Sonnet 4.5 | Anthropic | Closed-source | Web Interface | N/A |
| DeepSeek | R1 | DeepSeek | Open-source | Web Interface | N/A |

**Diversity**: 3 open-source vs 3 closed-source, range from 3B to 175B+ parameters

---

## Table 4: Test Set Selection

| Criterion | Value |
|-----------|-------|
| Total unified dataset | 148,746 |
| Random sample | 1,000 |
| Tested samples | 200 |
| Selection method | First 200 from stratified sample |
| Python samples | ~104 (52%) |
| C++ samples | ~87 (43.5%) |
| C samples | ~9 (4.5%) |

---

## Table 5: Model Performance (TO BE FILLED)

| Model | Valid Predictions | Success Rate | Most Common Category | Errors |
|-------|-------------------|--------------|---------------------|---------|
| Qwen 2.5 Coder | X/200 | X% | ? | X |
| Llama 3.2 | X/200 | X% | ? | X |
| Gemini 2.5 Flash | X/200 | X% | ? | X |
| ChatGPT (GPT-4o) | X/200 | X% | ? | X |
| Claude Sonnet 4.5 | X/200 | X% | ? | X |
| DeepSeek R1 | X/200 | X% | ? | X |

---

## Table 6: Inter-Model Agreement (TO BE FILLED)

|  | Qwen | Llama | Gemini | ChatGPT | Claude | DeepSeek |
|--|------|-------|--------|---------|--------|----------|
| **Qwen** | 100% | X% | X% | X% | X% | X% |
| **Llama** | X% | 100% | X% | X% | X% | X% |
| **Gemini** | X% | X% | 100% | X% | X% | X% |
| **ChatGPT** | X% | X% | X% | 100% | X% | X% |
| **Claude** | X% | X% | X% | X% | 100% | X% |
| **DeepSeek** | X% | X% | X% | X% | X% | 100% |

Agreement = % of samples where both models gave same category

---

## Table 7: Category Distribution (TO BE FILLED)

| Category | Frequency | % of Total | Agreement Rate |
|----------|-----------|------------|----------------|
| STMT_INTEGRITY | X | X% | X% |
| COND_BRANCH | X | X% | X% |
| LOOP_COND | X | X% | X% |
| IO_FORMAT | X | X% | X% |
| VAR_INIT | X | X% | X% |
| COMPUTATION | X | X% | X% |
| DATA_TYPE | X | X% | X% |


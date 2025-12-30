# 2. Related Work

## 2.1 Automated Program Repair

**Traditional Approaches:**
- DeepFix [Gupta et al.]: Neural approach for fixing syntax errors in C programs
- DrRepair [Yasunaga et al.]: Graph-based learning for code repair
- **Limitation**: Primarily focus on syntax errors, not logical errors

**LLM-based Approaches:**
- GitHub Copilot: Code completion but not error-specific
- CodeT5, CodeBERT: Pre-trained on code but not error classification
- **Gap**: Limited work on using modern LLMs for error categorization

## 2.2 Error Classification in Student Code

**Manual Classification:**
- [Your base paper - FILL IN]: 7-category taxonomy for logical errors
- Focus on Python/C++ educational datasets
- **Limitation**: Manual labeling doesn't scale

**Automated Classification:**
- Limited prior work using classical ML
- Rule-based systems for specific error types
- **Gap**: No systematic LLM evaluation

## 2.3 LLM Code Understanding

**Capabilities:**
- GPT-4 [OpenAI 2023]: Strong on code explanation
- Claude [Anthropic 2024]: Good at following instructions
- Llama Code [Meta 2024]: Open-source alternative
- Qwen Coder [Alibaba 2024]: Specialized for code

**Evaluation Studies:**
- HumanEval, MBPP benchmarks test code generation
- CodeXGLUE: Code understanding tasks
- **Gap**: No multi-model comparison on error classification

## 2.4 This Work

Our study fills the gap by:
1. Comparing 6 diverse LLMs (open vs closed)
2. Using large-scale real student code (148K samples)
3. Analyzing inter-model agreement
4. Identifying error types needing human validation

[FILL IN CITATIONS AFTER LITERATURE SEARCH]

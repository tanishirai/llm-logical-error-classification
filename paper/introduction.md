# 1. Introduction

Program errors are broadly categorized into two types: syntax errors and logical errors. While syntax errors are caught by compilers and provide clear feedback, logical errors are more subtle—the code compiles and runs but produces incorrect results. This makes logical errors particularly challenging for novice programmers to diagnose and fix.

Prior research has established taxonomies for classifying logical errors in student code. [Reference your base paper] proposed a seven-category classification system including Loop Condition (LOOP_COND), Conditional Branch (COND_BRANCH), Statement Integrity (STMT_INTEGRITY), and others. However, manually classifying thousands of buggy code submissions is time-intensive and requires expert knowledge.

Large Language Models (LLMs) have demonstrated impressive capabilities in code understanding tasks. Recent models like GPT-4, Claude, and open-source alternatives like Llama and Qwen have shown promise in analyzing code semantics. This raises an important question: **Can LLMs reliably classify logical errors in student code?**

## Research Objectives

This study systematically evaluates six state-of-the-art LLMs across three dimensions:

1. **Model diversity**: 3 open-source (Qwen 2.5 Coder, Llama 3.2, DeepSeek R1) vs 3 closed-source (GPT-4o, Claude Sonnet 4.5, Gemini 2.5 Flash)
2. **Scale**: Testing on 200 diverse samples from 148,746 buggy code submissions
3. **Agreement**: Inter-model consistency and conflict patterns

## Contributions

- First systematic comparison of multiple LLMs for logical error classification
- Large-scale unified dataset combining 5 sources (PyPal, Yaksh, Codeforces, SPOC, DeepFix)
- Analysis of agreement patterns between open and closed-source models
- Identification of challenging error categories requiring human validation

## Paper Organization

Section 2 reviews related work in automated program repair and error classification. Section 3 describes our methodology, dataset, and evaluation process. Section 4 presents performance results and agreement analysis. Section 5 discusses implications and limitations. Section 6 concludes with future directions.

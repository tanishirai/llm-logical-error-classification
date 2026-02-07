# Logical Error Classification Using Multiple LLMs

A systematic study comparing 6 large language models (LLMs) for classifying logical errors in student programming submissions.

## 📊 Dataset

- **Total Records**: 148,746 buggy code submissions
- **Sources**: PyPal, Yaksh, Codeforces, SPOC, DeepFix
- **Languages**: Python (52%), C++ (43%), C (5%)
- **Metadata**: 62% with problem descriptions, 52% with execution feedback

### Dataset Distribution

| Source | Records | Percentage |
|--------|---------|------------|
| Yaksh | 62,806 | 42.2% |
| Codeforces | 50,000 | 33.6% |
| SPOC | 14,558 | 9.8% |
| PyPal | 14,408 | 9.7% |
| DeepFix | 6,974 | 4.7% |

## 🤖 Models Evaluated

### Open-Source (API Access)
- **Qwen 2.5 Coder 7B** (Alibaba)
- **Llama 3.2 3B** (Meta)

### Closed-Source (Manual Testing)
- **Gemini 2.5 Flash** (Google)
- **GPT-4o** (OpenAI)
- **Claude Sonnet 4.5** (Anthropic)
- **DeepSeek R1** (DeepSeek)

## 📋 Error Categories

Based on established taxonomy for logical errors:

1. **LOOP_COND** - Loop condition errors
2. **COND_BRANCH** - Conditional branch errors
3. **STMT_INTEGRITY** - Statement integrity issues
4. **IO_FORMAT** - Input/output format errors
5. **VAR_INIT** - Variable initialization errors
6. **DATA_TYPE** - Data type mismatches
7. **COMPUTATION** - Computational/formula errors

## 🗂️ Project Structure

# Logical Error Classification Using Multiple LLMs

A systematic study comparing 6 large language models (LLMs) for classifying logical errors in student programming submissions.

## 📊 Dataset

- **Total Records**: 148,746 buggy code submissions
- **Sources**: PyPal, Yaksh, Codeforces, SPOC, DeepFix
- **Languages**: Python (52%), C++ (43%), C (5%)
- **Metadata**: 62% with problem descriptions, 52% with execution feedback

### Dataset Distribution

| Source | Records | Percentage |
|--------|---------|------------|
| Yaksh | 62,806 | 42.2% |
| Codeforces | 50,000 | 33.6% |
| SPOC | 14,558 | 9.8% |
| PyPal | 14,408 | 9.7% |
| DeepFix | 6,974 | 4.7% |

## 🤖 Models Evaluated

### Open-Source (API Access)
- **Qwen 2.5 Coder 7B** (Alibaba)
- **Llama 3.2 3B** (Meta)

### Closed-Source (Manual Testing)
- **Gemini 2.5 Flash** (Google)
- **GPT-4o** (OpenAI)
- **Claude Sonnet 4.5** (Anthropic)
- **DeepSeek R1** (DeepSeek)

## 📋 Error Categories

Based on established taxonomy for logical errors:

1. **LOOP_COND** - Loop condition errors
2. **COND_BRANCH** - Conditional branch errors
3. **STMT_INTEGRITY** - Statement integrity issues
4. **IO_FORMAT** - Input/output format errors
5. **VAR_INIT** - Variable initialization errors
6. **DATA_TYPE** - Data type mismatches
7. **COMPUTATION** - Computational/formula errors

## 🗂️ Project Structure
.
├── data/ # Dataset files (not in git)
│ ├── unified_dataset.json # 148K combined samples
│ └── README.md # Dataset documentation
│
├── config/ # Configuration files
│ ├── api_keys.json # API credentials (not in git)
│ └── categories.json # Error category definitions
│
├── scripts/ # Python scripts
│ ├── dataset_statistics.py # Generate dataset stats
│ ├── run_predictions_200.py # Automated predictions (200 samples)
│ ├── prepare_manual_testing.py # Prepare manual testing files
│ └── analyze_results.py # Analyze final results
│
├── outputs/ # Results and analysis
│ ├── predictions/ # Model predictions
│ └── manual_testing/ # Manual testing files
│
├── paper/ # Paper drafts and materials
│ ├── outline.md
│ ├── tables.md
│ ├── introduction.md
│ └── references.bib
│
└── README.md # This file

## 🚀 Usage

### 1. Dataset Statistics

python scripts/dataset_statistics.py


### 2. Run Automated Predictions (200 samples)

python scripts/run_predictions_200.py


### 3. Prepare Manual Testing

python scripts/prepare_manual_testing.py


### 4. Analyze Results (after manual testing)

python scripts/analyze_results.py


## 📝 Methodology

1. **Data Collection**: Unified 5 datasets into single JSON format
2. **Sampling**: Selected 200 diverse samples for evaluation
3. **Automated Testing**: API calls to Qwen and Llama models
4. **Manual Testing**: Web interface testing on 4 additional models
5. **Analysis**: Inter-model agreement and performance metrics

## 🔧 Requirements

Python 3.11+
requests
json
pathlib


## ⚙️ Configuration

Create `config/api_keys.json`:

{
"gemini_api_key": "your-key-here",
"huggingface_token": "your-token-here"
}



## 👥 Authors

Tanishi Rai

## 📧 Contact

tanishirai2604@gmail.com

## 📅 Timeline

- Dataset preparation: December 2024
- Automated testing: December 29, 2024
- Manual testing: December 30, 2024 - January 2025
- Analysis & paper writing: January 2025


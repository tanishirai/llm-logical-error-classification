"""
Replace Llama with GPT-OSS Predictions
======================================

Purpose:
    Replace biased Llama 3.2 3B predictions with GPT-NeoX-20B predictions
    for the same 200 samples.

Model: EleutherAI/gpt-neox-20b (20B parameters)
Provider: Hugging Face Inference API

Usage:
    python scripts/replace_llama_with_gptoss.py

Author: [Your Name]
Date: December 31, 2024
"""

import json
import requests
import time
from pathlib import Path


def load_api_config():
    """Load API configuration from config file."""
    config_path = Path(__file__).parent.parent / 'config' / 'api_keys.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config['gpt_oss']


def create_classification_prompt(record):
    """Create prompt for GPT-OSS classification."""
    
    problem_desc = record.get('problem_description') or 'N/A'
    if len(problem_desc) > 300:
        problem_desc = problem_desc[:300] + "..."
    
    exec_feedback = record.get('execution_feedback') or 'N/A'
    if len(exec_feedback) > 200:
        exec_feedback = exec_feedback[:200] + "..."
    
    prompt = f"""You are an expert code analyzer. Classify the PRIMARY logical error in this code.

Categories:
1. LOOP_COND - Incorrect loop condition
2. COND_BRANCH - Incorrect if/else condition
3. STMT_INTEGRITY - Missing or incorrect statement
4. IO_FORMAT - Wrong input/output format
5. VAR_INIT - Wrong variable initialization
6. DATA_TYPE - Incorrect data type
7. COMPUTATION - Wrong calculation

Problem: {problem_desc}

Language: {record.get('language', 'Unknown')}

Buggy Code:
{record.get('buggy_code', '')}

Execution Feedback: {exec_feedback}

Return ONLY the category code (e.g., LOOP_COND, STMT_INTEGRITY, etc.). No explanation."""

    return prompt


def get_gptoss_prediction(record, api_key, model):
    """
    Get prediction from GPT-OSS via Hugging Face API.
    
    Args:
        record: Dataset record
        api_key: Hugging Face API token
        model: Model name (EleutherAI/gpt-neox-20b)
    
    Returns:
        str: Predicted category or ERROR
    """
    
    prompt = create_classification_prompt(record)
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.1,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract prediction from response
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '').strip().upper()
            elif isinstance(result, dict):
                text = result.get('generated_text', '').strip().upper()
            else:
                return "PARSE_ERROR"
            
            # Validate category
            valid_categories = [
                'LOOP_COND', 'COND_BRANCH', 'STMT_INTEGRITY',
                'IO_FORMAT', 'VAR_INIT', 'DATA_TYPE', 'COMPUTATION'
            ]
            
            # Try to extract category from response
            for category in valid_categories:
                if category in text:
                    return category
            
            return "PARSE_ERROR"
        
        elif response.status_code == 503:
            # Model loading
            return "MODEL_LOADING"
        else:
            return f"ERROR_{response.status_code}"
    
    except Exception as e:
        return f"ERROR_{str(e)[:20]}"


def replace_llama_with_gptoss():
    """Replace all Llama predictions with GPT-OSS predictions."""
    
    print("="*80)
    print("🔄 REPLACING LLAMA WITH GPT-OSS (GPT-NeoX-20B)")
    print("="*80)
    print()
    
    # Load API config
    print("Loading API configuration...")
    gpt_config = load_api_config()
    api_key = gpt_config['api_key']
    model = gpt_config['model']
    
    print(f"Model: {model}")
    print(f"Provider: {gpt_config['provider']}")
    print()
    
    # Load predictions
    predictions_file = Path(__file__).parent.parent / 'outputs' / 'predictions' / 'predictions_200_final.json'
    
    print("Loading predictions file...")
    with open(predictions_file, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    
    print(f"Total samples: {len(predictions)}")
    print()
    
    # Load dataset
    sample_path = Path(__file__).parent.parent / 'data' / 'sample_1000.json'
    
    print("Loading dataset...")
    with open(sample_path, 'r', encoding='utf-8') as f:
        all_data = {r['unified_id']: r for r in json.load(f)}
    
    print()
    print("="*80)
    print("🚀 STARTING PREDICTIONS")
    print("="*80)
    print()
    
    # Track results
    valid_count = 0
    error_count = 0
    
    # Run predictions
    for idx, pred in enumerate(predictions, 1):
        unified_id = pred['unified_id']
        record = all_data.get(unified_id)
        
        if not record:
            print(f"Sample {idx}/200: {unified_id} - RECORD NOT FOUND")
            pred['gpt_oss'] = {'prediction': 'ERROR', 'reason': 'Record not found'}
            continue
        
        print(f"Sample {idx}/200: {unified_id}...", end=" ", flush=True)
        
        # Get GPT-OSS prediction
        gptoss_pred = get_gptoss_prediction(record, api_key, model)
        
        # Store prediction (replacing llama)
        pred['gpt_oss'] = {
            'prediction': gptoss_pred,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'model': model
        }
        
        # Track results
        valid_categories = ['LOOP_COND', 'COND_BRANCH', 'STMT_INTEGRITY',
                           'IO_FORMAT', 'VAR_INIT', 'DATA_TYPE', 'COMPUTATION']
        
        if gptoss_pred in valid_categories:
            valid_count += 1
            print(f"✓ {gptoss_pred}")
        else:
            error_count += 1
            print(f"✗ {gptoss_pred}")
        
        # Rate limiting - important for free tier!
        if gptoss_pred == "MODEL_LOADING":
            print("   ⏳ Model loading, waiting 10 seconds...")
            time.sleep(10)
        else:
            time.sleep(1.5)  # Rate limit for free tier
        
        # Save progress every 20 samples
        if idx % 20 == 0:
            temp_file = Path(__file__).parent.parent / 'outputs' / 'predictions' / 'predictions_200_gptoss_temp.json'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(predictions, f, indent=2)
            print(f"   💾 Progress saved (checkpoint at {idx}/200)")
    
    print()
    print("="*80)
    print("📊 RESULTS")
    print("="*80)
    print(f"Valid predictions: {valid_count}/{len(predictions)} ({valid_count/len(predictions)*100:.1f}%)")
    print(f"Errors: {error_count}/{len(predictions)} ({error_count/len(predictions)*100:.1f}%)")
    print()
    
    # Save final results
    output_file = Path(__file__).parent.parent / 'outputs' / 'predictions' / 'predictions_200_with_gptoss.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, indent=2)
    
    print(f"✅ SAVED: {output_file}")
    print()
    print("="*80)
    print("✨ NEXT STEPS")
    print("="*80)
    print("1. Review the predictions above")
    print("2. If many errors, check API status and retry")
    print("3. Run: python scripts\\update_csv_with_gptoss.py")
    print("4. Continue manual testing with updated CSV")
    print("="*80)


if __name__ == "__main__":
    replace_llama_with_gptoss()

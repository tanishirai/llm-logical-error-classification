import json
import time
import re
from pathlib import Path
from datetime import datetime
import requests
from google import genai


def load_config():
    """Load API configuration"""
    config_path = Path(__file__).parent.parent / 'config' / 'api_keys.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_sample(num_samples=None):
    """Load sample dataset"""
    sample_path = Path(__file__).parent.parent / 'data' / 'sample_1000.json'
    with open(sample_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if num_samples:
        return data[:num_samples]
    return data


def create_prompt(record):
    """Import from prompt_template.py"""
    from prompt_template import create_classification_prompt
    return create_classification_prompt(record)


def extract_category_code(response_text):
    """Extract category code from model response"""
    valid_codes = ['LOOP_COND', 'COND_BRANCH', 'STMT_INTEGRITY', 
                   'IO_FORMAT', 'VAR_INIT', 'DATA_TYPE', 'COMPUTATION']
    
    text = response_text.strip().upper()
    text = re.sub(r'</?THINK>', '', text, flags=re.IGNORECASE)
    
    # Look for exact code matches
    for code in valid_codes:
        pattern = r'\b' + re.escape(code) + r'\b'
        if re.search(pattern, text):
            return code
    
    # Check last lines for answer
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in reversed(lines[-5:]):
        for code in valid_codes:
            if code in line and len(line) < 50:
                return code
    
    return "PARSE_ERROR"


def predict_gemini(prompt, config):
    """Get prediction from Gemini"""
    try:
        client = genai.Client(
            api_key=config['gemini']['api_key'],
            http_options={'api_version': 'v1'}
        )
        
        response = client.models.generate_content(
            model=config['gemini']['model'],
            contents=prompt
        )
        
        return extract_category_code(response.text)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return "QUOTA_EXCEEDED"
        return "ERROR"


def predict_huggingface(prompt, model_name, config, max_retries=3):
    """Get prediction from Hugging Face with retry logic"""
    for attempt in range(max_retries):
        try:
            API_URL = "https://router.huggingface.co/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {config['deepseek']['api_key']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150,
                "temperature": 0.1
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
            
            if response.status_code == 200:
                result = response.json()
                raw_response = result['choices'][0]['message']['content']
                return extract_category_code(raw_response)
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 15 * (attempt + 1)
                    print(f"(rate limit, waiting {wait_time}s)", end=" ", flush=True)
                    time.sleep(wait_time)
                    continue
                return "RATE_LIMITED"
            elif response.status_code == 400:
                return "MODEL_NOT_AVAILABLE"
            else:
                return "ERROR"
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(10)
                continue
            return "ERROR"
    
    return "ERROR"


def run_5models_batch(num_samples=10):
    """Run predictions with all 5 models"""
    
    print("="*80)
    print("RUNNING PREDICTIONS - ALL 5 MODELS")
    print("="*80)
    print()
    
    config = load_config()
    sample = load_sample(num_samples)
    
    print(f"📊 Testing with {len(sample)} samples")
    print(f"🤖 Models: Gemini, DeepSeek, Qwen, GPT-NeoX, Llama")
    print(f"⏱️  Estimated time: ~{len(sample) * 3} minutes (with rate limit delays)")
    print()
    
    results = []
    model_stats = {
        'gemini': {'success': 0, 'errors': 0},
        'deepseek': {'success': 0, 'errors': 0},
        'qwen': {'success': 0, 'errors': 0},
        'gpt_neox': {'success': 0, 'errors': 0},
        'llama': {'success': 0, 'errors': 0}
    }
    
    valid_codes = ['LOOP_COND', 'COND_BRANCH', 'STMT_INTEGRITY', 
                   'IO_FORMAT', 'VAR_INIT', 'DATA_TYPE', 'COMPUTATION']
    
    for i, record in enumerate(sample, 1):
        print(f"\n[{i}/{len(sample)}] {record['unified_id']} ({record['source_dataset']})...")
        
        prompt = create_prompt(record)
        
        predictions = {
            'unified_id': record['unified_id'],
            'source_dataset': record['source_dataset'],
            'language': record['language'],
            'timestamp': datetime.now().isoformat()
        }
        
        # 1. Gemini
        print("  • Gemini...", end=" ", flush=True)
        predictions['gemini'] = predict_gemini(prompt, config)
        print(f"✓ {predictions['gemini']}")
        if predictions['gemini'] in valid_codes:
            model_stats['gemini']['success'] += 1
        else:
            model_stats['gemini']['errors'] += 1
        time.sleep(3)
        
        # 2. DeepSeek
        print("  • DeepSeek...", end=" ", flush=True)
        predictions['deepseek'] = predict_huggingface(
            prompt, 
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
            config
        )
        print(f"✓ {predictions['deepseek']}")
        if predictions['deepseek'] in valid_codes:
            model_stats['deepseek']['success'] += 1
        else:
            model_stats['deepseek']['errors'] += 1
        time.sleep(5)
        
        # 3. Qwen
        print("  • Qwen...", end=" ", flush=True)
        predictions['qwen'] = predict_huggingface(
            prompt,
            "Qwen/Qwen2.5-Coder-7B-Instruct",
            config
        )
        print(f"✓ {predictions['qwen']}")
        if predictions['qwen'] in valid_codes:
            model_stats['qwen']['success'] += 1
        else:
            model_stats['qwen']['errors'] += 1
        time.sleep(5)
        
        # 4. GPT-NeoX (GPT OSS)
        print("  • GPT-NeoX...", end=" ", flush=True)
        predictions['gpt_neox'] = predict_huggingface(
            prompt,
            "EleutherAI/gpt-neox-20b",
            config
        )
        print(f"✓ {predictions['gpt_neox']}")
        if predictions['gpt_neox'] in valid_codes:
            model_stats['gpt_neox']['success'] += 1
        else:
            model_stats['gpt_neox']['errors'] += 1
        time.sleep(5)
        
        # 5. Llama
        print("  • Llama...", end=" ", flush=True)
        predictions['llama'] = predict_huggingface(
            prompt,
            "meta-llama/Llama-3.2-3B-Instruct",
            config
        )
        print(f"✓ {predictions['llama']}")
        if predictions['llama'] in valid_codes:
            model_stats['llama']['success'] += 1
        else:
            model_stats['llama']['errors'] += 1
        
        results.append(predictions)
        
        # Wait between samples
        if i < len(sample):
            print("  (waiting 12s for rate limit reset...)", end="", flush=True)
            time.sleep(12)
            print(" done")
    
    # Save results
    output_dir = Path(__file__).parent.parent / 'outputs' / 'predictions'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f'predictions_5models_{len(sample)}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n✅ Predictions saved to: {output_file}")
    
    # Show summary
    print("\n" + "="*80)
    print("📊 PREDICTION SUMMARY - ALL 5 MODELS")
    print("="*80)
    print(f"{'Model':<15} {'Valid':<10} {'Errors':<10} {'Success %':<15}")
    print("-" * 80)
    
    for model_name, stats in model_stats.items():
        total = stats['success'] + stats['errors']
        rate = (stats['success'] / total * 100) if total > 0 else 0
        print(f"{model_name.capitalize():<15} {stats['success']:<10} {stats['errors']:<10} {rate:.1f}%")
    
    # Calculate conflicts
    models = ['gemini', 'deepseek', 'qwen', 'gpt_neox', 'llama']
    valid_results = [r for r in results 
                     if all(r[m] in valid_codes for m in models)]
    
    conflicts = []
    for r in valid_results:
        predictions_set = {r[m] for m in models}
        conflict_count = len(predictions_set)
        if conflict_count > 1:
            conflicts.append((r['unified_id'], conflict_count))
    
    print("\n" + "="*80)
    print(f"Total samples:          {len(results)}")
    print(f"All 5 models valid:     {len(valid_results)}")
    print(f"Samples with conflicts: {len(conflicts)} ({len(conflicts)/len(results)*100:.1f}%)")
    if conflicts:
        high_conflict = sum(1 for _, c in conflicts if c >= 4)
        print(f"High conflict (4+ different): {high_conflict}")
    print("="*80)
    
    return results


if __name__ == "__main__":
    print("\n🚀 5-MODEL PREDICTION TEST")
    print("⏱️  10 samples will take ~30 minutes")
    print("⏱️  300 samples will take ~15 hours\n")
    
    input("Press Enter to start 10-sample test with all 5 models...")
    
    run_5models_batch(num_samples=10)


import json
import time
import re
from pathlib import Path
from datetime import datetime
import requests
from google import genai

def load_config():
    config_path = Path(__file__).parent.parent / 'config' / 'api_keys.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_sample(num_samples=300):
    sample_path = Path(__file__).parent.parent / 'data' / 'sample_1000.json'
    with open(sample_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data[:num_samples]

def create_prompt(record):
    from prompt_template import create_classification_prompt
    return create_classification_prompt(record)

def extract_category_code(response_text):
    valid_codes = ['LOOP_COND', 'COND_BRANCH', 'STMT_INTEGRITY', 
                   'IO_FORMAT', 'VAR_INIT', 'DATA_TYPE', 'COMPUTATION']
    
    text = response_text.strip().upper()
    text = re.sub(r'</?THINK>', '', text, flags=re.IGNORECASE)
    
    for code in valid_codes:
        pattern = r'\b' + re.escape(code) + r'\b'
        if re.search(pattern, text):
            return code
    
    return "PARSE_ERROR"

def predict_gemini(prompt, config):
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
        if "429" in error_msg:
            return "QUOTA_EXCEEDED"
        return "ERROR"

def predict_huggingface(prompt, model_name, config, max_retries=2):
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
                "max_tokens": 50,  # Reduced for speed
                "temperature": 0.1
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                raw_response = result['choices'][0]['message']['content']
                return extract_category_code(raw_response)
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                return "RATE_LIMITED"
            else:
                return "ERROR"
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return "ERROR"
    
    return "ERROR"

def run_predictions_300_fast():
    print("="*80)
    print("⚡ FAST 300-SAMPLE PREDICTIONS - 3 MODELS")
    print("="*80)
    print()
    
    config = load_config()
    sample = load_sample(300)
    
    print(f"📊 Processing {len(sample)} samples")
    print(f"🤖 Models: Gemini, Qwen, Llama")
    print(f"⏱️  Estimated time: 60-90 minutes (FAST MODE)")
    print(f"💾 Auto-saves every 50 samples")
    print()
    
    output_dir = Path(__file__).parent.parent / 'outputs' / 'predictions'
    output_dir.mkdir(parents=True, exist_ok=True)
    progress_file = output_dir / 'predictions_300_progress.json'
    
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            results = json.load(f)
        print(f"📂 Resuming from {len(results)} predictions\n")
    else:
        results = []
    
    start_idx = len(results)
    model_stats = {
        'gemini': {'success': 0, 'errors': 0},
        'qwen': {'success': 0, 'errors': 0},
        'llama': {'success': 0, 'errors': 0}
    }
    
    valid_codes = ['LOOP_COND', 'COND_BRANCH', 'STMT_INTEGRITY', 
                   'IO_FORMAT', 'VAR_INIT', 'DATA_TYPE', 'COMPUTATION']
    
    start_time = time.time()
    
    for i, record in enumerate(sample[start_idx:], start_idx + 1):
        if i % 10 == 1:
            print(f"\n[{i}/{len(sample)}] Processing...")
        else:
            print(f"[{i}]", end=" ", flush=True)
        
        prompt = create_prompt(record)
        
        predictions = {
            'unified_id': record['unified_id'],
            'source_dataset': record['source_dataset'],
            'language': record['language'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Gemini
        predictions['gemini'] = predict_gemini(prompt, config)
        if predictions['gemini'] in valid_codes:
            model_stats['gemini']['success'] += 1
        else:
            model_stats['gemini']['errors'] += 1
        time.sleep(1)  # Minimal wait
        
        # Qwen
        predictions['qwen'] = predict_huggingface(
            prompt, "Qwen/Qwen2.5-Coder-7B-Instruct", config
        )
        if predictions['qwen'] in valid_codes:
            model_stats['qwen']['success'] += 1
        else:
            model_stats['qwen']['errors'] += 1
        time.sleep(2)  # Reduced wait
        
        # Llama
        predictions['llama'] = predict_huggingface(
            prompt, "meta-llama/Llama-3.2-3B-Instruct", config
        )
        if predictions['llama'] in valid_codes:
            model_stats['llama']['success'] += 1
        else:
            model_stats['llama']['errors'] += 1
        
        results.append(predictions)
        
        # Progress update
        if i % 10 == 0:
            elapsed = time.time() - start_time
            rate = (i - start_idx) / elapsed if elapsed > 0 else 0
            remaining = (len(sample) - i) / rate if rate > 0 else 0
            print(f"  ⏱️ {elapsed/60:.1f}m / ~{remaining/60:.1f}m left")
        
        # Save progress
        if i % 50 == 0:
            with open(progress_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"  💾 Saved {i}/{len(sample)}")
        
        # Short wait between samples
        time.sleep(3)  # Reduced from 6
    
    # Final save
    final_file = output_dir / 'predictions_300_final.json'
    with open(final_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n✅ SAVED: {final_file}")
    
    # Summary
    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80)
    
    for model_name, stats in model_stats.items():
        total = stats['success'] + stats['errors']
        rate = (stats['success'] / total * 100) if total > 0 else 0
        print(f"{model_name.upper():<10}: {stats['success']}/{total} valid ({rate:.1f}%)")
    
    # Conflicts
    valid_results = [r for r in results 
                     if all(r[m] in valid_codes for m in ['gemini', 'qwen', 'llama'])]
    
    conflicts = [r for r in valid_results 
                 if len({r['gemini'], r['qwen'], r['llama']}) > 1]
    
    conflicts_file = output_dir / 'conflicts_300.json'
    with open(conflicts_file, 'w') as f:
        json.dump(conflicts, f, indent=2)
    
    print(f"\nTotal samples:    {len(results)}")
    print(f"Valid (all 3):    {len(valid_results)}")
    print(f"Conflicts:        {len(conflicts)} ({len(conflicts)/len(results)*100:.1f}%)")
    print(f"\n💾 Conflicts: {conflicts_file}")
    
    total_time = time.time() - start_time
    print(f"⏱️  Total: {total_time/60:.1f} min")
    print("="*80)

if __name__ == "__main__":
    print("\n⚡ FAST MODE - 300 Samples")
    print("⏱️  Time: ~60-90 minutes\n")
    
    input("Press Enter to start...")
    
    run_predictions_300_fast()

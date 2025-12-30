import json
from pathlib import Path

def extract_qwen_llama_conflicts():
    """Extract conflicts between Qwen and Llama (ignoring Gemini failures)"""
    
    predictions_file = Path(__file__).parent.parent / 'outputs' / 'predictions' / 'predictions_300_final.json'
    
    with open(predictions_file, 'r') as f:
        results = json.load(f)
    
    valid_codes = ['LOOP_COND', 'COND_BRANCH', 'STMT_INTEGRITY', 
                   'IO_FORMAT', 'VAR_INIT', 'DATA_TYPE', 'COMPUTATION']
    
    # Filter where Qwen and Llama both valid
    qwen_llama_valid = [r for r in results 
                        if r['qwen'] in valid_codes and r['llama'] in valid_codes]
    
    # Find conflicts
    conflicts = []
    for r in qwen_llama_valid:
        if r['qwen'] != r['llama']:
            conflict_entry = {
                'unified_id': r['unified_id'],
                'source_dataset': r['source_dataset'],
                'language': r['language'],
                'qwen_prediction': r['qwen'],
                'llama_prediction': r['llama'],
                'gemini_prediction': r.get('gemini', 'N/A')
            }
            conflicts.append(conflict_entry)
    
    # Save conflicts
    output_dir = Path(__file__).parent.parent / 'outputs' / 'predictions'
    conflicts_file = output_dir / 'conflicts_qwen_llama.json'
    
    with open(conflicts_file, 'w') as f:
        json.dump(conflicts, f, indent=2, ensure_ascii=False)
    
    # Statistics
    print("="*80)
    print("QWEN vs LLAMA CONFLICT ANALYSIS")
    print("="*80)
    print(f"\nTotal samples analyzed:        {len(results)}")
    print(f"Qwen + Llama both valid:       {len(qwen_llama_valid)} ({len(qwen_llama_valid)/len(results)*100:.1f}%)")
    print(f"Conflicts (Qwen ≠ Llama):      {len(conflicts)} ({len(conflicts)/len(qwen_llama_valid)*100:.1f}%)")
    
    # Breakdown by category
    print("\n" + "-"*80)
    print("CONFLICT BREAKDOWN:")
    print("-"*80)
    
    conflict_pairs = {}
    for c in conflicts:
        pair = f"{c['qwen_prediction']} vs {c['llama_prediction']}"
        conflict_pairs[pair] = conflict_pairs.get(pair, 0) + 1
    
    for pair, count in sorted(conflict_pairs.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pair:<45} {count:>3} conflicts")
    
    print("\n" + "-"*80)
    print("DATASET DISTRIBUTION:")
    print("-"*80)
    
    dataset_counts = {}
    for c in conflicts:
        ds = c['source_dataset']
        dataset_counts[ds] = dataset_counts.get(ds, 0) + 1
    
    for dataset, count in sorted(dataset_counts.items()):
        print(f"  {dataset:<20} {count:>3} conflicts")
    
    print("\n" + "="*80)
    print(f"💾 Conflicts saved to: {conflicts_file}")
    print("="*80)
    
    return conflicts

if __name__ == "__main__":
    conflicts = extract_qwen_llama_conflicts()

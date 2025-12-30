import json
import random
from pathlib import Path

def create_sample_dataset(sample_size=1000, subset_size=100):
    """Create samples for automated and manual testing"""
    
    # Load unified dataset
    data_path = Path(__file__).parent.parent / 'data' / 'unified_dataset.json'
    
    print(f"Loading unified dataset from {data_path}...")
    with open(data_path, 'r', encoding='utf-8') as f:
        all_records = json.load(f)
    
    print(f"Total records: {len(all_records)}")
    
    # Random sample for automated testing
    random.seed(42)  # For reproducibility
    sample = random.sample(all_records, min(sample_size, len(all_records)))
    
    # Save main sample
    output_dir = Path(__file__).parent.parent / 'data'
    sample_path = output_dir / f'sample_{sample_size}.json'
    
    with open(sample_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Created main sample: {len(sample)} records")
    print(f"✅ Saved to: {sample_path}")
    
    # Create smaller subset for manual testing
    subset = random.sample(sample, min(subset_size, len(sample)))
    subset_path = output_dir / f'sample_manual_{subset_size}.json'
    
    with open(subset_path, 'w', encoding='utf-8') as f:
        json.dump(subset, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Created manual testing subset: {len(subset)} records")
    print(f"✅ Saved to: {subset_path}")
    
    # Show distribution
    dataset_counts = {}
    for record in sample:
        ds = record['source_dataset']
        dataset_counts[ds] = dataset_counts.get(ds, 0) + 1
    
    print("\n📊 Sample Distribution:")
    print("-" * 40)
    for dataset, count in sorted(dataset_counts.items()):
        percentage = (count / len(sample)) * 100
        print(f"  {dataset:<15}: {count:>4} ({percentage:>5.2f}%)")
    print("-" * 40)
    
    print("\n💡 TESTING STRATEGY:")
    print(f"  Phase 1: Run 4 automated models on {sample_size} samples (~2-3 hours)")
    print(f"  Phase 2: Manual test top 100 conflicts on Claude + GPT-5 (~50 min)")
    print("-" * 40)
    
    return sample_path, subset_path

if __name__ == "__main__":
    # Create both samples
    create_sample_dataset(sample_size=1000, subset_size=100)

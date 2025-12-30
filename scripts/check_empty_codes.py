"""
Empty Code Diagnostic Script
=============================

Purpose:
    Check for samples with empty or missing buggy code in the test set.
    Identifies which samples cannot be tested due to missing code.

Usage:
    python scripts/check_empty_codes.py

Author: [Your Name]
Date: December 2024
"""

import json
from pathlib import Path

# File paths
predictions_file = Path(__file__).parent.parent / 'outputs' / 'predictions' / 'predictions_200_final.json'
sample_file = Path(__file__).parent.parent / 'data' / 'sample_1000.json'

# Load predictions
with open(predictions_file, 'r', encoding='utf-8') as f:
    predictions = json.load(f)

# Load original data with UTF-8 encoding
with open(sample_file, 'r', encoding='utf-8') as f:
    all_data = {r['unified_id']: r for r in json.load(f)}

print("="*80)
print("CHECKING FOR EMPTY BUGGY CODES")
print("="*80)
print()

empty_samples = []
empty_count = 0

for idx, pred in enumerate(predictions, 1):
    record = all_data.get(pred['unified_id'])
    if record:
        buggy_code = record.get('buggy_code', '').strip()
        if not buggy_code:
            empty_count += 1
            empty_samples.append({
                'sample_num': idx,
                'unified_id': pred['unified_id'],
                'qwen': pred.get('qwen', 'ERROR'),
                'llama': pred.get('llama', 'ERROR')
            })
            print(f"Sample #{idx}: {pred['unified_id']}")
            print(f"  Dataset: {pred.get('source_dataset', 'N/A')}")
            print(f"  Language: {pred.get('language', 'N/A')}")
            print(f"  Qwen: {pred.get('qwen', 'ERROR')}")
            print(f"  Llama: {pred.get('llama', 'ERROR')}")
            print(f"  Status: ❌ EMPTY BUGGY CODE")
            print()

print("="*80)
print("SUMMARY")
print("="*80)
print(f"Total samples checked: {len(predictions)}")
print(f"Samples with empty code: {empty_count}")
print(f"Valid samples for testing: {len(predictions) - empty_count}")
print()

if empty_count > 0:
    print(f"⚠️  {empty_count} samples cannot be tested (no buggy code)")
    print(f"✅ {len(predictions) - empty_count} samples are ready for manual testing")
    print()
    print("RECOMMENDATION:")
    if empty_count <= 5:
        print(f"  → Skip these {empty_count} samples during manual testing")
        print(f"  → Focus on the remaining {len(predictions) - empty_count} samples")
    else:
        print(f"  → Regenerate test set excluding empty samples")
        print(f"  → Run: python scripts/create_valid_test_set.py")
else:
    print("✅ All samples have valid buggy code!")
    print("✅ Ready to proceed with manual testing!")

print("="*80)

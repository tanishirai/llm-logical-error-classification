import json
import pandas as pd
from pathlib import Path
import os
import re


def load_pypal(filepath):
    """Load and standardize PyPal dataset"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    standardized = []
    for idx, record in enumerate(data):
        standardized.append({
            'unified_id': f"PYPAL_{idx:06d}",
            'original_id': record.get('uid', ''),
            'source_dataset': 'PyPal',
            'problem_id': f"concept{record.get('concept_number')}_q{record.get('question_number')}",
            'problem_description': record.get('question', ''),
            'buggy_code': record.get('buggy_code', ''),
            'correct_code': None,
            'language': 'Python',
            'execution_feedback': record.get('execution_feedback', ''),
            'hint': record.get('hint', ''),
            'ground_truth_label': None,
            'additional_info': {
                'concept_number': record.get('concept_number'),
                'question_number': record.get('question_number'),
                'anon_id': record.get('anon_id')
            }
        })
    return standardized


def load_yaksh(filepath):
    """Load and standardize Yaksh dataset"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    standardized = []
    for idx, record in enumerate(data):
        standardized.append({
            'unified_id': record.get('uid', f"YAKSH_{idx:06d}"),
            'original_id': record.get('uid', ''),
            'source_dataset': 'Yaksh',
            'problem_id': None,
            'problem_description': record.get('problem_description', ''),
            'buggy_code': record.get('buggy_code', ''),
            'correct_code': None,
            'language': record.get('language', 'Python'),
            'execution_feedback': record.get('execution_feedback', ''),
            'hint': None,
            'ground_truth_label': record.get('ground_truth'),
            'additional_info': {}
        })
    return standardized


def load_codeforces(filepath):
    """Load and standardize Codeforces dataset"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    standardized = []
    for idx, record in enumerate(data):
        standardized.append({
            'unified_id': f"CODEFORCES_{idx:06d}",
            'original_id': record.get('file_name', ''),
            'source_dataset': 'Codeforces',
            'problem_id': record.get('problem_id', ''),
            'problem_description': None,
            'buggy_code': record.get('code', ''),
            'correct_code': None,
            'language': 'C++',
            'execution_feedback': None,
            'hint': None,
            'ground_truth_label': None,
            'additional_info': {
                'file_name': record.get('file_name')
            }
        })
    return standardized


def load_deepfix(filepath):
    """Load and standardize DeepFix dataset"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    standardized = []
    for idx, record in enumerate(data):
        standardized.append({
            'unified_id': f"DEEPFIX_{idx:06d}",
            'original_id': record.get('file_name', ''),
            'source_dataset': 'DeepFix',
            'problem_id': record.get('problem_id', ''),
            'problem_description': None,
            'buggy_code': record.get('erroneous_code', ''),
            'correct_code': record.get('correct_code', ''),
            'language': 'C',
            'execution_feedback': None,
            'hint': None,
            'ground_truth_label': None,
            'additional_info': {
                'file_name': record.get('file_name')
            }
        })
    return standardized


def load_spoc(filepath):
    """Load and standardize SPOC dataset"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    standardized = []
    for idx, record in enumerate(data):
        description = record.get('description', [])
        if isinstance(description, list):
            description = '\n'.join(description)
        
        standardized.append({
            'unified_id': f"SPOC_{idx:06d}",
            'original_id': record.get('submission_id', ''),
            'source_dataset': 'SPOC',
            'problem_id': record.get('problem_id', ''),
            'problem_description': description,
            'buggy_code': record.get('code', ''),
            'correct_code': None,
            'language': 'C++',
            'execution_feedback': None,
            'hint': None,
            'ground_truth_label': None,
            'additional_info': {
                'submission_id': record.get('submission_id')
            }
        })
    return standardized


def clean_for_excel(val):
    """Remove illegal characters for Excel"""
    if val is None:
        return val
    if isinstance(val, str):
        # Remove control characters that Excel doesn't support
        # Keep newlines (\n) and tabs (\t), remove others
        return re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', val)
    return val


def combine_all_datasets():
    """Main function to combine all datasets"""
    
    # Get the script's directory and navigate to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Define dataset paths
    base_path = project_root / 'data' / 'final_clean_datasets'
    datasets = {
        'pypal': base_path / 'pypal_clean.json',
        'yaksh': base_path / 'yaksh_logical_dedup.json',
        'codeforces': base_path / 'codeforces_clean.json',
        'deepfix': base_path / 'deepfix_clean.json',
        'spoc': base_path / 'spoc_programs.json'
    }
    
    # Verify all files exist
    print("Checking for dataset files...")
    for name, path in datasets.items():
        if not path.exists():
            print(f"❌ ERROR: {name} dataset not found at {path}")
            print(f"   Please copy {path.name} to data/final_clean_datasets/")
            return
        else:
            print(f"✓ Found {name}")
    
    # Load and standardize each dataset
    all_records = []
    dataset_stats = {}
    
    print("\n" + "="*60)
    print("Loading datasets...")
    print("="*60)
    
    # PyPal
    print(f"\n📂 Loading PyPal...")
    pypal_data = load_pypal(datasets['pypal'])
    all_records.extend(pypal_data)
    dataset_stats['PyPal'] = len(pypal_data)
    print(f"   ✓ Loaded {len(pypal_data)} records")
    
    # Yaksh
    print(f"\n📂 Loading Yaksh...")
    yaksh_data = load_yaksh(datasets['yaksh'])
    all_records.extend(yaksh_data)
    dataset_stats['Yaksh'] = len(yaksh_data)
    print(f"   ✓ Loaded {len(yaksh_data)} records")
    
    # Codeforces
    print(f"\n📂 Loading Codeforces...")
    codeforces_data = load_codeforces(datasets['codeforces'])
    all_records.extend(codeforces_data)
    dataset_stats['Codeforces'] = len(codeforces_data)
    print(f"   ✓ Loaded {len(codeforces_data)} records")
    
    # DeepFix
    print(f"\n📂 Loading DeepFix...")
    deepfix_data = load_deepfix(datasets['deepfix'])
    all_records.extend(deepfix_data)
    dataset_stats['DeepFix'] = len(deepfix_data)
    print(f"   ✓ Loaded {len(deepfix_data)} records")
    
    # SPOC
    print(f"\n📂 Loading SPOC...")
    spoc_data = load_spoc(datasets['spoc'])
    all_records.extend(spoc_data)
    dataset_stats['SPOC'] = len(spoc_data)
    print(f"   ✓ Loaded {len(spoc_data)} records")
    
    # Create output directory
    output_dir = project_root / 'data'
    output_dir.mkdir(exist_ok=True)
    
    # Save as JSON
    print("\n" + "="*60)
    print("💾 Saving unified_dataset.json...")
    json_output = output_dir / 'unified_dataset.json'
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved to {json_output}")
    
    # Save as Excel (with cleaning)
    print("\n💾 Saving unified_dataset.xlsx...")
    df = pd.DataFrame(all_records)
    df['additional_info'] = df['additional_info'].apply(lambda x: json.dumps(x))
    
    # Clean all string columns for Excel compatibility
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(clean_for_excel)
    
    excel_output = output_dir / 'unified_dataset.xlsx'
    df.to_excel(excel_output, index=False, engine='openpyxl')
    print(f"   ✓ Saved to {excel_output}")
    
    # Generate summary statistics
    print("\n💾 Generating summary...")
    summary_output = output_dir / 'dataset_summary.txt'
    with open(summary_output, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("UNIFIED DATASET SUMMARY\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Total Records: {len(all_records)}\n\n")
        
        f.write("Records per Dataset:\n")
        f.write("-"*40 + "\n")
        for dataset, count in dataset_stats.items():
            percentage = (count / len(all_records)) * 100
            f.write(f"  {dataset:<15}: {count:>6} ({percentage:>5.2f}%)\n")
        
        f.write("\n" + "-"*40 + "\n")
        f.write(f"{'Total':<15}: {len(all_records):>6} (100.00%)\n")
        
        # Language distribution
        f.write("\n\nLanguage Distribution:\n")
        f.write("-"*40 + "\n")
        lang_counts = {}
        for record in all_records:
            lang = record['language']
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        for lang, count in sorted(lang_counts.items()):
            percentage = (count / len(all_records)) * 100
            f.write(f"  {lang:<15}: {count:>6} ({percentage:>5.2f}%)\n")
        
        f.write("\n" + "="*60 + "\n")
    
    print(f"   ✓ Saved to {summary_output}")
    
    # Print summary to console
    print("\n" + "="*60)
    print("✅ COMBINATION COMPLETE!")
    print("="*60)
    print(f"\nTotal records combined: {len(all_records)}")
    print("\nBreakdown by dataset:")
    for dataset, count in dataset_stats.items():
        print(f"  • {dataset}: {count} records")
    
    print("\n📁 Output files created in data/ folder:")
    print("  • unified_dataset.json")
    print("  • unified_dataset.xlsx")
    print("  • dataset_summary.txt")
    print("\n" + "="*60)
    
    return all_records


if __name__ == "__main__":
    combine_all_datasets()

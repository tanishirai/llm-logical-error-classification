"""
Dataset Statistics Generator
============================

Purpose:
    Generate comprehensive statistics about the unified dataset of buggy code samples.
    
Output:
    Prints to console:
    - Total record count
    - Distribution by source dataset
    - Distribution by programming language
    - Metadata availability (hints, problem descriptions, execution feedback)
    
Usage:
    python scripts/dataset_statistics.py
    
Author: [Your Name]
Date: December 2024
Part of: FOSSEE Internship - Logical Error Classification Study
"""

import json
from pathlib import Path
from collections import Counter


def analyze_unified_dataset():
    """
    Analyze the unified dataset and print comprehensive statistics.
    
    Reads:
        data/unified_dataset.json - Full dataset (148K+ records)
    
    Prints:
        - Total records
        - Per-dataset distribution with percentages
        - Per-language distribution with percentages
        - Metadata field availability
    
    Returns:
        None (prints to stdout)
    """
    
    # Construct path to unified dataset relative to script location
    data_path = Path(__file__).parent.parent / 'data' / 'unified_dataset.json'
    
    # Load the entire dataset into memory
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Print header
    print("="*80)
    print("UNIFIED DATASET STATISTICS")
    print("="*80)
    print()
    
    # ========================================
    # Basic Statistics
    # ========================================
    print(f"Total records: {len(data):,}")
    print()
    
    # ========================================
    # Distribution by Source Dataset
    # ========================================
    print("Distribution by Dataset:")
    print("-"*80)
    
    # Count occurrences of each dataset using Counter
    datasets = Counter(r['source_dataset'] for r in data)
    
    # Sort by count (descending) and display with percentages
    for ds, count in sorted(datasets.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(data) * 100
        print(f"  {ds:<20} {count:>7,} ({pct:>5.2f}%)")
    
    print()
    
    # ========================================
    # Distribution by Programming Language
    # ========================================
    print("Distribution by Language:")
    print("-"*80)
    
    # Count occurrences of each language
    languages = Counter(r['language'] for r in data)
    
    # Sort by count (descending) and display with percentages
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(data) * 100
        print(f"  {lang:<20} {count:>7,} ({pct:>5.2f}%)")
    
    print()
    
    # ========================================
    # Metadata Availability
    # ========================================
    
    # Count records with non-empty 'hint' field
    with_hints = sum(1 for r in data if r.get('hint'))
    print(f"Records with hints: {with_hints:,} ({with_hints/len(data)*100:.2f}%)")
    
    # Count records with non-empty 'problem_description' field
    with_desc = sum(1 for r in data if r.get('problem_description'))
    print(f"Records with problem description: {with_desc:,} ({with_desc/len(data)*100:.2f}%)")
    
    # Count records with non-empty 'execution_feedback' field
    with_feedback = sum(1 for r in data if r.get('execution_feedback'))
    print(f"Records with execution feedback: {with_feedback:,} ({with_feedback/len(data)*100:.2f}%)")
    
    print()
    print("="*80)


if __name__ == "__main__":
    """
    Main entry point when script is run directly.
    
    Executes the dataset analysis and prints results to console.
    No command-line arguments required.
    """
    analyze_unified_dataset()

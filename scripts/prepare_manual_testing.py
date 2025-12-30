"""
Manual Testing Preparation Script
==================================

Purpose:
    Prepare files for manual testing of 200 samples across 4 additional LLMs.
    Creates a CSV file with automated predictions pre-filled and a text file
    with formatted prompts for easy copy-paste testing.

Input:
    - outputs/predictions/predictions_200_final.json (automated predictions)
    - data/sample_1000.json (original dataset records)

Output:
    - outputs/manual_testing/manual_testing_200_samples.csv (tracking sheet)
    - outputs/manual_testing/prompts_200_samples.txt (formatted prompts)

Usage:
    python scripts/prepare_manual_testing.py

Author: [Your Name]
Date: December 2024
Part of: FOSSEE Internship - Logical Error Classification Study
"""

import json
import csv
from pathlib import Path


def create_classification_prompt(record):
    """
    Create a formatted classification prompt for a single record.
    
    Args:
        record (dict): Dataset record with buggy code and metadata
        
    Returns:
        str: Formatted prompt ready for LLM testing
    """
    
    # Safely extract fields with None handling
    problem_desc = record.get('problem_description') or 'N/A'
    buggy_code = record.get('buggy_code') or ''
    language = record.get('language', 'Unknown')
    exec_feedback = record.get('execution_feedback') or 'N/A'
    hint = record.get('hint') or 'N/A'
    
    # Truncate long fields for readability
    if len(problem_desc) > 500:
        problem_desc = problem_desc[:500] + "..."
    
    if len(exec_feedback) > 300:
        exec_feedback = exec_feedback[:300] + "..."
    
    # Build the prompt
    prompt = f"""You are an expert code analyzer specializing in logical errors.

TASK: Classify the PRIMARY logical error in the buggy code below.

LOGICAL ERROR CATEGORIES:
1. Loop Condition [LOOP_COND]: Incorrect loops in the for/while condition
2. Condition Branch [COND_BRANCH]: Incorrect expression in the if condition
3. Statement Integrity [STMT_INTEGRITY]: Statement lacks a part of logical structure
4. Output/Input Format [IO_FORMAT]: Incorrect cin/cout statement (or print/input in Python)
5. Variable Initialization [VAR_INIT]: Incorrect declaration or initialization of variables
6. Data Type [DATA_TYPE]: Incorrect data type
7. Computation [COMPUTATION]: Incorrect basic math symbols or calculations

PROBLEM DETAILS:

Problem Description:
{problem_desc}

Buggy Code ({language}):
```{language.lower()}
{buggy_code}

Execution Feedback:
{exec_feedback}

Hint (if any):
{hint}

INSTRUCTIONS:
1. Analyze the buggy code carefully
2. Identify the PRIMARY logical error
3. Classify it into ONE of the 7 categories above
4. Return ONLY the category code (e.g., LOOP_COND, COND_BRANCH, etc.)
5. Do not include any explanation or additional text

YOUR CLASSIFICATION (code only):"""
    
    return prompt


def prepare_manual_testing_200():
    """
    Prepare 200 samples for manual testing across 4 LLM platforms.
    
    Process:
        1. Load automated predictions (Qwen, Llama)
        2. Load original dataset records
        3. Create CSV with pre-filled automated predictions
        4. Generate formatted prompts for manual copy-paste testing
    
    Returns:
        None (creates output files)
    """
    
    # ========================================
    # LOAD DATA
    # ========================================
    
    # Load predictions from 200-sample automated run
    predictions_file = Path(__file__).parent.parent / 'outputs' / 'predictions' / 'predictions_200_final.json'
    
    print("Loading predictions...")
    with open(predictions_file, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    
    # Load original dataset records for full information
    sample_path = Path(__file__).parent.parent / 'data' / 'sample_1000.json'
    
    print("Loading original dataset...")
    with open(sample_path, 'r', encoding='utf-8') as f:
        all_data = {r['unified_id']: r for r in json.load(f)}
    
    print("="*80)
    print("📊 PREPARING MANUAL TESTING - 200 SAMPLES")
    print("="*80)
    print(f"\nTotal samples: {len(predictions)}")
    print(f"Same samples for all 6 models")
    print()
    
    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent.parent / 'outputs' / 'manual_testing'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # ========================================
    # CREATE CSV FILE FOR TRACKING
    # ========================================
    
    print("Creating CSV file...")
    csv_file = output_dir / 'manual_testing_200_samples.csv'
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header row
        writer.writerow([
            'Sample_#',           # Sequential number 1-200
            'Unified_ID',         # Unique identifier (e.g., YAK_033938)
            'Dataset',            # Source dataset (Yaksh, PyPal, etc.)
            'Language',           # Programming language
            'Problem',            # Problem description (truncated)
            'Buggy_Code',         # Buggy code (truncated)
            'Qwen_Auto',          # Qwen automated prediction
            'Llama_Auto',         # Llama automated prediction
            'Gemini_Manual',      # To be filled manually
            'ChatGPT_Manual',     # To be filled manually
            'Claude_Manual',      # To be filled manually
            'DeepSeek_Manual',    # To be filled manually
            'Ground_Truth',       # Final validated category (optional)
            'Notes'               # Any observations
        ])
        
        # Write data rows for each prediction
        for idx, pred in enumerate(predictions, 1):
            # Get corresponding record from original dataset
            unified_id = pred.get('unified_id')
            record = all_data.get(unified_id)
            
            if not record:
                print(f"⚠️  Warning: Record {unified_id} not found in dataset")
                continue
            
            # Safely handle None values and truncate long text
            problem_desc = record.get('problem_description') or ''
            problem = (problem_desc[:200] + "...") if len(problem_desc) > 200 else (problem_desc if problem_desc else 'N/A')
            
            buggy_code = record.get('buggy_code') or ''
            code = (buggy_code[:800] + "...") if len(buggy_code) > 800 else (buggy_code if buggy_code else 'N/A')
            
            # Extract predictions from nested structure
            qwen_pred = pred.get('qwen', {})
            if isinstance(qwen_pred, dict):
                qwen_result = qwen_pred.get('prediction', 'ERROR')
            else:
                qwen_result = qwen_pred or 'ERROR'
            
            llama_pred = pred.get('llama', {})
            if isinstance(llama_pred, dict):
                llama_result = llama_pred.get('prediction', 'ERROR')
            else:
                llama_result = llama_pred or 'ERROR'
            
            # Write row with automated predictions pre-filled
            writer.writerow([
                idx,                                    # Sample number
                unified_id,                             # ID
                pred.get('source_dataset', 'N/A'),     # Dataset
                pred.get('language', 'N/A'),           # Language
                problem,                                # Problem (truncated)
                code,                                   # Code (truncated)
                qwen_result,                            # Qwen prediction
                llama_result,                           # Llama prediction
                '',  # Gemini - to be filled manually
                '',  # ChatGPT - to be filled manually
                '',  # Claude - to be filled manually
                '',  # DeepSeek - to be filled manually
                '',  # Ground truth - optional validation
                ''   # Notes - any observations
            ])
    
    print(f"✅ CSV created: {csv_file}")
    print(f"   Contains: 200 rows with Qwen/Llama predictions pre-filled\n")
    
    # ========================================
    # CREATE PROMPTS TEXT FILE
    # ========================================
    
    print("Creating prompts file...")
    prompts_file = output_dir / 'prompts_200_samples.txt'
    
    with open(prompts_file, 'w', encoding='utf-8') as f:
        # Write header with platform URLs
        f.write("="*80 + "\n")
        f.write("MANUAL TESTING - 200 SAMPLES\n")
        f.write("="*80 + "\n\n")
        
        f.write("PLATFORMS:\n")
        f.write("  1. Gemini:   https://aistudio.google.com/app/prompts/new_chat\n")
        f.write("  2. ChatGPT:  https://chatgpt.com\n")
        f.write("  3. Claude:   https://claude.ai\n")
        f.write("  4. DeepSeek: https://chat.deepseek.com\n\n")
        
        f.write("="*80 + "\n\n")
        
        # Generate prompt for each sample
        for idx, pred in enumerate(predictions, 1):
            # Get corresponding record
            unified_id = pred.get('unified_id')
            record = all_data.get(unified_id)
            
            if not record:
                continue
            
            # Skip if buggy code is empty (just to be safe)
            buggy_code = record.get('buggy_code', '').strip()
            if not buggy_code:
                print(f"⚠️  Skipping Sample #{idx} ({unified_id}): Empty buggy code")
                continue
            
            # Write sample header
            f.write(f"{'='*80}\n")
            f.write(f"SAMPLE #{idx}/200: {unified_id}\n")
            f.write(f"{'='*80}\n\n")
            
            # Show automated predictions for reference
            qwen_pred = pred.get('qwen', {})
            if isinstance(qwen_pred, dict):
                qwen_result = qwen_pred.get('prediction', 'ERROR')
            else:
                qwen_result = qwen_pred or 'ERROR'
            
            llama_pred = pred.get('llama', {})
            if isinstance(llama_pred, dict):
                llama_result = llama_pred.get('prediction', 'ERROR')
            else:
                llama_result = llama_pred or 'ERROR'
            
            f.write(f"📊 Qwen: {qwen_result} | Llama: {llama_result}\n\n")
            f.write(f"{'─'*80}\n\n")
            
            # Generate classification prompt using helper function
            prompt = create_classification_prompt(record)
            
            f.write(prompt)
            f.write("\n\n")
    
    print(f"✅ Prompts file created: {prompts_file}")
    print(f"   Contains: Formatted prompts ready for copy-paste\n")
    
    # ========================================
    # FINAL INSTRUCTIONS
    # ========================================
    
    print("="*80)
    print("✨ READY FOR MANUAL TESTING")
    print("="*80)
    print(f"\n⏱️  Estimated time: ~20 hours total (1.5 min per sample × 4 platforms)")
    print(f"💡 Suggestion: Break into 10 sessions × 20 samples × 2 hours each")
    print(f"📂 Files in: {output_dir}")
    print()
    print("NEXT STEPS:")
    print("  1. Open CSV in Excel/Google Sheets")
    print("  2. Open prompts text file in editor")
    print("  3. Open 4 browser tabs (see URLs in prompts file)")
    print("  4. For each sample:")
    print("     - Copy prompt from text file")
    print("     - Paste into each platform")
    print("     - Record category code in CSV")
    print("  5. Save CSV frequently!")
    print("="*80)


if __name__ == "__main__":
    """
    Main entry point for manual testing preparation.
    
    Executes the preparation workflow and creates necessary files.
    """
    prepare_manual_testing_200()

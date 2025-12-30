# Dataset Documentation

## Overview

This directory contains the unified dataset of 148,746 buggy code submissions from 5 sources.

## Files (Not in Git - Too Large)

- `unified_dataset.json` - Full dataset (148K records)
- `sample_1000.json` - Random sample of 1000 records
- `test_200.json` - Test set for model evaluation

## Data Structure

Each record contains:
{
"unified_id": "YAK_033938",
"source_dataset": "Yaksh",
"language": "Python",
"buggy_code": "...",
"correct_code": "...",
"problem_description": "...",
"execution_feedback": "...",
"hint": "..."
}


## Field Descriptions

| Field | Type | Description | Coverage |
|-------|------|-------------|----------|
| unified_id | string | Unique identifier | 100% |
| source_dataset | string | Original dataset name | 100% |
| language | string | Programming language | 100% |
| buggy_code | string | Student's incorrect code | 100% |
| correct_code | string | Reference solution | varies |
| problem_description | string | Problem statement | 61.7% |
| execution_feedback | string | Test case results | 51.9% |
| hint | string | Debugging hints | 9.7% |

## Statistics

See `../scripts/dataset_statistics.py` for detailed statistics.

Quick stats:
- Total: 148,746 records
- Python: 77,214 (52%)
- C++: 64,558 (43%)
- C: 6,974 (5%)

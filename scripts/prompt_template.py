import json
from pathlib import Path

def load_taxonomy():
    """Load taxonomy categories"""
    config_path = Path(__file__).parent.parent / 'config' / 'taxonomy_categories.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_classification_prompt(record):
    """Create prompt for logical error classification"""
    
    taxonomy = load_taxonomy()
    
    # Build category list for prompt
    category_list = "\n".join([
        f"{cat['id']}. {cat['name']} [{cat['code']}]: {cat['description']}"
        for cat in taxonomy['categories']
    ])
    
    # Build prompt
    prompt = f"""You are an expert code analyzer specializing in logical errors.

TASK: Classify the PRIMARY logical error in the buggy code below.

LOGICAL ERROR CATEGORIES:
{category_list}

PROBLEM DETAILS:
"""
    
    # Add problem description if available
    if record.get('problem_description'):
        prompt += f"\nProblem Description:\n{record['problem_description']}\n"
    
    # Add buggy code
    prompt += f"\nBuggy Code ({record['language']}):\n``````\n"
    
    # Add execution feedback if available
    if record.get('execution_feedback'):
        prompt += f"\nExecution Feedback:\n{record['execution_feedback']}\n"
    
    # Add hint if available (PyPal only)
    if record.get('hint'):
        prompt += f"\nHint:\n{record['hint']}\n"
    
    # Instructions
    prompt += f"""
INSTRUCTIONS:
1. Analyze the buggy code carefully
2. Identify the PRIMARY logical error
3. Classify it into ONE of the 7 categories above
4. Return ONLY the category code (e.g., LOOP_COND, COND_BRANCH, etc.)
5. Do not include any explanation or additional text

YOUR CLASSIFICATION (code only):"""
    
    return prompt

def test_prompt():
    """Test prompt generation with a sample record"""
    
    # Create a test record
    test_record = {
        'unified_id': 'TEST_001',
        'source_dataset': 'Test',
        'language': 'Python',
        'problem_description': 'Given an integer, return True if it is even, else return False.',
        'buggy_code': 'def main(a):\n\tif a%2 == 0:\n\t\treturn False\n\treturn True',
        'execution_feedback': '7 test cases failed.',
        'hint': 'The return values are swapped.'
    }
    
    prompt = create_classification_prompt(test_record)
    
    print("="*80)
    print("SAMPLE PROMPT FOR MODEL:")
    print("="*80)
    print(prompt)
    print("="*80)
    print("\nExpected Answer: COND_BRANCH (inverted boolean logic)")
    print("="*80)

if __name__ == "__main__":
    test_prompt()

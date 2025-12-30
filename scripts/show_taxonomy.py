import json
from pathlib import Path

def display_taxonomy():
    """Display the error taxonomy from the paper"""
    config_path = Path(__file__).parent.parent / 'config' / 'taxonomy_categories.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        taxonomy = json.load(f)
    
    print("="*80)
    print("LOGICAL ERROR TAXONOMY")
    print(f"Version: {taxonomy['taxonomy_version']}")
    print(f"Reference: {taxonomy['paper_reference']}")
    print("="*80)
    print()
    
    for category in taxonomy['categories']:
        print(f"{category['id']}. {category['name']} [{category['code']}]")
        print(f"   Description: {category['description']}")
        print(f"   Examples:")
        for example in category['examples']:
            print(f"     • {example}")
        print()
    
    print("="*80)
    print(f"Total Categories: {len(taxonomy['categories'])}")
    print("="*80)
    print()
    print("MODEL INSTRUCTIONS:")
    print(taxonomy['instructions_for_models'])
    print("="*80)

if __name__ == "__main__":
    display_taxonomy()

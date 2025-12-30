import json
from pathlib import Path
import requests

def test_gemini():
    """Test Gemini API"""
    try:
        from google import genai
        
        config_path = Path(__file__).parent.parent / 'config' / 'api_keys.json'
        with open(config_path) as f:
            config = json.load(f)
        
        client = genai.Client(
            api_key=config['gemini']['api_key'],
            http_options={'api_version': 'v1'}
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents='Say "Gemini works!"'
        )
        print(f"✅ Gemini: {response.text}")
        return True
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print(f"✅ Gemini: API key valid (quota limit is normal)")
            return "quota"
        else:
            print(f"❌ Gemini failed: {error_msg[:300]}")
            return False

def test_huggingface():
    """Test Hugging Face Router API"""
    try:
        config_path = Path(__file__).parent.parent / 'config' / 'api_keys.json'
        with open(config_path) as f:
            config = json.load(f)
        
        # Try multiple models that are commonly available
        models_to_try = [
            "meta-llama/Llama-3.2-3B-Instruct",
            "Qwen/Qwen2.5-Coder-7B-Instruct", 
            "mistralai/Mistral-7B-Instruct-v0.3"
        ]
        
        API_URL = "https://router.huggingface.co/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['deepseek']['api_key']}",
            "Content-Type": "application/json"
        }
        
        for model in models_to_try:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Reply with: HF works"}],
                "max_tokens": 20
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"✅ Hugging Face ({model.split('/')[1][:20]}): {content[:40]}")
                return True
            elif response.status_code == 400:
                # Try next model
                continue
            else:
                print(f"⚠️ Status {response.status_code} for {model}")
        
        # If all models failed
        print(f"❌ Hugging Face: No available models found")
        print(f"   Last response: {response.text[:200]}")
        print(f"\n💡 This might mean you need to enable 'Inference Providers'")
        print(f"   Go to: https://huggingface.co/settings/tokens")
        print(f"   Make sure 'Make calls to Inference Providers' is checked")
        return False
            
    except Exception as e:
        print(f"❌ Hugging Face failed: {str(e)[:200]}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Testing API Connections...")
    print("="*60)
    print()
    
    print("Testing Gemini (v1 API)...")
    gemini_ok = test_gemini()
    print()
    
    print("Testing Hugging Face (Router API)...")
    hf_ok = test_huggingface()
    
    print("\n" + "="*60)
    
    both_working = (gemini_ok == "quota" or gemini_ok == True) and hf_ok
    
    if both_working:
        print("✅✅ SETUP COMPLETE!")
        print("\n✨ Step 2 Complete! Ready for Step 3: Define Error Taxonomy")
        print("\n📝 Note: Gemini quota will reset in ~1 hour")
    elif gemini_ok == "quota" and not hf_ok:
        print("✅ Gemini API key is valid!")
        print("⚠️ Hugging Face needs token permission fix")
        print("\n💡 Go to: https://huggingface.co/settings/tokens")
        print("   Enable: 'Make calls to Inference Providers'")
    elif hf_ok:
        print("✅ Hugging Face working!")
        print("⚠️ Gemini needs attention")
    else:
        print("❌ Both APIs need attention - see messages above")
    
    print("="*60)

"""Quick Ollama connection test"""
import requests

print("Testing Ollama connection...")

try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        print("✅ Ollama is connected!")
        data = response.json()
        models = data.get("models", [])
        print(f"✅ Available models: {len(models)}")
        for model in models:
            print(f"   • {model.get('name', 'unknown')}")
        
        # Test a simple generation
        print("\nTesting generation...")
        gen_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": "Say hello in one sentence",
                "stream": False
            },
            timeout=30
        )
        
        if gen_response.status_code == 200:
            result = gen_response.json()
            print(f"✅ Response: {result.get('response', 'No response')}")
        else:
            print(f"❌ Generation failed: {gen_response.status_code}")
    else:
        print(f"❌ Ollama not responding: {response.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTo fix:")
    print("1. Make sure Ollama is installed")
    print("2. Run: ollama serve")
    print("3. Or use: start_christa.bat")

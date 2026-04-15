"""
Comments AI Module - Local LLM Chat via Ollama
Supports: Streaming, conversation history, and configurable models.
"""

import requests
import json
import sys

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3"
SYSTEM_PROMPT = "You are a helpful AI assistant running locally. Keep responses concise."


def check_ollama_status():
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if resp.status_code == 200:
            return True, [m["name"] for m in resp.json().get("models", [])]
        return False, []
    except (requests.ConnectionError, requests.Timeout):
        return False, []


def chat(prompt, model=None, stream=True, history=None):
    if model is None:
        model = DEFAULT_MODEL
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model, "messages": messages, "stream": stream}

    try:
        if stream:
            resp = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, stream=True, timeout=120)
            resp.raise_for_status()
            full = ""
            print("\n🤖 ", end="", flush=True)
            for line in resp.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            token = data["message"]["content"]
                            print(token, end="", flush=True)
                            full += token
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue
            print()
            return full
        else:
            resp = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            text = data.get("message", {}).get("content", "")
            print(f"\n🤖 {text}")
            return text
    except requests.ConnectionError:
        print("\n[✗] Cannot connect to Ollama. Run: ollama serve")
        return None
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        return None


def run_chat():
    print("=" * 55)
    print("  💬 AI Chat — Powered by Local Ollama LLM")
    print("=" * 55)

    available, models = check_ollama_status()
    if not available:
        print("\n  [✗] Ollama is not running!")
        print("  Install: https://ollama.ai | Start: ollama serve")
        return

    print(f"  ✅ Connected | Models: {', '.join(models) if models else 'none'}")
    model = DEFAULT_MODEL
    if models and DEFAULT_MODEL not in " ".join(models):
        model = models[0] if models else DEFAULT_MODEL
    print(f"  🤖 Using: {model}")
    print(f"  Commands: /models, /clear, /exit")
    print("=" * 55)

    history = []
    while True:
        try:
            user_input = input("\n👤 You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            return
        if not user_input:
            continue
        if user_input.lower() in ("/exit", "/quit"):
            print("👋 Goodbye!")
            return
        if user_input.lower() == "/clear":
            history = []
            print("[✓] History cleared.")
            continue
        if user_input.lower() == "/models":
            _, m = check_ollama_status()
            print(f"Models: {', '.join(m)}")
            continue

        resp = chat(user_input, model=model, history=history)
        if resp:
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": resp})
            if len(history) > 20:
                history = history[-20:]


if __name__ == "__main__":
    run_chat()
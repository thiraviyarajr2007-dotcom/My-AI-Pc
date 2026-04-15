# 🎮 How to Use Christa AI - Quick Guide

## ✅ System is Running!

Your Christa AI is currently running in the background. Here's how to use it:

---

## 🚀 Quick Start

### Option 1: Use the Interactive Launcher (Currently Running)

The launcher is already running! You can interact with it by:

1. **Go to the terminal** where it's running
2. **Choose an option** (1-6)
3. **Follow the prompts**

### Option 2: Use Individual Modules

You can also use the modules directly in Python:

---

## 📝 Example 1: Text Commands

```python
from ai_brain import AIBrain

brain = AIBrain(use_sqlite=True)

# Process a command
result = brain.process_input("open chrome")
print(result['response'])

brain.close()
```

**Try these commands:**
- "open chrome"
- "find my documents"
- "take a screenshot"
- "what can you do?"
- "search for python files"

---

## 🎤 Example 2: Voice Commands (Offline!)

```python
from whisper_voice import HybridVoice
from ai_brain import AIBrain

voice = HybridVoice(prefer_offline=True)
brain = AIBrain(use_sqlite=True)

# Listen and process
print("Speak now...")
text = voice.listen(timeout=5)

if text:
    result = brain.process_input(text)
    print(f"You said: {text}")
    print(f"Response: {result['response']}")

brain.close()
```

---

## 📚 Example 3: Document Search

```python
from rag_system import RAGSystem

rag = RAGSystem()

# Add documents
rag.add_file("README.md")
rag.add_directory("./documents")

# Search
results = rag.search("How to install?", top_k=3)

for result in results:
    doc = result['document']
    print(f"Found: {doc['content'][:100]}...")
```

---

## 🎯 What Each Feature Does

### 1. Voice Command (Option 1)
- Uses **Whisper** for offline speech recognition
- Speaks to Christa and get responses
- Works without internet!

### 2. Text Command (Option 2)
- Type commands directly
- AI understands intent
- Executes actions

### 3. Search Documents (Option 3)
- Semantic search across your files
- AI-powered document understanding
- Find relevant information quickly

### 4. View Statistics (Option 4)
- See how many commands you've used
- Most used commands
- System analytics

### 5. System Status (Option 5)
- Check what's working
- See available features
- Verify offline capability

---

## 🔥 Cool Things to Try

### 1. Test Offline Voice Recognition
```bash
python whisper_voice.py
# Choose option 1 and speak!
```

### 2. Test Memory System
```bash
python memory_system.py
# See how it stores data
```

### 3. Test RAG System
```bash
python rag_system.py
# See document search in action
```

### 4. Run Full Test Suite
```bash
python test_free_stack.py
# Verify everything works
```

---

## 💡 Tips

### For Best Performance:
1. **Install Ollama** for better AI responses
   - Download: https://ollama.com
   - Run: `ollama pull llama3`

2. **Use Whisper for offline voice**
   - Already installed and working!
   - No internet needed

3. **Add your documents to RAG**
   ```python
   from rag_system import RAGSystem
   rag = RAGSystem()
   rag.add_directory("./your_documents")
   ```

---

## 🎮 Interactive Commands

When the launcher is running, try:

**Option 1 - Voice Command:**
- Say: "Hey Christa, open Chrome"
- Say: "Find my Python files"
- Say: "Take a screenshot"

**Option 2 - Text Command:**
- Type: "open notepad"
- Type: "search for documents"
- Type: "what can you do?"

**Option 3 - Search Documents:**
- Query: "How to install?"
- Query: "What is this project?"

---

## 📊 Check Your Stats

After using for a while:

```python
from ai_brain import AIBrain

brain = AIBrain(use_sqlite=True)

# Get statistics
stats = brain.get_statistics()
print(f"Total commands: {stats['total_commands']}")

# Get most used commands
most_used = brain.get_most_used_commands(limit=10)
for cmd in most_used:
    print(f"{cmd['command']}: {cmd['count']} times")

brain.close()
```

---

## 🐛 Troubleshooting

### Voice not working?
```bash
# Test microphone
python -c "import speech_recognition as sr; print('Mic OK' if sr.Microphone() else 'No mic')"
```

### Ollama not connected?
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama run llama3
```

### Need help?
```bash
# Run diagnostics
python test_free_stack.py
```

---

## 🎉 You're Ready!

Your Christa AI is:
- ✅ Running
- ✅ 100% FREE
- ✅ Offline capable
- ✅ Production ready

**Start using it now!** 🚀

---

## 📞 Quick Commands Reference

| Command | What it does |
|---------|-------------|
| `python start_free_christa.py` | Start interactive launcher |
| `python quick_test.py` | Quick feature test |
| `python test_free_stack.py` | Full system test |
| `python memory_system.py` | Test memory |
| `python whisper_voice.py` | Test voice |
| `python rag_system.py` | Test RAG |
| `python ai_brain.py` | Test AI brain |

---

**Enjoy your FREE AI assistant!** 🎊

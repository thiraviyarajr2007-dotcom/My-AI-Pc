# 🚀 Christa AI - Installation Guide

Complete step-by-step installation guide for Christa AI Advanced.

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10/11 (primary support), Linux/Mac (partial support)
- **RAM**: 8 GB minimum, 16 GB recommended
- **Storage**: 20 GB free space
- **Webcam**: Required for face/gesture features
- **Microphone**: Required for voice features
- **Internet**: Required for initial setup and Ollama

### Software Requirements
- Python 3.10 or higher
- Git (optional, for cloning)
- Ollama (for AI brain)

## 🔧 Step-by-Step Installation

### Step 1: Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: `python --version`

**Linux:**
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

**Mac:**
```bash
brew install python@3.10
```

### Step 2: Clone or Download Project

**Option A: Using Git**
```bash
git clone <your-repo-url>
cd christa-ai
```

**Option B: Manual Download**
1. Download ZIP file
2. Extract to desired location
3. Open terminal in that folder

### Step 3: Install Python Dependencies

**Basic Installation:**
```bash
pip install -r requirements.txt
```

**If you encounter errors, install individually:**

```bash
# Core dependencies
pip install requests pyautogui

# Voice dependencies
pip install SpeechRecognition pyttsx3

# Vision dependencies
pip install opencv-python mediapipe

# Advanced features
pip install schedule pyperclip psutil

# Windows-specific
pip install pywin32

# Optional: System tray
pip install pillow pystray
```

### Step 4: Install PyAudio (for voice)

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

### Step 5: Install Ollama (AI Brain)

**Windows/Mac:**
1. Go to https://ollama.com
2. Download installer
3. Run installer
4. Open terminal and run:
   ```bash
   ollama pull llama3
   ```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
```

**Verify Ollama:**
```bash
ollama list
# Should show llama3
```

### Step 6: Test Installation

**Check dependencies:**
```bash
python christa_launcher.py --check-deps
```

**Test basic system:**
```bash
python main.py
```

**Test AI brain:**
```bash
python ai_brain.py
```

**Test voice:**
```bash
python voice_ai.py
```

## 🎯 Quick Start After Installation

### Launch Advanced System

**Voice Mode (Recommended):**
```bash
python christa_launcher.py --mode voice
```
Then say "Hey Christa" to activate!

**Chat Mode:**
```bash
python christa_launcher.py --mode chat
```
Type your commands naturally.

**Interactive Menu:**
```bash
python christa_launcher.py
```
Choose from menu options.

## 🔧 Troubleshooting

### Issue: "No module named 'speech_recognition'"
**Solution:**
```bash
pip install SpeechRecognition
```

### Issue: "PyAudio not found"
**Solution (Windows):**
```bash
pip install pipwin
pipwin install pyaudio
```

**Solution (Linux):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Issue: "Ollama connection failed"
**Solution:**
1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```
2. In another terminal:
   ```bash
   ollama pull llama3
   ```
3. Test:
   ```bash
   ollama run llama3
   ```

### Issue: "Microphone not detected"
**Solution:**
1. Check microphone is connected
2. Check system permissions
3. Test with:
   ```bash
   python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
   ```

### Issue: "Camera not working"
**Solution:**
1. Check camera permissions
2. Close other apps using camera
3. Test with:
   ```bash
   python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
   ```

### Issue: "Import error: win32gui"
**Solution (Windows only):**
```bash
pip install pywin32
```

### Issue: "pyttsx3 not speaking"
**Solution:**
```bash
pip uninstall pyttsx3
pip install pyttsx3==2.90
```

## 📦 Optional Dependencies

### For Enhanced Features

**Whisper (Better offline speech recognition):**
```bash
pip install openai-whisper
```

**Face Recognition:**
```bash
# Requires cmake and dlib (advanced)
pip install face_recognition
```

**LangChain (Advanced AI features):**
```bash
pip install langchain chromadb
```

**Image Processing:**
```bash
pip install pillow
```

## 🧪 Verify Everything Works

Run this test script:

```bash
# Test 1: Check Python version
python --version

# Test 2: Check dependencies
python christa_launcher.py --check-deps

# Test 3: Test AI brain
python ai_brain.py
# Type: "open chrome" and press Enter

# Test 4: Test voice (if microphone available)
python voice_ai.py
# Say: "open calculator"

# Test 5: Test Ollama
python comments_ai.py
# Type: "hello"

# Test 6: Launch full system
python christa_launcher.py --mode chat
# Type: "what can you do?"
```

## ✅ Installation Complete!

If all tests pass, you're ready to use Christa AI!

### Next Steps:

1. **Read the README:**
   ```bash
   cat README_ADVANCED.md
   ```

2. **Try voice mode:**
   ```bash
   python christa_launcher.py --mode voice
   ```

3. **Explore features:**
   - Say "Hey Christa, what can you do?"
   - Try "Hey Christa, open Chrome"
   - Try "Hey Christa, take a screenshot"

4. **Create workflows:**
   ```bash
   python christa_launcher.py --mode workflow
   ```

5. **Monitor context:**
   ```bash
   python christa_launcher.py --mode context
   ```

## 🆘 Still Having Issues?

1. Check `README_ADVANCED.md` for detailed documentation
2. Check `ADVANCED_ROADMAP.md` for feature status
3. Verify all prerequisites are met
4. Try reinstalling dependencies:
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

## 🎉 Enjoy Christa AI!

You now have a fully functional AI assistant with:
- ✅ Voice control with wake word
- ✅ Natural language understanding
- ✅ Context awareness
- ✅ Proactive assistance
- ✅ Workflow automation
- ✅ And much more!

Say "Hey Christa" and start exploring! 🚀

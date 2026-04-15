# 🚀 Get Started with Christa AI

Welcome! This guide will get you up and running in minutes.

## ⚡ Super Quick Start (Easiest)

### Windows Users
1. Double-click `start_christa.bat`
2. Follow the prompts
3. Done! 🎉

### All Platforms
```bash
python quick_start.py
```

The script will:
- ✅ Check your Python version
- ✅ Check dependencies
- ✅ Offer to install missing packages
- ✅ Check Ollama status
- ✅ Recommend best mode for your system
- ✅ Launch Christa AI

## 📋 What You Need

### Minimum Requirements
- Python 3.10+
- Microphone (for voice features)
- 8 GB RAM
- Windows 10/11 (primary support)

### Recommended
- Ollama installed (for AI brain)
- 16 GB RAM
- Webcam (for face/gesture features)

## 🎯 Choose Your Experience

### 🎤 Voice Mode (Recommended)
**Best for**: Hands-free control, natural interaction

**Requirements**: Microphone + Ollama

**Launch**:
```bash
python christa_launcher.py --mode voice
```

**Usage**:
1. Say "Hey Christa" to activate
2. Give your command naturally
3. AI understands and executes
4. Responds with voice

**Examples**:
- "Hey Christa, open Chrome"
- "Hey Christa, take a screenshot"
- "Hey Christa, find my documents"

---

### 💬 Chat Mode
**Best for**: Text-based interaction, quiet environments

**Requirements**: Ollama (microphone optional)

**Launch**:
```bash
python christa_launcher.py --mode chat
```

**Usage**:
1. Type your command
2. Press Enter
3. AI responds and executes

**Examples**:
```
You > open chrome
Christa: Opening Chrome...

You > what can you do?
Christa: I can open apps, search files, control your mouse...
```

---

### 📋 Basic Mode
**Best for**: Original features, no Ollama needed

**Requirements**: Just Python + dependencies

**Launch**:
```bash
python main.py
```

**Usage**:
- Menu-driven interface
- Select module to launch
- Original Christa AI features

---

### 🔄 Workflow Mode
**Best for**: Automating repetitive tasks

**Launch**:
```bash
python christa_launcher.py --mode workflow
```

**Usage**:
1. Record actions: `record morning_routine`
2. Perform actions (they're recorded)
3. Stop: `stop`
4. Execute: `execute morning_routine`
5. Schedule: `schedule morning_routine 09:00`

---

### 👁️ Context Mode
**Best for**: Understanding your work patterns

**Launch**:
```bash
python christa_launcher.py --mode context
```

**Usage**:
- Monitors your activity
- Tracks app usage
- Learns patterns
- Press Ctrl+C to see summary

---

### 🖼️ System Tray
**Best for**: Always-accessible quick actions

**Launch**:
```bash
python christa_launcher.py --mode tray
```

**Usage**:
- Icon appears in system tray
- Right-click for menu
- Quick actions available
- Runs in background

## 🎓 First-Time Setup

### Step 1: Install Python
Download from https://www.python.org/downloads/
- ✅ Check "Add Python to PATH"
- Install version 3.10 or higher

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Ollama (Optional but Recommended)
1. Go to https://ollama.com
2. Download and install
3. Run: `ollama pull llama3`

### Step 4: Test Installation
```bash
python quick_start.py
```

## 🎯 What to Try First

### Beginner Path
1. **Start with Chat Mode**
   ```bash
   python christa_launcher.py --mode chat
   ```

2. **Try basic commands**:
   - "open calculator"
   - "what can you do?"
   - "take a screenshot"

3. **Explore features**:
   - Ask questions
   - Open applications
   - Search files

### Intermediate Path
1. **Enable Voice Mode**
   ```bash
   python christa_launcher.py --mode voice
   ```

2. **Use wake word**:
   - Say "Hey Christa"
   - Give voice commands
   - Hear AI responses

3. **Create workflows**:
   - Record common tasks
   - Schedule automations
   - Save time daily

### Advanced Path
1. **Monitor context**:
   - Track your patterns
   - Get insights
   - Optimize workflow

2. **Customize settings**:
   - Adjust voice rate
   - Change wake word
   - Configure notifications

3. **Integrate everything**:
   - Use system tray
   - Combine features
   - Build custom workflows

## 💡 Pro Tips

### Voice Control Tips
- Speak clearly and naturally
- Wait for "I'm listening..." before speaking
- Say "exit" or "stop" to quit
- Adjust microphone if not detecting

### Chat Mode Tips
- Type naturally, no rigid syntax needed
- Ask "what can you do?" to see capabilities
- Use "exit" or "quit" to close
- Context is remembered during session

### Workflow Tips
- Record your morning routine
- Schedule end-of-day cleanup
- Create shortcuts for common tasks
- Test workflows before scheduling

### Performance Tips
- Close unused modules
- Use chat mode if voice not needed
- Schedule heavy tasks for off-hours
- Monitor resource usage

## 🔧 Quick Troubleshooting

### "Python not found"
- Install Python 3.10+
- Make sure "Add to PATH" was checked
- Restart terminal after installation

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Microphone not working"
- Check system permissions
- Test with: `python voice_ai.py`
- Adjust energy threshold if needed

### "Ollama not connecting"
```bash
ollama serve
ollama pull llama3
```

### "PyAudio error"
**Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux**:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## 📚 Learn More

- **Full Documentation**: `README_ADVANCED.md`
- **Installation Guide**: `INSTALLATION_GUIDE.md`
- **Feature Roadmap**: `ADVANCED_ROADMAP.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

## 🎯 Common Use Cases

### Morning Routine
```bash
# Record once
python christa_launcher.py --mode workflow
> record morning_routine

# Then perform:
# - Open email
# - Open calendar
# - Open Spotify
# - Open work apps

> stop

# Schedule for 9 AM daily
> schedule morning_routine 09:00
```

### Voice Assistant
```bash
python christa_launcher.py --mode voice

# Then say:
"Hey Christa, open Chrome"
"Hey Christa, take a screenshot"
"Hey Christa, find my reports"
"Hey Christa, what's the time?"
```

### File Organization
```bash
python christa_launcher.py --mode chat

# Then type:
"organize my downloads"
"find files modified today"
"search for report.pdf"
```

### Productivity Tracking
```bash
python christa_launcher.py --mode context

# Let it run while you work
# Press Ctrl+C to see:
# - Most used apps
# - Time spent per app
# - Activity patterns
# - Suggestions
```

## 🎉 You're Ready!

Choose your path:

**Quick & Easy**:
```bash
python quick_start.py
```

**Voice Control**:
```bash
python christa_launcher.py --mode voice
```

**Text Chat**:
```bash
python christa_launcher.py --mode chat
```

**Explore All**:
```bash
python christa_launcher.py
```

## 🆘 Need Help?

1. Check `INSTALLATION_GUIDE.md` for detailed setup
2. Read `README_ADVANCED.md` for all features
3. Run `python christa_launcher.py --check-deps` to verify setup
4. Try `python quick_start.py` for guided setup

## 🚀 Have Fun!

Christa AI is your intelligent copilot. Explore, experiment, and enjoy!

Say "Hey Christa" and start your journey! 🎤✨

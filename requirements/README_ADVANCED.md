# 🤖 Christa AI - Advanced Personal Assistant

Your intelligent laptop copilot with voice control, context awareness, and proactive assistance.

## ✨ Features

### 🎤 Voice Control
- **Wake Word Detection**: Say "Hey Christa" to activate
- **Natural Language Understanding**: No rigid commands needed
- **Voice Feedback**: AI responds with speech
- **Continuous Listening**: Always ready to help

### 🧠 AI Intelligence
- **Unified AI Brain**: Powered by Ollama LLM
- **Context Memory**: Remembers your conversations
- **Intent Classification**: Understands what you want
- **Multi-step Planning**: Handles complex requests

### 👁️ Context Awareness
- **Active Window Tracking**: Knows what you're working on
- **Clipboard Monitoring**: Smart paste suggestions
- **Activity Patterns**: Learns your habits
- **Usage Analytics**: Track app usage time

### 🤖 Proactive Assistance
- **Smart Notifications**: Timely reminders and suggestions
- **Break Reminders**: Health-conscious assistance
- **Battery Monitoring**: Low battery warnings
- **Auto-Organization**: Organize downloads automatically

### 🔄 Workflow Automation
- **Record & Replay**: Record actions and replay them
- **Scheduled Tasks**: Run workflows at specific times
- **Visual Builder**: Create automation workflows
- **Multi-step Actions**: Complex task automation

### 🖼️ System Integration
- **System Tray Icon**: Always accessible
- **Quick Actions**: Screenshot, search, control
- **Dashboard**: Activity insights and stats
- **Cross-module Integration**: All features work together

### 📋 Original Features (Still Available)
- Voice commands
- Gesture control
- Face recognition
- File search
- Screen automation
- PC control
- AI chat

## 🚀 Quick Start

### Installation

1. **Install Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama (for AI brain)**
   - Download from: https://ollama.com
   - Install and run: `ollama run llama3`

4. **Optional: Install pyttsx3 for voice feedback**
   ```bash
   pip install pyttsx3
   ```

### Launch

**Simple Launch:**
```bash
python christa_launcher.py
```

**Direct Launch Modes:**
```bash
# Advanced voice mode with wake word
python christa_launcher.py --mode voice

# Text-based chat mode
python christa_launcher.py --mode chat

# Workflow builder
python christa_launcher.py --mode workflow

# Context monitor
python christa_launcher.py --mode context

# System tray
python christa_launcher.py --mode tray

# AI brain test
python christa_launcher.py --mode brain

# Check dependencies
python christa_launcher.py --check-deps
```

## 📖 Usage Guide

### Voice Mode

1. Launch voice mode:
   ```bash
   python christa_launcher.py --mode voice
   ```

2. Say "Hey Christa" to activate

3. Give your command naturally:
   - "Open Chrome"
   - "Find my documents"
   - "Take a screenshot"
   - "What can you do?"

### Chat Mode

1. Launch chat mode:
   ```bash
   python christa_launcher.py --mode chat
   ```

2. Type your commands naturally

3. The AI will understand and execute

### Workflow Automation

1. Launch workflow builder:
   ```bash
   python christa_launcher.py --mode workflow
   ```

2. Record a workflow:
   ```
   record morning_routine
   ```

3. Perform actions (they'll be recorded)

4. Stop recording:
   ```
   stop
   ```

5. Execute workflow:
   ```
   execute morning_routine
   ```

### Context Monitoring

1. Launch context monitor:
   ```bash
   python christa_launcher.py --mode context
   ```

2. It will track:
   - Active applications
   - Usage time
   - Clipboard history
   - Activity patterns

3. Press Ctrl+C to see summary

## 🏗️ Architecture

```
Christa AI Advanced
│
├── Core Intelligence
│   ├── ai_brain.py              # Unified AI decision engine
│   ├── wake_word_detector.py    # "Hey Christa" detection
│   └── voice_feedback.py        # Text-to-speech responses
│
├── Context & Awareness
│   ├── context_awareness.py     # Activity tracking
│   └── proactive_assistant.py   # Smart notifications
│
├── Automation
│   └── workflow_automation.py   # Record & replay workflows
│
├── Interface
│   ├── christa_advanced.py      # Integrated system
│   ├── christa_launcher.py      # Main launcher
│   └── system_tray.py           # System tray icon
│
└── Original Modules
    ├── voice_ai.py              # Voice commands
    ├── control_ai.py            # PC control
    ├── aiscreencontrol_ai.py    # Screen automation
    ├── gesture_ai.py            # Hand gestures
    ├── facereg_ai.py            # Face recognition
    ├── filesearch_ai.py         # File search
    └── comments_ai.py           # Ollama chat
```

## 🎯 Command Examples

### Natural Language Commands

```
"Hey Christa, open Chrome"
"Find files containing 'report'"
"Take a screenshot"
"What's the weather?" (requires web search)
"Open my documents folder"
"Lock the screen"
"What can you do?"
"Remember this: meeting at 3pm"
"What did I ask you earlier?"
```

### Workflow Commands

```
record morning_routine
record end_of_day
execute morning_routine
list
schedule morning_routine 09:00
```

### Context Commands

```
"What am I working on?"
"Show my most used apps"
"What's in my clipboard?"
"Organize my downloads"
```

## ⚙️ Configuration

### Voice Settings

Edit in `voice_feedback.py`:
```python
VoiceFeedback(
    rate=175,           # Speech rate (words per minute)
    volume=0.9,         # Volume (0.0 to 1.0)
    voice_gender="female"  # "male" or "female"
)
```

### Wake Word

Edit in `wake_word_detector.py`:
```python
wake_words = ["hey christa", "christa", "hey crystal"]
```

### Context Monitoring

Edit in `context_awareness.py`:
```python
ContextAwarenessSystem(
    update_interval=2.0  # Check every 2 seconds
)
```

## 🔧 Troubleshooting

### Microphone Not Working

1. Check microphone permissions
2. Test with: `python voice_ai.py`
3. Adjust energy threshold in code

### Ollama Not Connecting

1. Make sure Ollama is running: `ollama serve`
2. Check if model is downloaded: `ollama list`
3. Pull model if needed: `ollama pull llama3`

### PyAudio Installation Issues

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

### System Tray Not Working

Install required packages:
```bash
pip install pillow pystray
```

## 📊 Performance

- **CPU Usage (Idle)**: < 5%
- **CPU Usage (Active)**: 10-20%
- **RAM Usage**: 100-200 MB
- **Voice Response Time**: < 500ms
- **Wake Word Detection**: Real-time

## 🔒 Privacy & Security

- **Local-First**: All processing happens on your machine
- **No Cloud**: Works completely offline (except Ollama if using cloud models)
- **Data Storage**: All data stored locally
- **Microphone**: Only active when listening
- **Camera**: Only active when using face/gesture features

## 🛣️ Roadmap

### ✅ Completed (Phase 1-2)
- [x] Unified AI brain with Ollama
- [x] Wake word detection ("Hey Christa")
- [x] Voice feedback (text-to-speech)
- [x] Context awareness system
- [x] Proactive assistance
- [x] Workflow automation
- [x] System tray icon
- [x] Natural language understanding
- [x] Context memory

### 🚧 In Progress (Phase 3)
- [ ] Computer vision for UI detection
- [ ] Advanced gesture controls
- [ ] Enhanced file management
- [ ] Multi-monitor support

### 📅 Planned (Phase 4+)
- [ ] Calendar integration
- [ ] Email automation
- [ ] Browser automation
- [ ] Mobile companion app
- [ ] Multi-device sync
- [ ] Plugin system

See `ADVANCED_ROADMAP.md` for complete roadmap.

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

## 📝 License

Personal use only. Not for commercial distribution.

## 🙏 Acknowledgments

- **Ollama**: Local LLM inference
- **MediaPipe**: Hand gesture recognition
- **OpenCV**: Computer vision
- **SpeechRecognition**: Voice input
- **pyttsx3**: Text-to-speech

## 📞 Support

For issues or questions, check:
1. This README
2. `ADVANCED_ROADMAP.md` for features
3. Individual module files for documentation

## 🎓 Learning Resources

- **Ollama**: https://ollama.com
- **MediaPipe**: https://mediapipe.dev
- **OpenCV**: https://opencv.org
- **Python Speech Recognition**: https://pypi.org/project/SpeechRecognition/

---

**Made with ❤️ for personal productivity**

*Christa AI - Your intelligent copilot that understands, learns, and assists proactively.*

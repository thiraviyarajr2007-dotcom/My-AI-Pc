# 🚀 Quick Start Guide - Christa AI Web UI

## Start the UI in 3 Steps:

### Step 1: Start Ollama (if not running)
```bash
ollama serve
```
Leave this terminal open.

### Step 2: Start Christa UI
Open a new terminal and run:
```bash
python christa_ui.py
```

### Step 3: Open Browser
Go to: **http://localhost:5000**

---

## 🎨 What You'll See

### Oracle-Style Interface with:
- **Blue theme** (#005FB8) - Your primary color
- **Clean sidebar** - System status and stats
- **Modern chat** - Centered, professional layout
- **Voice button** - Click to speak
- **Real-time updates** - Live statistics

---

## ✨ Quick Test

1. **Type a message**: "hello" → Press Enter
2. **Try voice**: Click 🎤 → Say "what can you do?"
3. **Use suggestions**: Click any suggestion card
4. **Check stats**: See command count in sidebar

---

## 🎯 Features to Try

### Text Commands:
- "open chrome"
- "what can you do?"
- "take a screenshot"
- "find my documents"

### Voice Commands:
- Click microphone
- Speak clearly
- Wait for response

### UI Features:
- Clear chat button
- Refresh stats button
- System status indicators
- Confidence badges

---

## 📱 Mobile Friendly

The UI is responsive! Try it on:
- Desktop (best experience)
- Tablet
- Mobile phone

---

## 🔧 Troubleshooting

### Port already in use?
```bash
# Kill the process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Voice not working?
- Allow microphone in browser
- Check Whisper model loaded
- Try text input first

### Stats showing 0?
- Send a few commands first
- Click refresh button
- Check AI Brain initialized

---

**Ready to go! Start the server and enjoy your new UI! 🎉**

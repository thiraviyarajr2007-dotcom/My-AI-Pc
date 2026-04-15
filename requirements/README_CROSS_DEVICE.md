# 🌐 Christa AI - Cross-Device Control System

Transform your laptop into a central AI hub that can be controlled from any device - phone, watch, TV, or tablet.

## 🎯 What Is This?

Christa AI Cross-Device System allows you to:
- 📱 Control your laptop from your phone
- ⌚ Execute commands from your smartwatch
- 📺 Integrate with your Smart TV
- 🌐 Access from anywhere with internet
- 🔐 Secure device authentication
- ⚡ Real-time communication

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install flask flask-cors flask-socketio python-socketio
```

### Step 2: Start API Server
```bash
python api_server.py
```

You'll see:
```
🌐 Christa AI - API Server
Server starting on http://0.0.0.0:5000
```

### Step 3: Find Your Laptop IP
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

Look for something like `192.168.1.100`

### Step 4: Test from Another Device

**Option A: Use Python Client (Testing)**
```bash
python mobile_client.py
```

**Option B: Use curl (Quick Test)**
```bash
# Register device
curl -X POST http://YOUR_LAPTOP_IP:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"device_id":"test_device","device_info":{"type":"test"}}'

# Execute command (use API key from registration)
curl -X POST http://YOUR_LAPTOP_IP:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"device_id":"test_device","api_key":"YOUR_API_KEY","command":"open chrome"}'
```

## 📱 Build Mobile App

### Flutter (Recommended)

1. **Create project**:
   ```bash
   flutter create christa_mobile
   cd christa_mobile
   ```

2. **Add dependencies** to `pubspec.yaml`:
   ```yaml
   dependencies:
     http: ^1.1.0
     socket_io_client: ^2.0.3+1
     speech_to_text: ^6.5.1
   ```

3. **Copy code** from `mobile_app/README.md`

4. **Update server URL**:
   ```dart
   ApiService(baseUrl: 'http://YOUR_LAPTOP_IP:5000')
   ```

5. **Run**:
   ```bash
   flutter run
   ```

### React Native

```javascript
// ChristaAPI.js
const API_URL = 'http://YOUR_LAPTOP_IP:5000';

export async function registerDevice(deviceId, deviceInfo) {
  const response = await fetch(`${API_URL}/api/register`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({device_id: deviceId, device_info: deviceInfo})
  });
  return response.json();
}

export async function executeCommand(deviceId, apiKey, command) {
  const response = await fetch(`${API_URL}/api/command`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({device_id: deviceId, api_key: apiKey, command})
  });
  return response.json();
}
```

## ⌚ Smartwatch Integration

### Wear OS (Kotlin)

```kotlin
class ChristaApiService(private val baseUrl: String) {
    suspend fun executeCommand(command: String) {
        val json = JSONObject().apply {
            put("device_id", "my_watch")
            put("api_key", apiKey)
            put("command", command)
        }
        
        val request = Request.Builder()
            .url("$baseUrl/api/command")
            .post(json.toString().toRequestBody())
            .build()
        
        client.newCall(request).execute()
    }
}

// In your composable
Button(onClick = { 
    scope.launch { 
        apiService.executeCommand("open chrome") 
    }
}) {
    Text("Chrome")
}
```

### Apple Watch (Swift)

```swift
class ChristaAPI: ObservableObject {
    func executeCommand(_ command: String) async {
        let url = URL(string: "\(baseURL)/api/command")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let body: [String: Any] = [
            "device_id": "my_watch",
            "api_key": apiKey,
            "command": command
        ]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        let (_, _) = try? await URLSession.shared.data(for: request)
    }
}

// In your view
Button("Chrome") {
    Task { await api.executeCommand("open chrome") }
}
```

## 📺 Smart TV Integration

### Android TV

```kotlin
class TVActivity : Activity() {
    private val apiService = ChristaApiService("http://YOUR_LAPTOP_IP:5000")
    
    fun openYouTube(view: View) {
        lifecycleScope.launch {
            apiService.executeCommand("play youtube on tv")
        }
        
        // Open YouTube on TV
        val intent = Intent(Intent.ACTION_VIEW).apply {
            data = Uri.parse("https://www.youtube.com")
        }
        startActivity(intent)
    }
}
```

## 🔐 Security Setup

### 1. Device Registration

Every device must register first:

```python
# Python example
client = ChristaClient(server_url="http://laptop:5000")
client.register({
    "type": "mobile",
    "name": "My Phone",
    "platform": "Android"
})
# Returns API key - store securely!
```

### 2. Secure Storage

**Android:**
```kotlin
val encryptedPrefs = EncryptedSharedPreferences.create(...)
encryptedPrefs.edit().putString("api_key", apiKey).apply()
```

**iOS:**
```swift
let keychain = KeychainSwift()
keychain.set(apiKey, forKey: "christa_api_key")
```

### 3. Firewall Configuration

**Windows:**
```cmd
netsh advfirewall firewall add rule name="Christa AI" dir=in action=allow protocol=TCP localport=5000
```

**Linux:**
```bash
sudo ufw allow 5000/tcp
```

## 🌐 Remote Access (Optional)

### Option 1: VPN (Recommended)
1. Set up VPN on laptop (WireGuard, OpenVPN)
2. Connect devices to VPN
3. Use laptop's VPN IP

### Option 2: Port Forwarding
1. Configure router to forward port 5000
2. Use dynamic DNS (No-IP, DuckDNS)
3. Access via public URL

**⚠️ Security Warning:** Always use HTTPS and strong authentication for remote access!

## 📡 Real-Time Communication

### WebSocket Example

```javascript
import io from 'socket.io-client';

const socket = io('http://YOUR_LAPTOP_IP:5000');

socket.on('connect', () => {
    socket.emit('register', {
        device_id: 'my_phone',
        device_info: {type: 'mobile'}
    });
});

socket.on('command_executed', (data) => {
    console.log('Command executed:', data);
    // Update UI
});

// Send command
socket.emit('command', {
    device_id: 'my_phone',
    api_key: 'YOUR_API_KEY',
    command: 'open chrome'
});
```

## 🎯 Use Cases

### Morning Routine
```
Watch: Tap "Morning"
→ Laptop: Opens email, calendar, Spotify
→ TV: Shows news
→ Phone: Displays weather
```

### Movie Time
```
Phone: "Hey Christa, movie time"
→ Laptop: Dims lights (if smart home)
→ TV: Opens Netflix
→ Phone: DND mode
```

### Work Mode
```
Any device: "Start work mode"
→ Laptop: Opens VS Code, Slack
→ Watch: Work notifications only
→ TV: Turns off
```

### Remote Control
```
From anywhere:
→ Take screenshot
→ Search files
→ Lock/shutdown
→ Check status
```

## 📊 API Reference

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register` | POST | Register new device |
| `/api/command` | POST | Execute command |
| `/api/status` | GET | Get system status |
| `/api/history` | GET | Get command history |
| `/api/screenshot` | POST | Take screenshot |
| `/api/devices` | GET | List devices (admin) |

### Request Examples

**Register:**
```json
POST /api/register
{
  "device_id": "my_phone",
  "device_info": {
    "type": "mobile",
    "name": "My Android Phone",
    "platform": "Android 13"
  }
}
```

**Execute Command:**
```json
POST /api/command
{
  "device_id": "my_phone",
  "api_key": "your_api_key_here",
  "command": "open chrome"
}
```

**Response:**
```json
{
  "success": true,
  "intent": "open_app",
  "confidence": 0.9,
  "response": "Opening Chrome...",
  "action": {
    "module": "control_ai",
    "function": "open_app",
    "params": {"app_name": "chrome"}
  }
}
```

## 🔧 Troubleshooting

### Can't Connect to Server

1. **Check server is running:**
   ```bash
   curl http://localhost:5000/api/status
   ```

2. **Check firewall:**
   ```bash
   # Windows
   netsh advfirewall show allprofiles
   
   # Linux
   sudo ufw status
   ```

3. **Check network:**
   ```bash
   ping YOUR_LAPTOP_IP
   ```

### Commands Not Executing

1. **Verify registration:**
   - Check API key is stored
   - Re-register if needed

2. **Check server logs:**
   - Look for errors in terminal
   - Verify AI modules loaded

3. **Test with Python client:**
   ```bash
   python mobile_client.py
   ```

### Slow Response

1. **Use WebSocket** instead of REST
2. **Check network latency**
3. **Optimize laptop performance**
4. **Reduce polling frequency**

## 📚 Documentation

- **API Server**: `api_server.py` - Complete server code
- **Mobile Client**: `mobile_client.py` - Python client library
- **Flutter Guide**: `mobile_app/README.md` - Mobile app guide
- **Complete Guide**: `CROSS_DEVICE_GUIDE.md` - All integrations
- **Summary**: `CROSS_DEVICE_SUMMARY.md` - Overview

## 🎓 Learning Path

### Beginner
1. Start API server
2. Test with Python client
3. Try curl commands
4. Understand REST API

### Intermediate
1. Build simple mobile app
2. Implement device registration
3. Add quick action buttons
4. Test on real device

### Advanced
1. Add WebSocket support
2. Implement push notifications
3. Create watch app
4. Set up TV integration
5. Add cloud sync

## 💡 Pro Tips

1. **Use WebSocket** for real-time updates
2. **Cache API key** securely
3. **Implement retry logic** for failed commands
4. **Add offline queue** for commands
5. **Use voice input** for natural control
6. **Create widgets** for quick access
7. **Enable notifications** for feedback
8. **Log all commands** for debugging

## 🚀 Next Steps

1. **Test the system**:
   ```bash
   python api_server.py
   python mobile_client.py
   ```

2. **Build mobile app**:
   - Follow `mobile_app/README.md`
   - Test on real device

3. **Add more devices**:
   - Create watch app
   - Integrate with TV
   - Add tablet support

4. **Enhance features**:
   - Add file transfer
   - Implement screen streaming
   - Create automation rules

## 🎉 Success!

You now have:
- ✅ API server running
- ✅ Device authentication
- ✅ Command execution
- ✅ Real-time communication
- ✅ Multi-device support
- ✅ Secure connections

**Your laptop is now a central AI hub accessible from any device!** 🌐

---

**Questions?** Check the documentation files or test with the Python client first.

**Made with ❤️ for seamless cross-device control**

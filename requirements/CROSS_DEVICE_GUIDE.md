## 🌐 Christa AI - Cross-Device System Guide

Complete guide for connecting mobile, watch, TV, and other devices to Christa AI.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Christa AI Ecosystem                  │
└─────────────────────────────────────────────────────────┘

         📱 Mobile          ⌚ Watch          📺 TV
            │                 │                │
            └─────────────────┼────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   API Server      │
                    │  (Flask + Socket) │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │   AI Brain        │
                    │   (Ollama LLM)    │
                    └─────────┬─────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
      ┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐
      │  Control  │    │  Screen   │    │   File    │
      │    AI     │    │  Control  │    │  Search   │
      └───────────┘    └───────────┘    └───────────┘
```

## 🚀 Quick Start

### 1. Start the API Server (Laptop)

```bash
# Install dependencies
pip install flask flask-cors flask-socketio python-socketio

# Start server
python api_server.py

# Server will run on http://0.0.0.0:5000
```

### 2. Find Your Laptop IP

**Windows:**
```cmd
ipconfig
# Look for IPv4 Address
```

**Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```

### 3. Connect Devices

All devices must be on the same network as your laptop.

---

## 📱 Mobile App Integration

### Option 1: Python Client (Testing)

```bash
python mobile_client.py
```

### Option 2: Flutter App (Production)

See `mobile_app/README.md` for complete Flutter implementation.

**Quick Setup:**
```bash
cd mobile_app
flutter create christa_mobile
# Copy code from README
flutter run
```

**Key Features:**
- Voice commands from phone
- Quick action buttons
- Command history
- Real-time notifications
- File browser

---

## ⌚ Smartwatch Integration

### Wear OS (Android Watch)

#### 1. Create Wear OS App

```kotlin
// MainActivity.kt
class MainActivity : ComponentActivity() {
    private val apiService = ChristaApiService("http://YOUR_LAPTOP_IP:5000")
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            ChristaWatchApp(apiService)
        }
    }
}

@Composable
fun ChristaWatchApp(apiService: ChristaApiService) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Quick action buttons
        Button(onClick = { apiService.executeCommand("open chrome") }) {
            Text("Chrome")
        }
        
        Button(onClick = { apiService.executeCommand("lock screen") }) {
            Text("Lock")
        }
        
        Button(onClick = { apiService.executeCommand("shutdown") }) {
            Text("Shutdown")
        }
    }
}
```

#### 2. API Service for Watch

```kotlin
// ChristaApiService.kt
class ChristaApiService(private val baseUrl: String) {
    private val client = OkHttpClient()
    private var deviceId = "my_watch"
    private var apiKey: String? = null
    
    suspend fun register() {
        val json = JSONObject().apply {
            put("device_id", deviceId)
            put("device_info", JSONObject().apply {
                put("type", "watch")
                put("name", "My Watch")
            })
        }
        
        val request = Request.Builder()
            .url("$baseUrl/api/register")
            .post(json.toString().toRequestBody("application/json".toMediaType()))
            .build()
        
        client.newCall(request).execute().use { response ->
            if (response.isSuccessful) {
                val data = JSONObject(response.body?.string() ?: "")
                apiKey = data.getString("api_key")
            }
        }
    }
    
    suspend fun executeCommand(command: String) {
        val json = JSONObject().apply {
            put("device_id", deviceId)
            put("api_key", apiKey)
            put("command", command)
        }
        
        val request = Request.Builder()
            .url("$baseUrl/api/command")
            .post(json.toString().toRequestBody("application/json".toMediaType()))
            .build()
        
        client.newCall(request).execute()
    }
}
```

#### 3. Watch Complications (Quick Actions)

```kotlin
class ChristaComplication : ComplicationProviderService() {
    override fun onComplicationUpdate(
        complicationId: Int,
        type: Int,
        manager: ComplicationManager
    ) {
        val complicationData = ShortTextComplicationData.Builder(
            PlainComplicationText.Builder("Christa").build(),
            ComplicationText.EMPTY
        )
        .setTapAction(createTapAction())
        .build()
        
        manager.updateComplicationData(complicationId, complicationData)
    }
    
    private fun createTapAction(): PendingIntent {
        // Open app or execute quick command
        return PendingIntent.getActivity(...)
    }
}
```

### Apple Watch

#### 1. SwiftUI App

```swift
// ContentView.swift
import SwiftUI

struct ContentView: View {
    @StateObject private var apiService = ChristaAPIService()
    
    var body: some View {
        VStack(spacing: 10) {
            Button("Chrome") {
                apiService.executeCommand("open chrome")
            }
            
            Button("Lock") {
                apiService.executeCommand("lock screen")
            }
            
            Button("Shutdown") {
                apiService.executeCommand("shutdown")
            }
        }
    }
}
```

#### 2. API Service

```swift
// ChristaAPIService.swift
class ChristaAPIService: ObservableObject {
    let baseURL = "http://YOUR_LAPTOP_IP:5000"
    var deviceId = "my_apple_watch"
    var apiKey: String?
    
    func register() async {
        let url = URL(string: "\(baseURL)/api/register")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "device_id": deviceId,
            "device_info": [
                "type": "watch",
                "name": "My Apple Watch"
            ]
        ]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        do {
            let (data, _) = try await URLSession.shared.data(for: request)
            let response = try JSONDecoder().decode(RegisterResponse.self, from: data)
            apiKey = response.api_key
        } catch {
            print("Registration error: \(error)")
        }
    }
    
    func executeCommand(_ command: String) {
        Task {
            let url = URL(string: "\(baseURL)/api/command")!
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            
            let body: [String: Any] = [
                "device_id": deviceId,
                "api_key": apiKey ?? "",
                "command": command
            ]
            
            request.httpBody = try? JSONSerialization.data(withJSONObject: body)
            
            do {
                let (_, _) = try await URLSession.shared.data(for: request)
            } catch {
                print("Command error: \(error)")
            }
        }
    }
}
```

---

## 📺 Smart TV Integration

### Android TV App

#### 1. TV App Layout

```xml
<!-- activity_main.xml -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="48dp">
    
    <TextView
        android:text="Christa AI"
        android:textSize="48sp"
        android:layout_marginBottom="32dp"/>
    
    <GridLayout
        android:columnCount="3"
        android:rowCount="2">
        
        <Button
            android:text="YouTube"
            android:onClick="openYouTube"/>
        
        <Button
            android:text="Netflix"
            android:onClick="openNetflix"/>
        
        <Button
            android:text="Cast Screen"
            android:onClick="castScreen"/>
    </GridLayout>
</LinearLayout>
```

#### 2. TV Activity

```kotlin
class MainActivity : Activity() {
    private lateinit var apiService: ChristaApiService
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        apiService = ChristaApiService("http://YOUR_LAPTOP_IP:5000")
        
        lifecycleScope.launch {
            apiService.register()
        }
    }
    
    fun openYouTube(view: View) {
        lifecycleScope.launch {
            apiService.executeCommand("play youtube on tv")
        }
        
        // Also open YouTube on TV
        val intent = Intent(Intent.ACTION_VIEW).apply {
            data = Uri.parse("https://www.youtube.com")
        }
        startActivity(intent)
    }
    
    fun openNetflix(view: View) {
        lifecycleScope.launch {
            apiService.executeCommand("play netflix on tv")
        }
        
        val intent = packageManager.getLaunchIntentForPackage("com.netflix.ninja")
        startActivity(intent)
    }
    
    fun castScreen(view: View) {
        lifecycleScope.launch {
            apiService.executeCommand("cast screen to tv")
        }
        // Implement screen casting
    }
}
```

### Google Cast Integration

```python
# On laptop - cast_server.py
from pychromecast import get_chromecasts

def cast_to_tv(content_url: str):
    """Cast content to TV."""
    chromecasts, browser = get_chromecasts()
    
    if chromecasts:
        cast = chromecasts[0]
        cast.wait()
        
        mc = cast.media_controller
        mc.play_media(content_url, 'video/mp4')
        mc.block_until_active()
        
        return True
    return False
```

---

## 🔐 Security & Authentication

### Device Registration Flow

```
1. Device → Server: Register request with device_id
2. Server → Device: Returns API key
3. Device stores API key securely
4. All future requests include device_id + API key
```

### Secure Storage

**Android:**
```kotlin
// Use EncryptedSharedPreferences
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val sharedPreferences = EncryptedSharedPreferences.create(
    context,
    "christa_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

sharedPreferences.edit().putString("api_key", apiKey).apply()
```

**iOS:**
```swift
// Use Keychain
let keychain = KeychainSwift()
keychain.set(apiKey, forKey: "christa_api_key")
```

---

## 🌐 Network Configuration

### Firewall Rules (Laptop)

**Windows:**
```cmd
netsh advfirewall firewall add rule name="Christa AI" dir=in action=allow protocol=TCP localport=5000
```

**Linux:**
```bash
sudo ufw allow 5000/tcp
```

### Port Forwarding (Remote Access)

1. Configure router to forward port 5000 to laptop
2. Use dynamic DNS service (e.g., No-IP, DuckDNS)
3. Update device apps with public URL

**Security Warning:** Use VPN or authentication for remote access!

---

## 📡 Real-Time Communication

### WebSocket Connection

**JavaScript/TypeScript:**
```typescript
import io from 'socket.io-client';

const socket = io('http://YOUR_LAPTOP_IP:5000');

socket.on('connect', () => {
    console.log('Connected to Christa AI');
    
    socket.emit('register', {
        device_id: 'my_device',
        device_info: { type: 'mobile' }
    });
});

socket.on('command_executed', (data) => {
    console.log('Command executed:', data);
    // Update UI
});

// Send command
socket.emit('command', {
    device_id: 'my_device',
    api_key: 'YOUR_API_KEY',
    command: 'open chrome'
});
```

---

## 🎯 Use Cases

### Morning Routine (Watch)
```
Tap watch → "Start morning routine"
→ Laptop opens email, calendar, Spotify
→ TV turns on with news
```

### Movie Time (Phone)
```
Say "Hey Christa, movie time"
→ Laptop dims lights (if smart home)
→ TV opens Netflix
→ Phone goes to DND mode
```

### Work Mode (All Devices)
```
Phone: "Start work mode"
→ Laptop opens VS Code, Slack
→ Watch shows work notifications only
→ TV turns off
```

---

## 🔧 Troubleshooting

### Devices Can't Connect

1. **Check network:**
   ```bash
   ping YOUR_LAPTOP_IP
   ```

2. **Check server:**
   ```bash
   curl http://YOUR_LAPTOP_IP:5000/api/status
   ```

3. **Check firewall:**
   - Temporarily disable to test
   - Add firewall rule for port 5000

### Commands Not Executing

1. **Verify registration:**
   ```bash
   curl http://YOUR_LAPTOP_IP:5000/api/devices?admin_key=YOUR_SECRET_KEY
   ```

2. **Check API key:**
   - Re-register device
   - Verify key is stored correctly

3. **Check server logs:**
   - Look for errors in terminal

---

## 📊 API Reference

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register` | POST | Register device |
| `/api/command` | POST | Execute command |
| `/api/status` | GET | Get server status |
| `/api/history` | GET | Get command history |
| `/api/screenshot` | POST | Take screenshot |

### WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | Connection established |
| `register` | Client → Server | Register device |
| `command` | Client → Server | Execute command |
| `command_result` | Server → Client | Command result |
| `command_executed` | Server → All | Broadcast execution |

---

## 🚀 Next Steps

1. **Build mobile app** using Flutter
2. **Create watch app** for quick actions
3. **Set up TV integration** for media control
4. **Implement notifications** for all devices
5. **Add cloud sync** for remote access

---

## 📚 Resources

- **API Server**: `api_server.py`
- **Mobile Client**: `mobile_client.py`
- **Flutter Guide**: `mobile_app/README.md`
- **Main Docs**: `README_ADVANCED.md`

---

**Your laptop is now the central AI hub for all your devices!** 🎉

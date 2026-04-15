# 📱 Christa AI - Mobile App

Flutter-based mobile app for controlling your laptop via Christa AI.

## Features

- 🎤 Voice commands from phone
- 🖥️ Control laptop remotely
- 📸 Take screenshots
- 📁 Access and search files
- 🔔 Receive notifications from laptop
- ⚡ Quick action buttons
- 📊 Activity dashboard

## Setup

### Prerequisites

- Flutter SDK (3.0+)
- Android Studio / VS Code
- Android device or emulator

### Installation

1. **Install Flutter**
   ```bash
   # Follow: https://flutter.dev/docs/get-started/install
   ```

2. **Create Flutter project**
   ```bash
   flutter create christa_mobile
   cd christa_mobile
   ```

3. **Add dependencies** (pubspec.yaml)
   ```yaml
   dependencies:
     flutter:
       sdk: flutter
     http: ^1.1.0
     socket_io_client: ^2.0.3+1
     speech_to_text: ^6.5.1
     permission_handler: ^11.1.0
     shared_preferences: ^2.2.2
   ```

4. **Install dependencies**
   ```bash
   flutter pub get
   ```

## Project Structure

```
christa_mobile/
├── lib/
│   ├── main.dart                 # App entry point
│   ├── services/
│   │   ├── api_service.dart      # REST API client
│   │   └── websocket_service.dart # WebSocket client
│   ├── screens/
│   │   ├── home_screen.dart      # Main dashboard
│   │   ├── voice_screen.dart     # Voice control
│   │   └── settings_screen.dart  # Settings
│   ├── widgets/
│   │   ├── quick_action_button.dart
│   │   └── command_history.dart
│   └── models/
│       └── command_result.dart
└── android/
    └── app/
        └── src/
            └── main/
                └── AndroidManifest.xml  # Permissions
```

## Code Examples

### API Service (lib/services/api_service.dart)

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;
  String? deviceId;
  String? apiKey;

  ApiService({required this.baseUrl});

  Future<bool> register(String deviceId, Map<String, dynamic> deviceInfo) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'device_id': deviceId,
          'device_info': deviceInfo,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        this.deviceId = deviceId;
        this.apiKey = data['api_key'];
        return true;
      }
      return false;
    } catch (e) {
      print('Registration error: $e');
      return false;
    }
  }

  Future<Map<String, dynamic>> executeCommand(String command) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/command'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'device_id': deviceId,
          'api_key': apiKey,
          'command': command,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return {'error': 'Command failed'};
    } catch (e) {
      return {'error': e.toString()};
    }
  }

  Future<Map<String, dynamic>> getStatus() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/status?device_id=$deviceId&api_key=$apiKey'),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return {'error': 'Status check failed'};
    } catch (e) {
      return {'error': e.toString()};
    }
  }
}
```

### Main App (lib/main.dart)

```dart
import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const ChristaApp());
}

class ChristaApp extends StatelessWidget {
  const ChristaApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Christa AI',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
```

### Home Screen (lib/screens/home_screen.dart)

```dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late ApiService apiService;
  bool isConnected = false;
  String statusText = 'Not connected';

  @override
  void initState() {
    super.initState();
    apiService = ApiService(baseUrl: 'http://YOUR_LAPTOP_IP:5000');
    _initialize();
  }

  Future<void> _initialize() async {
    // Register device
    final success = await apiService.register(
      'my_android_phone',
      {
        'type': 'mobile',
        'name': 'My Phone',
        'platform': 'Android',
      },
    );

    setState(() {
      isConnected = success;
      statusText = success ? 'Connected' : 'Connection failed';
    });
  }

  Future<void> _executeCommand(String command) async {
    final result = await apiService.executeCommand(command);
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(result['response'] ?? 'Command executed'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Christa AI'),
        actions: [
          IconButton(
            icon: Icon(
              isConnected ? Icons.cloud_done : Icons.cloud_off,
              color: isConnected ? Colors.green : Colors.red,
            ),
            onPressed: _initialize,
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Status Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    Icon(
                      isConnected ? Icons.check_circle : Icons.error,
                      size: 48,
                      color: isConnected ? Colors.green : Colors.red,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      statusText,
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            
            // Quick Actions
            Text(
              'Quick Actions',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                children: [
                  _buildQuickAction(
                    'Open Chrome',
                    Icons.web,
                    () => _executeCommand('open chrome'),
                  ),
                  _buildQuickAction(
                    'Screenshot',
                    Icons.screenshot,
                    () => _executeCommand('take screenshot'),
                  ),
                  _buildQuickAction(
                    'Lock Screen',
                    Icons.lock,
                    () => _executeCommand('lock screen'),
                  ),
                  _buildQuickAction(
                    'Search Files',
                    Icons.search,
                    () => _showSearchDialog(),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Navigate to voice screen
        },
        child: const Icon(Icons.mic),
      ),
    );
  }

  Widget _buildQuickAction(String label, IconData icon, VoidCallback onTap) {
    return Card(
      child: InkWell(
        onTap: isConnected ? onTap : null,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48),
            const SizedBox(height: 8),
            Text(label, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }

  void _showSearchDialog() {
    showDialog(
      context: context,
      builder: (context) {
        String query = '';
        return AlertDialog(
          title: const Text('Search Files'),
          content: TextField(
            onChanged: (value) => query = value,
            decoration: const InputDecoration(
              hintText: 'Enter search query',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                Navigator.pop(context);
                _executeCommand('find $query');
              },
              child: const Text('Search'),
            ),
          ],
        );
      },
    );
  }
}
```

## Android Permissions

Add to `android/app/src/main/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Internet permission -->
    <uses-permission android:name="android.permission.INTERNET" />
    
    <!-- Microphone for voice commands -->
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    
    <!-- Network state -->
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application>
        <!-- Your app configuration -->
    </application>
</manifest>
```

## Configuration

### Connect to Your Laptop

1. Find your laptop's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. Update `baseUrl` in the app:
   ```dart
   ApiService(baseUrl: 'http://YOUR_LAPTOP_IP:5000')
   ```

3. Make sure laptop and phone are on same network

4. Start the API server on laptop:
   ```bash
   python api_server.py
   ```

## Building the App

### Debug Build
```bash
flutter run
```

### Release Build (Android)
```bash
flutter build apk --release
```

The APK will be in `build/app/outputs/flutter-apk/app-release.apk`

## Features to Implement

### Phase 1 (Basic)
- [x] REST API connection
- [x] Device registration
- [x] Command execution
- [x] Quick action buttons
- [ ] Voice input
- [ ] Command history

### Phase 2 (Advanced)
- [ ] WebSocket real-time connection
- [ ] Push notifications
- [ ] File browser
- [ ] Screenshot viewer
- [ ] Settings page
- [ ] Dark mode

### Phase 3 (Pro)
- [ ] Widgets
- [ ] Shortcuts
- [ ] Automation triggers
- [ ] Multi-device support
- [ ] Offline queue

## Testing

1. **Start laptop server**:
   ```bash
   python api_server.py
   ```

2. **Run mobile app**:
   ```bash
   flutter run
   ```

3. **Test commands**:
   - Tap "Open Chrome"
   - Tap "Screenshot"
   - Try voice command

## Troubleshooting

### Cannot connect to server
- Check laptop and phone on same WiFi
- Verify laptop IP address
- Check firewall settings
- Ensure server is running

### Voice not working
- Grant microphone permission
- Check device microphone
- Test with other voice apps

### Commands not executing
- Check API key is valid
- Verify device is registered
- Check server logs

## Next Steps

1. Implement voice input screen
2. Add WebSocket for real-time updates
3. Create settings page
4. Add file browser
5. Implement notifications

## Resources

- Flutter Docs: https://flutter.dev/docs
- HTTP Package: https://pub.dev/packages/http
- Socket.IO Client: https://pub.dev/packages/socket_io_client
- Speech to Text: https://pub.dev/packages/speech_to_text

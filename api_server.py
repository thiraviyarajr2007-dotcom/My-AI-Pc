"""
Christa AI - API Server
REST API + WebSocket server for cross-device communication
Allows mobile, watch, TV, and other devices to control the laptop
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
import json
import os
from datetime import datetime
from typing import Dict, Optional
import secrets


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
CORS(app)  # Enable CORS for cross-origin requests
socketio = SocketIO(app, cors_allowed_origins="*")

# Import Christa AI modules
try:
    from ai_brain import AIBrain
    import control_ai
    import aiscreencontrol_ai
    import filesearch_ai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("[!] AI modules not available. Running in limited mode.")

# Global state
brain = AIBrain() if AI_AVAILABLE else None
connected_devices = {}
command_history = []
MAX_HISTORY = 100


# ─── Authentication ────────────────────────────────────────────
class DeviceAuth:
    """Simple device authentication system."""
    
    def __init__(self):
        self.devices_file = "registered_devices.json"
        self.devices = self.load_devices()
    
    def load_devices(self) -> Dict:
        """Load registered devices."""
        if os.path.exists(self.devices_file):
            try:
                with open(self.devices_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_devices(self):
        """Save registered devices."""
        try:
            with open(self.devices_file, 'w') as f:
                json.dump(self.devices, f, indent=2)
        except Exception as e:
            print(f"[!] Could not save devices: {e}")
    
    def register_device(self, device_id: str, device_info: Dict) -> str:
        """Register a new device and return API key."""
        api_key = secrets.token_urlsafe(32)
        self.devices[device_id] = {
            "api_key": api_key,
            "info": device_info,
            "registered_at": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat()
        }
        self.save_devices()
        return api_key
    
    def verify_device(self, device_id: str, api_key: str) -> bool:
        """Verify device credentials."""
        if device_id in self.devices:
            if self.devices[device_id]["api_key"] == api_key:
                self.devices[device_id]["last_seen"] = datetime.now().isoformat()
                return True
        return False
    
    def get_device_info(self, device_id: str) -> Optional[Dict]:
        """Get device information."""
        return self.devices.get(device_id)


auth = DeviceAuth()


# ─── Helper Functions ──────────────────────────────────────────
def log_command(device_id: str, command: str, result: Dict):
    """Log command execution."""
    entry = {
        "device_id": device_id,
        "command": command,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }
    command_history.append(entry)
    
    # Keep only recent history
    if len(command_history) > MAX_HISTORY:
        command_history.pop(0)


def execute_command(command: str, device_id: str) -> Dict:
    """Execute a command and return result."""
    if not AI_AVAILABLE:
        return {
            "success": False,
            "error": "AI modules not available",
            "response": "System is running in limited mode"
        }
    
    try:
        # Process through AI brain
        result = brain.process_input(command)
        
        # Execute action if available
        action = result.get('action', {})
        if action and action.get('module'):
            _execute_action(action)
        
        log_command(device_id, command, result)
        
        return {
            "success": True,
            "intent": result.get('intent'),
            "confidence": result.get('confidence'),
            "response": result.get('response'),
            "action": action
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": f"Error executing command: {e}"
        }


def _execute_action(action: Dict):
    """Execute the determined action."""
    module_name = action.get('module')
    function_name = action.get('function')
    params = action.get('params', {})
    
    try:
        if module_name == "control_ai":
            if function_name == "open_app":
                control_ai.open_app(params.get('app_name', ''))
            elif function_name == "run_system_command":
                control_ai.run_system_command(params.get('command', ''))
        
        elif module_name == "aiscreencontrol_ai":
            if function_name == "take_screenshot":
                path = aiscreencontrol_ai.take_screenshot()
                return {"screenshot_path": path}
            elif function_name == "type_text":
                aiscreencontrol_ai.type_text(params.get('text', ''))
        
        elif module_name == "filesearch_ai":
            if function_name == "search_by_name":
                results = filesearch_ai.search_by_name(params.get('query', ''), max_results=5)
                return {"files": [r['path'] for r in results]}
    
    except Exception as e:
        print(f"[!] Action execution error: {e}")


# ─── REST API Endpoints ────────────────────────────────────────

@app.route('/')
def index():
    """API information."""
    return jsonify({
        "name": "Christa AI API",
        "version": "1.0.0",
        "status": "running",
        "ai_available": AI_AVAILABLE,
        "endpoints": {
            "POST /api/register": "Register a new device",
            "POST /api/command": "Execute a command",
            "GET /api/status": "Get system status",
            "GET /api/history": "Get command history",
            "GET /api/devices": "List connected devices",
            "WebSocket /socket.io": "Real-time communication"
        }
    })


@app.route('/api/register', methods=['POST'])
def register_device():
    """Register a new device."""
    data = request.json
    device_id = data.get('device_id')
    device_info = data.get('device_info', {})
    
    if not device_id:
        return jsonify({"error": "device_id required"}), 400
    
    api_key = auth.register_device(device_id, device_info)
    
    return jsonify({
        "success": True,
        "device_id": device_id,
        "api_key": api_key,
        "message": "Device registered successfully"
    })


@app.route('/api/command', methods=['POST'])
def execute_command_endpoint():
    """Execute a command from a device."""
    data = request.json
    device_id = data.get('device_id')
    api_key = data.get('api_key')
    command = data.get('command')
    
    # Verify authentication
    if not auth.verify_device(device_id, api_key):
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not command:
        return jsonify({"error": "command required"}), 400
    
    # Execute command
    result = execute_command(command, device_id)
    
    # Broadcast to connected WebSocket clients
    socketio.emit('command_executed', {
        "device_id": device_id,
        "command": command,
        "result": result
    })
    
    return jsonify(result)


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status."""
    device_id = request.args.get('device_id')
    api_key = request.args.get('api_key')
    
    if device_id and api_key:
        if not auth.verify_device(device_id, api_key):
            return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({
        "status": "online",
        "ai_available": AI_AVAILABLE,
        "connected_devices": len(connected_devices),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get command history."""
    device_id = request.args.get('device_id')
    api_key = request.args.get('api_key')
    limit = int(request.args.get('limit', 10))
    
    if not auth.verify_device(device_id, api_key):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Filter history for this device
    device_history = [
        h for h in command_history
        if h['device_id'] == device_id
    ][-limit:]
    
    return jsonify({
        "history": device_history,
        "count": len(device_history)
    })


@app.route('/api/devices', methods=['GET'])
def list_devices():
    """List registered devices."""
    admin_key = request.args.get('admin_key')
    
    # Simple admin authentication (in production, use proper auth)
    if admin_key != app.config['SECRET_KEY']:
        return jsonify({"error": "Unauthorized"}), 401
    
    devices = []
    for device_id, info in auth.devices.items():
        devices.append({
            "device_id": device_id,
            "info": info['info'],
            "registered_at": info['registered_at'],
            "last_seen": info['last_seen']
        })
    
    return jsonify({"devices": devices})


@app.route('/api/screenshot', methods=['POST'])
def take_screenshot_endpoint():
    """Take a screenshot and return path."""
    data = request.json
    device_id = data.get('device_id')
    api_key = data.get('api_key')
    
    if not auth.verify_device(device_id, api_key):
        return jsonify({"error": "Invalid credentials"}), 401
    
    try:
        path = aiscreencontrol_ai.take_screenshot()
        return jsonify({
            "success": True,
            "path": path,
            "message": "Screenshot taken"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ─── WebSocket Events ──────────────────────────────────────────

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print(f"[WebSocket] Client connected: {request.sid}")
    emit('connected', {"message": "Connected to Christa AI"})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print(f"[WebSocket] Client disconnected: {request.sid}")
    
    # Remove from connected devices
    if request.sid in connected_devices:
        del connected_devices[request.sid]


@socketio.on('register')
def handle_register(data):
    """Register device via WebSocket."""
    device_id = data.get('device_id')
    device_info = data.get('device_info', {})
    
    connected_devices[request.sid] = {
        "device_id": device_id,
        "info": device_info,
        "connected_at": datetime.now().isoformat()
    }
    
    emit('registered', {
        "success": True,
        "message": f"Device {device_id} registered"
    })
    
    print(f"[WebSocket] Device registered: {device_id}")


@socketio.on('command')
def handle_command(data):
    """Handle command via WebSocket."""
    device_id = data.get('device_id')
    api_key = data.get('api_key')
    command = data.get('command')
    
    # Verify authentication
    if not auth.verify_device(device_id, api_key):
        emit('error', {"error": "Invalid credentials"})
        return
    
    # Execute command
    result = execute_command(command, device_id)
    
    # Send result back to sender
    emit('command_result', result)
    
    # Broadcast to all connected devices
    socketio.emit('command_executed', {
        "device_id": device_id,
        "command": command,
        "result": result
    }, broadcast=True)


@socketio.on('ping')
def handle_ping():
    """Handle ping for keep-alive."""
    emit('pong', {"timestamp": datetime.now().isoformat()})


# ─── Server Control ────────────────────────────────────────────

def run_server(host='0.0.0.0', port=5000, debug=False):
    """Run the API server."""
    print("=" * 60)
    print("  🌐 Christa AI - API Server")
    print("=" * 60)
    print(f"\n  Server starting on http://{host}:{port}")
    print(f"  AI Available: {AI_AVAILABLE}")
    print(f"\n  Endpoints:")
    print(f"    • REST API: http://{host}:{port}/api/")
    print(f"    • WebSocket: ws://{host}:{port}/socket.io")
    print(f"\n  Press Ctrl+C to stop")
    print("=" * 60)
    
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Christa AI API Server")
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    try:
        run_server(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\n\n[!] Server stopped")
        print("👋 Goodbye!")

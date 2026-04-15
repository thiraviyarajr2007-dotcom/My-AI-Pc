"""
Christa AI - Mobile Client Library
Python client for connecting mobile/watch/TV devices to Christa AI
Can be used as reference for Flutter/Android implementation
"""

import requests
import json
from typing import Dict, Optional, Callable
import socketio
from datetime import datetime


class ChristaClient:
    """Client for connecting to Christa AI API server."""
    
    def __init__(
        self,
        server_url: str = "http://localhost:5000",
        device_id: str = None,
        device_type: str = "mobile"
    ):
        """
        Initialize Christa AI client.
        
        Args:
            server_url: URL of the Christa AI server
            device_id: Unique device identifier
            device_type: Type of device (mobile, watch, tv, etc.)
        """
        self.server_url = server_url.rstrip('/')
        self.device_id = device_id or f"{device_type}_{datetime.now().timestamp()}"
        self.device_type = device_type
        self.api_key = None
        self.sio = None
        self.connected = False
    
    def register(self, device_info: Optional[Dict] = None) -> bool:
        """
        Register this device with the server.
        
        Args:
            device_info: Additional device information
        
        Returns:
            True if registration successful
        """
        if device_info is None:
            device_info = {
                "type": self.device_type,
                "name": f"My {self.device_type.title()}",
                "platform": "python_client"
            }
        
        try:
            response = requests.post(
                f"{self.server_url}/api/register",
                json={
                    "device_id": self.device_id,
                    "device_info": device_info
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.api_key = data.get('api_key')
                print(f"[✓] Device registered: {self.device_id}")
                print(f"    API Key: {self.api_key[:20]}...")
                return True
            else:
                print(f"[✗] Registration failed: {response.text}")
                return False
        
        except Exception as e:
            print(f"[✗] Registration error: {e}")
            return False
    
    def execute_command(self, command: str) -> Dict:
        """
        Execute a command on the laptop.
        
        Args:
            command: Natural language command
        
        Returns:
            Result dictionary
        """
        if not self.api_key:
            return {"error": "Not registered. Call register() first."}
        
        try:
            response = requests.post(
                f"{self.server_url}/api/command",
                json={
                    "device_id": self.device_id,
                    "api_key": self.api_key,
                    "command": command
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Command failed: {response.text}"}
        
        except Exception as e:
            return {"error": f"Command error: {e}"}
    
    def get_status(self) -> Dict:
        """Get server status."""
        try:
            response = requests.get(
                f"{self.server_url}/api/status",
                params={
                    "device_id": self.device_id,
                    "api_key": self.api_key
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Status check failed"}
        
        except Exception as e:
            return {"error": f"Status error: {e}"}
    
    def get_history(self, limit: int = 10) -> Dict:
        """Get command history."""
        if not self.api_key:
            return {"error": "Not registered"}
        
        try:
            response = requests.get(
                f"{self.server_url}/api/history",
                params={
                    "device_id": self.device_id,
                    "api_key": self.api_key,
                    "limit": limit
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "History fetch failed"}
        
        except Exception as e:
            return {"error": f"History error: {e}"}
    
    def take_screenshot(self) -> Dict:
        """Request a screenshot from the laptop."""
        if not self.api_key:
            return {"error": "Not registered"}
        
        try:
            response = requests.post(
                f"{self.server_url}/api/screenshot",
                json={
                    "device_id": self.device_id,
                    "api_key": self.api_key
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Screenshot failed"}
        
        except Exception as e:
            return {"error": f"Screenshot error: {e}"}
    
    # ─── WebSocket Methods ─────────────────────────────────────
    
    def connect_websocket(
        self,
        on_message: Optional[Callable] = None,
        on_command_executed: Optional[Callable] = None
    ):
        """
        Connect to server via WebSocket for real-time communication.
        
        Args:
            on_message: Callback for general messages
            on_command_executed: Callback when commands are executed
        """
        self.sio = socketio.Client()
        
        @self.sio.on('connect')
        def on_connect():
            print("[WebSocket] Connected to server")
            self.connected = True
            
            # Register device
            self.sio.emit('register', {
                "device_id": self.device_id,
                "device_info": {
                    "type": self.device_type,
                    "platform": "python_client"
                }
            })
        
        @self.sio.on('disconnect')
        def on_disconnect():
            print("[WebSocket] Disconnected from server")
            self.connected = False
        
        @self.sio.on('registered')
        def on_registered(data):
            print(f"[WebSocket] {data.get('message')}")
        
        @self.sio.on('command_result')
        def on_command_result(data):
            if on_message:
                on_message(data)
        
        @self.sio.on('command_executed')
        def on_cmd_executed(data):
            if on_command_executed:
                on_command_executed(data)
        
        @self.sio.on('error')
        def on_error(data):
            print(f"[WebSocket Error] {data.get('error')}")
        
        try:
            self.sio.connect(self.server_url)
            return True
        except Exception as e:
            print(f"[✗] WebSocket connection failed: {e}")
            return False
    
    def send_command_ws(self, command: str):
        """Send command via WebSocket."""
        if not self.connected:
            print("[!] Not connected to WebSocket")
            return
        
        self.sio.emit('command', {
            "device_id": self.device_id,
            "api_key": self.api_key,
            "command": command
        })
    
    def disconnect_websocket(self):
        """Disconnect from WebSocket."""
        if self.sio and self.connected:
            self.sio.disconnect()


# ─── Quick Action Helpers ──────────────────────────────────────

class QuickActions:
    """Pre-defined quick actions for common tasks."""
    
    def __init__(self, client: ChristaClient):
        self.client = client
    
    def open_app(self, app_name: str) -> Dict:
        """Open an application."""
        return self.client.execute_command(f"open {app_name}")
    
    def take_screenshot(self) -> Dict:
        """Take a screenshot."""
        return self.client.take_screenshot()
    
    def lock_screen(self) -> Dict:
        """Lock the laptop screen."""
        return self.client.execute_command("lock screen")
    
    def shutdown(self, cancel: bool = False) -> Dict:
        """Shutdown or cancel shutdown."""
        if cancel:
            return self.client.execute_command("cancel shutdown")
        return self.client.execute_command("shutdown")
    
    def search_files(self, query: str) -> Dict:
        """Search for files."""
        return self.client.execute_command(f"find {query}")
    
    def type_text(self, text: str) -> Dict:
        """Type text on laptop."""
        return self.client.execute_command(f"type {text}")


# ─── Example Usage ─────────────────────────────────────────────

def example_mobile_app():
    """Example mobile app simulation."""
    print("=" * 60)
    print("  📱 Christa AI - Mobile Client Example")
    print("=" * 60)
    
    # Initialize client
    client = ChristaClient(
        server_url="http://localhost:5000",
        device_id="my_phone",
        device_type="mobile"
    )
    
    # Register device
    print("\n[1] Registering device...")
    if not client.register({
        "type": "mobile",
        "name": "My Android Phone",
        "platform": "Android 13"
    }):
        print("[✗] Registration failed")
        return
    
    # Create quick actions helper
    actions = QuickActions(client)
    
    # Interactive menu
    print("\n" + "=" * 60)
    print("  Mobile Control Menu")
    print("=" * 60)
    print("\n  Commands:")
    print("    1. Open Chrome")
    print("    2. Take Screenshot")
    print("    3. Lock Screen")
    print("    4. Search Files")
    print("    5. Custom Command")
    print("    6. Get Status")
    print("    7. View History")
    print("    8. Exit")
    print("\n" + "=" * 60)
    
    while True:
        try:
            choice = input("\n📱 Choose (1-8): ").strip()
            
            if choice == "1":
                print("\n[▶] Opening Chrome...")
                result = actions.open_app("chrome")
                print(f"[✓] {result.get('response', 'Done')}")
            
            elif choice == "2":
                print("\n[▶] Taking screenshot...")
                result = actions.take_screenshot()
                if result.get('success'):
                    print(f"[✓] Screenshot saved: {result.get('path')}")
                else:
                    print(f"[✗] {result.get('error')}")
            
            elif choice == "3":
                print("\n[▶] Locking screen...")
                result = actions.lock_screen()
                print(f"[✓] {result.get('response', 'Done')}")
            
            elif choice == "4":
                query = input("  Search for: ").strip()
                print(f"\n[▶] Searching for '{query}'...")
                result = actions.search_files(query)
                print(f"[✓] {result.get('response', 'Done')}")
            
            elif choice == "5":
                command = input("  Enter command: ").strip()
                print(f"\n[▶] Executing: {command}")
                result = client.execute_command(command)
                print(f"[✓] {result.get('response', 'Done')}")
            
            elif choice == "6":
                print("\n[▶] Getting status...")
                status = client.get_status()
                print(f"[✓] Status: {status.get('status')}")
                print(f"    AI Available: {status.get('ai_available')}")
                print(f"    Connected Devices: {status.get('connected_devices')}")
            
            elif choice == "7":
                print("\n[▶] Fetching history...")
                history = client.get_history(limit=5)
                if 'history' in history:
                    print(f"[✓] Recent commands:")
                    for h in history['history']:
                        print(f"    • {h['command']} ({h['timestamp']})")
                else:
                    print(f"[!] {history.get('error')}")
            
            elif choice == "8":
                print("\n👋 Goodbye!")
                break
            
            else:
                print("[!] Invalid choice")
        
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"[✗] Error: {e}")


if __name__ == "__main__":
    example_mobile_app()

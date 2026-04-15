"""
Context Awareness System - Understands what user is doing
Tracks: Active window, clipboard, screen content, activity patterns
"""

import os
import sys
import time
import threading
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

# Platform-specific imports
if sys.platform == "win32":
    import win32gui
    import win32process
    import psutil
    try:
        import pyperclip
    except ImportError:
        pyperclip = None
else:
    print("[!] Context awareness currently supports Windows only")


class ActiveWindowTracker:
    """Tracks the currently active window and application."""
    
    def __init__(self):
        self.current_window = None
        self.current_app = None
        self.window_history = []
        self.app_usage_time = defaultdict(float)
        self.last_check_time = time.time()
    
    def get_active_window(self) -> Dict:
        """Get information about the currently active window."""
        if sys.platform != "win32":
            return {}
        
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            
            # Get process info
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            app_name = process.name()
            
            return {
                "title": window_title,
                "app": app_name,
                "pid": pid,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {}
    
    def update(self):
        """Update current window info and track usage time."""
        window_info = self.get_active_window()
        
        if not window_info:
            return
        
        current_time = time.time()
        time_delta = current_time - self.last_check_time
        
        # Track app usage time
        if self.current_app:
            self.app_usage_time[self.current_app] += time_delta
        
        # Update current window
        if window_info["app"] != self.current_app:
            self.current_app = window_info["app"]
            self.current_window = window_info["title"]
            self.window_history.append(window_info)
            
            # Keep only last 100 entries
            if len(self.window_history) > 100:
                self.window_history = self.window_history[-100:]
        
        self.last_check_time = current_time
    
    def get_most_used_apps(self, top_n: int = 5) -> List[tuple]:
        """Get most used applications."""
        sorted_apps = sorted(
            self.app_usage_time.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_apps[:top_n]
    
    def get_context_summary(self) -> str:
        """Get a summary of current context."""
        if not self.current_app:
            return "No active application detected"
        
        return f"Currently using: {self.current_app} - {self.current_window}"


class ClipboardMonitor:
    """Monitors clipboard for smart paste suggestions."""
    
    def __init__(self):
        self.clipboard_history = []
        self.last_clipboard = ""
        self.max_history = 20
    
    def update(self):
        """Check clipboard and update history."""
        if not pyperclip:
            return
        
        try:
            current = pyperclip.paste()
            
            if current and current != self.last_clipboard:
                self.clipboard_history.append({
                    "content": current[:500],  # Limit size
                    "timestamp": datetime.now().isoformat(),
                    "length": len(current)
                })
                
                # Keep only recent items
                if len(self.clipboard_history) > self.max_history:
                    self.clipboard_history = self.clipboard_history[-self.max_history:]
                
                self.last_clipboard = current
        
        except Exception as e:
            pass
    
    def get_recent(self, n: int = 5) -> List[Dict]:
        """Get recent clipboard items."""
        return self.clipboard_history[-n:]
    
    def search(self, query: str) -> List[Dict]:
        """Search clipboard history."""
        query_lower = query.lower()
        results = []
        
        for item in reversed(self.clipboard_history):
            if query_lower in item["content"].lower():
                results.append(item)
                if len(results) >= 5:
                    break
        
        return results


class ActivityPattern:
    """Learns and tracks user activity patterns."""
    
    def __init__(self, storage_file: str = "activity_patterns.json"):
        self.storage_file = storage_file
        self.patterns = {
            "hourly_activity": defaultdict(list),  # Activity by hour
            "app_sequences": defaultdict(int),  # Common app sequences
            "frequent_files": defaultdict(int),  # Frequently accessed files
            "work_hours": {"start": 9, "end": 17}  # Default work hours
        }
        self.load()
    
    def load(self):
        """Load patterns from disk."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.patterns.update(data)
            except:
                pass
    
    def save(self):
        """Save patterns to disk."""
        try:
            # Convert defaultdicts to regular dicts for JSON
            data = {
                "hourly_activity": dict(self.patterns["hourly_activity"]),
                "app_sequences": dict(self.patterns["app_sequences"]),
                "frequent_files": dict(self.patterns["frequent_files"]),
                "work_hours": self.patterns["work_hours"]
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[!] Could not save patterns: {e}")
    
    def record_activity(self, activity_type: str, details: Dict):
        """Record an activity for pattern learning."""
        hour = datetime.now().hour
        
        # Record hourly activity
        self.patterns["hourly_activity"][str(hour)].append({
            "type": activity_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update work hours based on activity
        if activity_type in ["app_opened", "file_accessed"]:
            if hour < self.patterns["work_hours"]["start"]:
                self.patterns["work_hours"]["start"] = hour
            if hour > self.patterns["work_hours"]["end"]:
                self.patterns["work_hours"]["end"] = hour
    
    def predict_next_app(self, current_app: str) -> Optional[str]:
        """Predict what app user might open next."""
        # Find most common app after current_app
        max_count = 0
        predicted_app = None
        
        for sequence, count in self.patterns["app_sequences"].items():
            if sequence.startswith(current_app + "->"):
                if count > max_count:
                    max_count = count
                    predicted_app = sequence.split("->")[1]
        
        return predicted_app
    
    def is_work_hours(self) -> bool:
        """Check if current time is within work hours."""
        current_hour = datetime.now().hour
        return (
            self.patterns["work_hours"]["start"] <= current_hour <=
            self.patterns["work_hours"]["end"]
        )


class ContextAwarenessSystem:
    """Main context awareness system."""
    
    def __init__(self, update_interval: float = 2.0):
        """
        Initialize context awareness system.
        
        Args:
            update_interval: How often to update context (seconds)
        """
        self.window_tracker = ActiveWindowTracker()
        self.clipboard_monitor = ClipboardMonitor()
        self.activity_pattern = ActivityPattern()
        self.update_interval = update_interval
        self.is_running = False
        self._thread = None
    
    def _update_loop(self):
        """Background update loop."""
        while self.is_running:
            try:
                self.window_tracker.update()
                self.clipboard_monitor.update()
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"[!] Context update error: {e}")
                time.sleep(self.update_interval)
    
    def start(self):
        """Start context monitoring."""
        if self.is_running:
            return
        
        self.is_running = True
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()
        print("[✓] Context awareness started")
    
    def stop(self):
        """Stop context monitoring."""
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=5)
        self.activity_pattern.save()
        print("[✓] Context awareness stopped")
    
    def get_current_context(self) -> Dict:
        """Get complete current context."""
        return {
            "active_window": self.window_tracker.get_context_summary(),
            "current_app": self.window_tracker.current_app,
            "recent_clipboard": self.clipboard_monitor.get_recent(3),
            "is_work_hours": self.activity_pattern.is_work_hours(),
            "most_used_apps": self.window_tracker.get_most_used_apps(5)
        }
    
    def get_suggestions(self) -> List[str]:
        """Get proactive suggestions based on context."""
        suggestions = []
        
        # Suggest break if working for long time
        if self.activity_pattern.is_work_hours():
            top_apps = self.window_tracker.get_most_used_apps(1)
            if top_apps and top_apps[0][1] > 3600:  # More than 1 hour
                suggestions.append("You've been working for a while. Consider taking a break!")
        
        # Suggest next app
        if self.window_tracker.current_app:
            next_app = self.activity_pattern.predict_next_app(
                self.window_tracker.current_app
            )
            if next_app:
                suggestions.append(f"You usually open {next_app} next. Want me to open it?")
        
        return suggestions


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  👁️  Context Awareness System - Test Mode")
    print("=" * 55)
    
    if sys.platform != "win32":
        print("\n[!] This system currently supports Windows only")
        sys.exit(1)
    
    context_system = ContextAwarenessSystem(update_interval=2.0)
    context_system.start()
    
    print("\n  Monitoring your activity...")
    print("  Press Ctrl+C to stop and see summary\n")
    
    try:
        while True:
            time.sleep(5)
            
            # Show current context
            context = context_system.get_current_context()
            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] {context['active_window']}", end="")
    
    except KeyboardInterrupt:
        print("\n\n[!] Stopping...")
        context_system.stop()
        
        # Show summary
        context = context_system.get_current_context()
        print("\n📊 Activity Summary:")
        print(f"\n  Most used applications:")
        for app, duration in context["most_used_apps"]:
            minutes = int(duration / 60)
            print(f"    • {app}: {minutes} minutes")
        
        print(f"\n  Recent clipboard items:")
        for item in context["recent_clipboard"]:
            preview = item["content"][:50]
            print(f"    • {preview}...")
        
        suggestions = context_system.get_suggestions()
        if suggestions:
            print(f"\n  💡 Suggestions:")
            for suggestion in suggestions:
                print(f"    • {suggestion}")
        
        print("\n👋 Goodbye!")

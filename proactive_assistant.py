"""
Proactive Assistant - Anticipates needs and provides suggestions
Features: Smart notifications, auto-organization, predictive actions
"""

import os
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from collections import defaultdict


class SmartNotification:
    """Represents a smart notification."""
    
    def __init__(
        self,
        title: str,
        message: str,
        priority: str = "normal",
        action: Optional[Callable] = None
    ):
        self.title = title
        self.message = message
        self.priority = priority  # low, normal, high, urgent
        self.action = action
        self.timestamp = datetime.now()
        self.shown = False
    
    def show(self):
        """Display the notification."""
        priority_icons = {
            "low": "ℹ️",
            "normal": "💡",
            "high": "⚠️",
            "urgent": "🚨"
        }
        icon = priority_icons.get(self.priority, "💡")
        
        print(f"\n{icon} {self.title}")
        print(f"   {self.message}")
        if self.action:
            print(f"   [Action available]")
        print()
        
        self.shown = True


class ProactiveAssistant:
    """Main proactive assistance system."""
    
    def __init__(self, context_system=None):
        """
        Initialize proactive assistant.
        
        Args:
            context_system: ContextAwarenessSystem instance for context info
        """
        self.context_system = context_system
        self.notifications: List[SmartNotification] = []
        self.is_running = False
        self._thread = None
        
        # Tracking
        self.last_break_reminder = None
        self.last_backup_reminder = None
        self.work_session_start = None
        self.downloads_checked = set()
    
    def _check_loop(self):
        """Background loop for proactive checks."""
        while self.is_running:
            try:
                self._check_break_reminder()
                self._check_battery()
                self._check_downloads_folder()
                self._check_work_session()
                self._check_meeting_reminders()
                
                # Show pending notifications
                self._show_pending_notifications()
                
                time.sleep(60)  # Check every minute
            
            except Exception as e:
                print(f"[!] Proactive check error: {e}")
                time.sleep(60)
    
    def _check_break_reminder(self):
        """Remind user to take breaks."""
        if not self.context_system:
            return
        
        # Check if user has been working continuously
        if self.context_system.activity_pattern.is_work_hours():
            now = datetime.now()
            
            # Remind every 60 minutes
            if (not self.last_break_reminder or
                (now - self.last_break_reminder) > timedelta(minutes=60)):
                
                self.add_notification(
                    "Break Time! 🧘",
                    "You've been working for a while. Take a 5-minute break to rest your eyes.",
                    priority="normal"
                )
                self.last_break_reminder = now
    
    def _check_battery(self):
        """Check battery status and warn if low."""
        try:
            import psutil
            battery = psutil.sensors_battery()
            
            if battery:
                if battery.percent < 20 and not battery.power_plugged:
                    self.add_notification(
                        "Low Battery! 🔋",
                        f"Battery at {battery.percent}%. Please plug in your charger.",
                        priority="high"
                    )
                elif battery.percent == 100 and battery.power_plugged:
                    self.add_notification(
                        "Battery Full 🔌",
                        "Battery is fully charged. You can unplug the charger.",
                        priority="low"
                    )
        except:
            pass
    
    def _check_downloads_folder(self):
        """Check for new files in downloads and suggest organization."""
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        if not os.path.exists(downloads_path):
            return
        
        try:
            files = os.listdir(downloads_path)
            recent_files = []
            
            for filename in files:
                filepath = os.path.join(downloads_path, filename)
                
                if filepath in self.downloads_checked:
                    continue
                
                if os.path.isfile(filepath):
                    # Check if file is recent (last 10 minutes)
                    mtime = os.path.getmtime(filepath)
                    if time.time() - mtime < 600:  # 10 minutes
                        recent_files.append(filename)
                        self.downloads_checked.add(filepath)
            
            if recent_files:
                self.add_notification(
                    "New Downloads 📥",
                    f"You have {len(recent_files)} new file(s) in Downloads. Want me to organize them?",
                    priority="low"
                )
        except:
            pass
    
    def _check_work_session(self):
        """Track work session and provide insights."""
        if not self.context_system:
            return
        
        if self.context_system.activity_pattern.is_work_hours():
            if not self.work_session_start:
                self.work_session_start = datetime.now()
            
            # After 4 hours, suggest end of day routine
            session_duration = datetime.now() - self.work_session_start
            if session_duration > timedelta(hours=4):
                self.add_notification(
                    "End of Day 🌅",
                    "You've been working for 4+ hours. Want me to run your end-of-day routine?",
                    priority="normal"
                )
                self.work_session_start = None  # Reset
        else:
            self.work_session_start = None
    
    def _check_meeting_reminders(self):
        """Check for upcoming meetings (placeholder for calendar integration)."""
        # This would integrate with calendar APIs
        # For now, it's a placeholder
        pass
    
    def _show_pending_notifications(self):
        """Show all pending notifications."""
        for notification in self.notifications:
            if not notification.shown:
                notification.show()
    
    def add_notification(
        self,
        title: str,
        message: str,
        priority: str = "normal",
        action: Optional[Callable] = None
    ):
        """Add a new notification."""
        # Check if similar notification already exists
        for notif in self.notifications:
            if notif.title == title and not notif.shown:
                return  # Don't duplicate
        
        notification = SmartNotification(title, message, priority, action)
        self.notifications.append(notification)
        
        # Keep only last 50 notifications
        if len(self.notifications) > 50:
            self.notifications = self.notifications[-50:]
    
    def start(self):
        """Start proactive assistant."""
        if self.is_running:
            return
        
        self.is_running = True
        self._thread = threading.Thread(target=self._check_loop, daemon=True)
        self._thread.start()
        print("[✓] Proactive assistant started")
    
    def stop(self):
        """Stop proactive assistant."""
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=5)
        print("[✓] Proactive assistant stopped")
    
    def get_suggestions(self) -> List[str]:
        """Get current suggestions based on context."""
        suggestions = []
        
        if self.context_system:
            # Get context-based suggestions
            context_suggestions = self.context_system.get_suggestions()
            suggestions.extend(context_suggestions)
        
        return suggestions


class AutoOrganizer:
    """Automatically organizes files based on type and patterns."""
    
    FILE_CATEGORIES = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Code": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css"],
        "Executables": [".exe", ".msi", ".dmg", ".app"],
    }
    
    @staticmethod
    def organize_downloads(dry_run: bool = True) -> Dict:
        """
        Organize files in Downloads folder.
        
        Args:
            dry_run: If True, only show what would be done without moving files
        
        Returns:
            Dictionary with organization results
        """
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        if not os.path.exists(downloads_path):
            return {"error": "Downloads folder not found"}
        
        results = defaultdict(list)
        
        for filename in os.listdir(downloads_path):
            filepath = os.path.join(downloads_path, filename)
            
            if not os.path.isfile(filepath):
                continue
            
            # Determine category
            ext = os.path.splitext(filename)[1].lower()
            category = None
            
            for cat, extensions in AutoOrganizer.FILE_CATEGORIES.items():
                if ext in extensions:
                    category = cat
                    break
            
            if not category:
                category = "Other"
            
            # Create category folder
            category_path = os.path.join(downloads_path, category)
            
            if not dry_run:
                os.makedirs(category_path, exist_ok=True)
                
                # Move file
                new_path = os.path.join(category_path, filename)
                try:
                    os.rename(filepath, new_path)
                    results[category].append(filename)
                except Exception as e:
                    results["errors"].append(f"{filename}: {e}")
            else:
                results[category].append(filename)
        
        return dict(results)
    
    @staticmethod
    def clean_temp_files() -> int:
        """Clean temporary files (placeholder)."""
        # This would clean temp directories
        # Requires careful implementation for safety
        return 0


class PredictiveActions:
    """Predicts and suggests next actions."""
    
    def __init__(self, context_system=None):
        self.context_system = context_system
        self.action_history = []
    
    def predict_next_action(self) -> Optional[str]:
        """Predict what user might want to do next."""
        if not self.context_system:
            return None
        
        context = self.context_system.get_current_context()
        current_app = context.get("current_app")
        
        # Simple prediction based on patterns
        predictions = {
            "chrome.exe": "You might want to search something. Should I open a new tab?",
            "Code.exe": "Working on code? Want me to run your tests?",
            "WINWORD.EXE": "Writing a document? Need me to check grammar?",
        }
        
        return predictions.get(current_app)


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  🤖 Proactive Assistant - Test Mode")
    print("=" * 55)
    
    # Test auto-organizer
    print("\n[Test] Auto-Organizer (dry run):")
    results = AutoOrganizer.organize_downloads(dry_run=True)
    
    for category, files in results.items():
        if files:
            print(f"\n  {category}:")
            for f in files[:5]:
                print(f"    • {f}")
            if len(files) > 5:
                print(f"    ... and {len(files) - 5} more")
    
    # Test proactive assistant
    print("\n\n[Test] Starting Proactive Assistant...")
    assistant = ProactiveAssistant()
    
    # Add some test notifications
    assistant.add_notification(
        "Welcome! 👋",
        "Proactive assistant is now active and monitoring your activity.",
        priority="normal"
    )
    
    assistant.start()
    
    print("\n  Monitoring... (Press Ctrl+C to stop)")
    
    try:
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n[!] Stopping...")
        assistant.stop()
        print("👋 Goodbye!")

"""
System Tray Icon - Always-accessible Christa AI interface
Provides: Quick actions, status indicator, settings access
"""

import sys
import os
import threading
from typing import Optional, Callable

try:
    from PIL import Image, ImageDraw
    import pystray
    from pystray import MenuItem as item
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("[!] System tray requires: pip install pillow pystray")


class ChristaTrayIcon:
    """System tray icon for Christa AI."""
    
    def __init__(
        self,
        on_activate: Optional[Callable] = None,
        on_chat: Optional[Callable] = None,
        on_settings: Optional[Callable] = None
    ):
        """
        Initialize system tray icon.
        
        Args:
            on_activate: Callback when "Activate" is clicked
            on_chat: Callback when "Chat" is clicked
            on_settings: Callback when "Settings" is clicked
        """
        if not PIL_AVAILABLE:
            raise ImportError("System tray requires pillow and pystray")
        
        self.on_activate = on_activate
        self.on_chat = on_chat
        self.on_settings = on_settings
        self.icon = None
        self.is_active = False
        self._thread = None
    
    def _create_icon_image(self, color: str = "blue") -> Image.Image:
        """Create icon image."""
        # Create a simple circular icon
        size = 64
        image = Image.new('RGB', (size, size), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw circle
        colors = {
            "blue": "#4A90E2",
            "green": "#7ED321",
            "red": "#D0021B",
            "gray": "#9B9B9B"
        }
        
        circle_color = colors.get(color, colors["blue"])
        draw.ellipse([8, 8, size-8, size-8], fill=circle_color)
        
        # Draw "C" for Christa
        draw.text((20, 18), "C", fill="white", font=None)
        
        return image
    
    def _create_menu(self):
        """Create context menu."""
        return pystray.Menu(
            item(
                "Christa AI",
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            item(
                "🎤 Activate Voice",
                self._on_activate_clicked,
                default=True
            ),
            item(
                "💬 Open Chat",
                self._on_chat_clicked
            ),
            item(
                "📊 Dashboard",
                self._on_dashboard_clicked
            ),
            pystray.Menu.SEPARATOR,
            item(
                "Quick Actions",
                pystray.Menu(
                    item("📸 Screenshot", self._take_screenshot),
                    item("🔍 Search Files", self._search_files),
                    item("🖥️ Screen Control", self._screen_control),
                )
            ),
            pystray.Menu.SEPARATOR,
            item(
                "⚙️ Settings",
                self._on_settings_clicked
            ),
            item(
                "❌ Exit",
                self._on_exit_clicked
            )
        )
    
    def _on_activate_clicked(self, icon, item):
        """Handle activate click."""
        if self.on_activate:
            threading.Thread(target=self.on_activate, daemon=True).start()
    
    def _on_chat_clicked(self, icon, item):
        """Handle chat click."""
        if self.on_chat:
            threading.Thread(target=self.on_chat, daemon=True).start()
    
    def _on_dashboard_clicked(self, icon, item):
        """Handle dashboard click."""
        print("[Dashboard] Opening dashboard...")
        # This would open a GUI dashboard
    
    def _on_settings_clicked(self, icon, item):
        """Handle settings click."""
        if self.on_settings:
            threading.Thread(target=self.on_settings, daemon=True).start()
    
    def _take_screenshot(self, icon, item):
        """Take screenshot quick action."""
        try:
            import aiscreencontrol_ai
            aiscreencontrol_ai.take_screenshot()
            self.show_notification("Screenshot taken!")
        except Exception as e:
            print(f"[!] Screenshot error: {e}")
    
    def _search_files(self, icon, item):
        """Search files quick action."""
        print("[Quick Action] Opening file search...")
        # This would open file search interface
    
    def _screen_control(self, icon, item):
        """Screen control quick action."""
        print("[Quick Action] Opening screen control...")
        # This would open screen control interface
    
    def _on_exit_clicked(self, icon, item):
        """Handle exit click."""
        print("[Tray] Exiting...")
        self.stop()
    
    def start(self):
        """Start system tray icon."""
        if self.icon:
            return
        
        image = self._create_icon_image("blue")
        menu = self._create_menu()
        
        self.icon = pystray.Icon(
            "christa_ai",
            image,
            "Christa AI",
            menu
        )
        
        # Run in separate thread
        self._thread = threading.Thread(target=self.icon.run, daemon=True)
        self._thread.start()
        
        print("[✓] System tray icon started")
    
    def stop(self):
        """Stop system tray icon."""
        if self.icon:
            self.icon.stop()
            self.icon = None
        print("[✓] System tray icon stopped")
    
    def update_icon(self, color: str = "blue"):
        """Update icon color (e.g., to show status)."""
        if self.icon:
            self.icon.icon = self._create_icon_image(color)
    
    def show_notification(self, message: str, title: str = "Christa AI"):
        """Show system notification."""
        if self.icon:
            self.icon.notify(message, title)


# ─── Simple Text-Based Tray (Fallback) ────────────────────────
class SimpleTrayMenu:
    """Simple text-based menu when GUI tray is not available."""
    
    def __init__(self):
        self.is_running = False
    
    def start(self):
        """Show simple menu."""
        self.is_running = True
        
        print("\n" + "=" * 55)
        print("  🤖 Christa AI - Quick Menu")
        print("=" * 55)
        print("\n  Commands:")
        print("    1. Activate Voice")
        print("    2. Open Chat")
        print("    3. Take Screenshot")
        print("    4. Search Files")
        print("    5. Settings")
        print("    6. Exit")
        print("\n" + "=" * 55)
        
        while self.is_running:
            try:
                choice = input("\n  Choose (1-6): ").strip()
                
                if choice == "1":
                    print("[▶] Activating voice...")
                elif choice == "2":
                    print("[▶] Opening chat...")
                elif choice == "3":
                    try:
                        import aiscreencontrol_ai
                        aiscreencontrol_ai.take_screenshot()
                    except:
                        print("[!] Screenshot failed")
                elif choice == "4":
                    print("[▶] Opening file search...")
                elif choice == "5":
                    print("[▶] Opening settings...")
                elif choice == "6":
                    print("👋 Goodbye!")
                    self.is_running = False
                else:
                    print("[!] Invalid choice")
            
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                self.is_running = False
    
    def stop(self):
        """Stop menu."""
        self.is_running = False


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  🖼️  System Tray Icon - Test Mode")
    print("=" * 55)
    
    if not PIL_AVAILABLE:
        print("\n[!] GUI tray not available. Using simple menu...")
        menu = SimpleTrayMenu()
        menu.start()
    else:
        def on_activate():
            print("\n[Callback] Activate voice triggered!")
        
        def on_chat():
            print("\n[Callback] Chat triggered!")
        
        def on_settings():
            print("\n[Callback] Settings triggered!")
        
        tray = ChristaTrayIcon(
            on_activate=on_activate,
            on_chat=on_chat,
            on_settings=on_settings
        )
        
        tray.start()
        
        print("\n  System tray icon is running")
        print("  Right-click the icon in your system tray")
        print("  Press Ctrl+C to stop\n")
        
        try:
            import time
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n[!] Stopping...")
            tray.stop()
            print("👋 Goodbye!")

"""
AI Screen Control Module - Intelligent Mouse & Keyboard Automation
Uses pyautogui for screen interaction with AI-driven command parsing.
"""

import os
import sys
import time


def _import_pyautogui():
    """Import pyautogui with safety settings."""
    try:
        import pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.3  # Small pause between actions for safety
        return pyautogui
    except ImportError:
        print("[✗] pyautogui not installed. Run: pip install pyautogui")
        sys.exit(1)


def move_mouse(x, y, duration=0.5):
    """Move mouse to screen coordinates with smooth animation."""
    pag = _import_pyautogui()
    screen_w, screen_h = pag.size()
    if 0 <= x <= screen_w and 0 <= y <= screen_h:
        pag.moveTo(x, y, duration=duration)
        print(f"[✓] Mouse moved to ({x}, {y})")
    else:
        print(f"[✗] Coordinates ({x}, {y}) out of screen bounds ({screen_w}x{screen_h})")


def click_at(x, y, clicks=1, button="left"):
    """Click at specific screen coordinates."""
    pag = _import_pyautogui()
    pag.click(x, y, clicks=clicks, button=button)
    print(f"[✓] Clicked at ({x}, {y}) [{button}, {clicks}x]")


def type_text(text, interval=0.03):
    """Type text with a natural typing speed."""
    pag = _import_pyautogui()
    pag.write(text, interval=interval)
    print(f"[✓] Typed: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")


def press_key(key):
    """Press a single key or key combination (e.g., 'enter', 'ctrl+c')."""
    pag = _import_pyautogui()
    if "+" in key:
        keys = [k.strip() for k in key.split("+")]
        pag.hotkey(*keys)
        print(f"[✓] Pressed hotkey: {key}")
    else:
        pag.press(key)
        print(f"[✓] Pressed key: {key}")


def take_screenshot(filepath=None):
    """Take a screenshot and save it."""
    pag = _import_pyautogui()
    if filepath is None:
        filepath = os.path.join(
            os.path.expanduser("~"), "Desktop",
            f"screenshot_{int(time.time())}.png"
        )
    screenshot = pag.screenshot()
    screenshot.save(filepath)
    print(f"[✓] Screenshot saved: {filepath}")
    return filepath


def find_and_click_image(image_path, confidence=0.8):
    """
    Find an image on screen and click on it.
    Requires: pip install opencv-python pyautogui
    """
    pag = _import_pyautogui()
    if not os.path.exists(image_path):
        print(f"[✗] Image not found: {image_path}")
        return False

    try:
        location = pag.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pag.center(location)
            pag.click(center)
            print(f"[✓] Found and clicked image at: {center}")
            return True
        else:
            print(f"[!] Image not found on screen: {image_path}")
            return False
    except Exception as e:
        print(f"[✗] Error finding image: {e}")
        return False


def scroll(amount, x=None, y=None):
    """Scroll the mouse wheel. Positive = up, negative = down."""
    pag = _import_pyautogui()
    pag.scroll(amount, x=x, y=y)
    direction = "up" if amount > 0 else "down"
    print(f"[✓] Scrolled {direction} by {abs(amount)}")


def get_mouse_position():
    """Get current mouse coordinates."""
    pag = _import_pyautogui()
    x, y = pag.position()
    print(f"[✓] Mouse position: ({x}, {y})")
    return x, y


def get_screen_size():
    """Get screen resolution."""
    pag = _import_pyautogui()
    w, h = pag.size()
    print(f"[✓] Screen size: {w} x {h}")
    return w, h


# ─── Command Parser ────────────────────────────────────────────

def parse_and_execute(command):
    """
    Parse a natural-language-like command and execute the appropriate action.
    Supports commands like:
        - "move mouse to 500 300"
        - "click at 100 200"
        - "type Hello World"
        - "press enter"
        - "press ctrl+s"
        - "screenshot"
        - "scroll up 5"
        - "scroll down 3"
        - "where is mouse"
        - "screen size"
    """
    cmd = command.lower().strip()

    if cmd.startswith("move mouse to") or cmd.startswith("move to"):
        parts = cmd.split()
        nums = [p for p in parts if p.isdigit()]
        if len(nums) >= 2:
            move_mouse(int(nums[0]), int(nums[1]))
        else:
            print("[!] Usage: move mouse to <x> <y>")

    elif cmd.startswith("click at") or cmd.startswith("click"):
        parts = cmd.split()
        nums = [p for p in parts if p.isdigit()]
        if len(nums) >= 2:
            click_at(int(nums[0]), int(nums[1]))
        else:
            # Click at current position
            pag = _import_pyautogui()
            pag.click()
            print("[✓] Clicked at current position")

    elif cmd.startswith("double click"):
        parts = cmd.split()
        nums = [p for p in parts if p.isdigit()]
        if len(nums) >= 2:
            click_at(int(nums[0]), int(nums[1]), clicks=2)
        else:
            pag = _import_pyautogui()
            pag.doubleClick()
            print("[✓] Double-clicked at current position")

    elif cmd.startswith("right click"):
        parts = cmd.split()
        nums = [p for p in parts if p.isdigit()]
        if len(nums) >= 2:
            click_at(int(nums[0]), int(nums[1]), button="right")
        else:
            pag = _import_pyautogui()
            pag.rightClick()
            print("[✓] Right-clicked at current position")

    elif cmd.startswith("type "):
        text = command[5:]  # preserve original case
        type_text(text)

    elif cmd.startswith("press "):
        key = cmd[6:].strip()
        press_key(key)

    elif cmd == "screenshot":
        take_screenshot()

    elif cmd.startswith("scroll up"):
        parts = cmd.split()
        amount = int(parts[-1]) if parts[-1].isdigit() else 3
        scroll(amount)

    elif cmd.startswith("scroll down"):
        parts = cmd.split()
        amount = int(parts[-1]) if parts[-1].isdigit() else 3
        scroll(-amount)

    elif cmd in ("where is mouse", "mouse position", "position"):
        get_mouse_position()

    elif cmd in ("screen size", "resolution"):
        get_screen_size()

    else:
        print(f"[?] Unknown command: \"{command}\"")
        print("    Available commands:")
        print("      • move mouse to <x> <y>")
        print("      • click at <x> <y>")
        print("      • double click [x y]")
        print("      • right click [x y]")
        print("      • type <text>")
        print("      • press <key or key+key>")
        print("      • screenshot")
        print("      • scroll up/down [amount]")
        print("      • where is mouse")
        print("      • screen size")


def run_screen_control():
    """Interactive screen control prompt."""
    print("=" * 55)
    print("  🖥️  AI Screen Controller - Ready")
    print("=" * 55)
    print("  ⚠️  SAFETY: Move mouse to any screen corner to abort!")
    print("  Commands: move, click, type, press, screenshot, scroll")
    print("  Type 'exit' to quit")
    print("=" * 55)

    while True:
        try:
            cmd = input("\n🖥️  Command > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Screen control stopped.")
            return

        if cmd.lower() in ("exit", "quit", "stop"):
            print("👋 Screen control stopped.")
            return

        if cmd:
            try:
                parse_and_execute(cmd)
            except Exception as e:
                print(f"[✗] Error: {e}")


if __name__ == "__main__":
    run_screen_control()
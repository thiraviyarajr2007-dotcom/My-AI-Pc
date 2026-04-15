"""
AI in my PC — Unified Launcher
Main entry point to access all AI modules from a single menu.
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MODULES = {
    "1": ("🎙️  Voice AI", "voice_ai.py", "Voice commands to control your PC"),
    "2": ("🖐️  Gesture AI", "gesture_ai.py", "Hand gesture recognition & actions"),
    "3": ("👤 Face Recognition", "facereg_ai.py", "Face detection & identification"),
    "4": ("🔍 File Search", "filesearch_ai.py", "Search files by name, content, size"),
    "5": ("🖥️  Screen Control", "aiscreencontrol_ai.py", "Mouse & keyboard automation"),
    "6": ("💬 AI Chat (Ollama)", "comments_ai.py", "Chat with local LLM via Ollama"),
    "7": ("🎮 PC Control", "control_ai.py", "Open apps, system commands"),
}


def check_dependencies():
    """Check which dependencies are installed."""
    deps = {
        "speech_recognition": "SpeechRecognition",
        "cv2": "opencv-python",
        "mediapipe": "mediapipe",
        "pyautogui": "pyautogui",
        "requests": "requests",
    }
    print("\n  📦 Dependency Status:")
    missing = []
    for module, pip_name in deps.items():
        try:
            __import__(module)
            print(f"    ✅ {pip_name}")
        except ImportError:
            print(f"    ❌ {pip_name} (pip install {pip_name})")
            missing.append(pip_name)

    if missing:
        print(f"\n  Install missing: pip install {' '.join(missing)}")
    else:
        print("\n  ✅ All dependencies installed!")
    return missing


def run_module(key):
    """Launch a module in a subprocess."""
    if key not in MODULES:
        print("[?] Invalid option.")
        return

    name, filename, _ = MODULES[key]
    filepath = os.path.join(SCRIPT_DIR, filename)

    if not os.path.exists(filepath):
        print(f"[✗] Module file not found: {filepath}")
        return

    print(f"\n[▶] Launching {name}...")
    print("-" * 50)

    try:
        subprocess.run([sys.executable, filepath], cwd=SCRIPT_DIR)
    except KeyboardInterrupt:
        print(f"\n[!] {name} interrupted.")
    except Exception as e:
        print(f"[✗] Error running {name}: {e}")

    print("-" * 50)
    print(f"[✓] {name} finished.\n")


def main():
    print()
    print("╔" + "═" * 53 + "╗")
    print("║" + "  🤖 AI in my PC — Unified AI Control System".center(53) + "║")
    print("╚" + "═" * 53 + "╝")

    while True:
        print("\n  Select a module to launch:\n")
        for key, (name, _, desc) in MODULES.items():
            print(f"    [{key}] {name:25s} — {desc}")
        print(f"\n    [D] Check Dependencies")
        print(f"    [Q] Quit")

        try:
            choice = input("\n  ▸ Choose (1-7, D, Q): ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            return

        if choice == "Q":
            print("\n👋 Goodbye!")
            return
        elif choice == "D":
            check_dependencies()
        elif choice in MODULES:
            run_module(choice)
        else:
            print("  [!] Invalid choice. Enter 1-7, D, or Q.")


if __name__ == "__main__":
    main()

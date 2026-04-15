"""
Quick Start Script for Christa AI
Checks everything and launches the best mode for your system
"""

import sys
import os
import subprocess


def print_banner():
    """Print welcome banner."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  🤖 Christa AI - Quick Start".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Download from: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check critical dependencies."""
    critical_deps = {
        "requests": "Core functionality",
        "speech_recognition": "Voice control",
        "pyttsx3": "Voice feedback",
    }
    
    optional_deps = {
        "pyautogui": "Screen automation",
        "cv2": "Vision features",
        "mediapipe": "Gesture control",
        "schedule": "Workflow scheduling",
        "pyperclip": "Clipboard monitoring",
        "psutil": "System monitoring",
    }
    
    print("\n📦 Checking dependencies...")
    
    missing_critical = []
    missing_optional = []
    
    # Check critical
    for module, purpose in critical_deps.items():
        try:
            __import__(module)
            print(f"✅ {module:20s} - {purpose}")
        except ImportError:
            print(f"❌ {module:20s} - {purpose}")
            missing_critical.append(module)
    
    # Check optional
    for module, purpose in optional_deps.items():
        try:
            __import__(module)
            print(f"✅ {module:20s} - {purpose}")
        except ImportError:
            print(f"⚠️  {module:20s} - {purpose} (optional)")
            missing_optional.append(module)
    
    return missing_critical, missing_optional


def check_ollama():
    """Check if Ollama is available."""
    try:
        import requests
        resp = requests.get("http://localhost:11434/api/tags", timeout=2)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            if models:
                print(f"✅ Ollama running with {len(models)} model(s)")
                return True
            else:
                print("⚠️  Ollama running but no models installed")
                print("   Run: ollama pull llama3")
                return False
    except:
        print("❌ Ollama not running")
        print("   Install from: https://ollama.com")
        print("   Then run: ollama pull llama3")
        return False


def check_microphone():
    """Check if microphone is available."""
    try:
        import speech_recognition as sr
        mics = sr.Microphone.list_microphone_names()
        if mics:
            print(f"✅ Microphone detected ({len(mics)} device(s))")
            return True
        else:
            print("⚠️  No microphone detected")
            return False
    except:
        print("⚠️  Cannot check microphone")
        return False


def install_missing(packages):
    """Offer to install missing packages."""
    if not packages:
        return True
    
    print(f"\n📥 Missing packages: {', '.join(packages)}")
    response = input("   Install now? (y/n): ").strip().lower()
    
    if response == 'y':
        print("\n   Installing...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + packages)
            print("   ✅ Installation complete!")
            return True
        except subprocess.CalledProcessError:
            print("   ❌ Installation failed")
            return False
    
    return False


def recommend_mode(has_mic, has_ollama):
    """Recommend best launch mode."""
    print("\n🎯 Recommended mode:")
    
    if has_mic and has_ollama:
        print("   🎤 Voice Mode (with wake word)")
        print("   This is the full experience!")
        return "voice"
    elif has_ollama:
        print("   💬 Chat Mode (text-based)")
        print("   Voice not available, but AI brain works!")
        return "chat"
    else:
        print("   📋 Basic Mode")
        print("   Limited features without Ollama")
        return "basic"


def launch_mode(mode):
    """Launch the recommended mode."""
    print(f"\n🚀 Launching {mode} mode...")
    print("   (Press Ctrl+C to stop)\n")
    print("=" * 60)
    
    try:
        if mode == "voice":
            subprocess.run([sys.executable, "christa_launcher.py", "--mode", "voice"])
        elif mode == "chat":
            subprocess.run([sys.executable, "christa_launcher.py", "--mode", "chat"])
        else:
            subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except FileNotFoundError:
        print("\n❌ Launcher not found. Make sure you're in the correct directory.")


def main():
    """Main quick start flow."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    missing_critical, missing_optional = check_dependencies()
    
    # Offer to install critical dependencies
    if missing_critical:
        if not install_missing(missing_critical):
            print("\n❌ Cannot continue without critical dependencies")
            print("   Install manually: pip install " + " ".join(missing_critical))
            return
    
    # Check Ollama
    print()
    has_ollama = check_ollama()
    
    # Check microphone
    has_mic = check_microphone()
    
    # Recommend mode
    mode = recommend_mode(has_mic, has_ollama)
    
    # Ask to launch
    print("\n" + "=" * 60)
    response = input("\n🚀 Launch Christa AI? (y/n): ").strip().lower()
    
    if response == 'y':
        launch_mode(mode)
    else:
        print("\n📚 To launch later, run:")
        print(f"   python christa_launcher.py --mode {mode}")
        print("\n   Or for interactive menu:")
        print("   python christa_launcher.py")
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Check INSTALLATION_GUIDE.md for help")

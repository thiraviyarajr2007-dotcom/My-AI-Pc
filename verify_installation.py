"""
Christa AI - Complete Installation Verification
Checks all dependencies and features from the roadmap
"""

import sys
import os
from typing import Dict, List, Tuple


def check_python_version() -> bool:
    """Check Python version."""
    version = sys.version_info
    required = (3, 10)
    
    print("\n🐍 Python Version Check:")
    print(f"   Current: {version.major}.{version.minor}.{version.micro}")
    print(f"   Required: {required[0]}.{required[1]}+")
    
    if version >= required:
        print("   ✅ Python version OK")
        return True
    else:
        print(f"   ❌ Python {required[0]}.{required[1]}+ required")
        return False


def check_dependencies() -> Tuple[List[str], List[str]]:
    """Check all dependencies."""
    deps = {
        "Core": {
            "requests": "requests",
            "pyautogui": "pyautogui",
        },
        "Voice": {
            "speech_recognition": "SpeechRecognition",
            "pyttsx3": "pyttsx3",
        },
        "Vision": {
            "cv2": "opencv-python",
            "mediapipe": "mediapipe",
        },
        "Advanced": {
            "schedule": "schedule",
            "pyperclip": "pyperclip",
            "psutil": "psutil",
        },
        "API Server": {
            "flask": "flask",
            "flask_cors": "flask-cors",
            "flask_socketio": "flask-socketio",
            "socketio": "python-socketio",
        },
        "System Tray": {
            "PIL": "pillow",
            "pystray": "pystray",
        }
    }
    
    print("\n📦 Dependency Check:")
    installed = []
    missing = []
    
    for category, modules in deps.items():
        print(f"\n  {category}:")
        for module, pip_name in modules.items():
            try:
                __import__(module)
                print(f"    ✅ {pip_name}")
                installed.append(pip_name)
            except ImportError:
                print(f"    ❌ {pip_name}")
                missing.append(pip_name)
    
    return installed, missing


def check_optional_dependencies() -> Dict[str, bool]:
    """Check optional dependencies."""
    optional = {
        "PyAudio (voice input)": "pyaudio",
        "Whisper (better speech)": "whisper",
        "LangChain (RAG)": "langchain",
        "ChromaDB (vector DB)": "chromadb",
        "PyChromecast (TV)": "pychromecast",
        "Face Recognition": "face_recognition",
    }
    
    print("\n📦 Optional Dependencies:")
    status = {}
    
    for name, module in optional.items():
        try:
            __import__(module)
            print(f"    ✅ {name}")
            status[name] = True
        except ImportError:
            print(f"    ⚠️  {name} (optional)")
            status[name] = False
    
    return status


def check_files() -> Tuple[List[str], List[str]]:
    """Check if all required files exist."""
    required_files = {
        "Core Intelligence": [
            "ai_brain.py",
            "wake_word_detector.py",
            "voice_feedback.py",
        ],
        "Context & Awareness": [
            "context_awareness.py",
            "proactive_assistant.py",
        ],
        "Automation": [
            "workflow_automation.py",
        ],
        "Cross-Device": [
            "api_server.py",
            "mobile_client.py",
        ],
        "Interface": [
            "christa_advanced.py",
            "christa_launcher.py",
            "system_tray.py",
        ],
        "Original Modules": [
            "main.py",
            "voice_ai.py",
            "control_ai.py",
            "aiscreencontrol_ai.py",
            "gesture_ai.py",
            "facereg_ai.py",
            "filesearch_ai.py",
            "comments_ai.py",
        ],
        "Utilities": [
            "quick_start.py",
        ]
    }
    
    print("\n📁 File Check:")
    present = []
    missing = []
    
    for category, files in required_files.items():
        print(f"\n  {category}:")
        for file in files:
            if os.path.exists(file):
                print(f"    ✅ {file}")
                present.append(file)
            else:
                print(f"    ❌ {file}")
                missing.append(file)
    
    return present, missing


def check_ollama() -> bool:
    """Check if Ollama is available."""
    print("\n🤖 Ollama Check:")
    try:
        import requests
        resp = requests.get("http://localhost:11434/api/tags", timeout=2)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            if models:
                print(f"   ✅ Ollama running with {len(models)} model(s)")
                for model in models:
                    print(f"      • {model['name']}")
                return True
            else:
                print("   ⚠️  Ollama running but no models installed")
                print("      Run: ollama pull llama3")
                return False
    except:
        print("   ❌ Ollama not running")
        print("      Install from: https://ollama.com")
        print("      Then run: ollama pull llama3")
        return False


def check_hardware() -> Dict[str, bool]:
    """Check hardware availability."""
    print("\n🎤 Hardware Check:")
    hardware = {}
    
    # Check microphone
    try:
        import speech_recognition as sr
        mics = sr.Microphone.list_microphone_names()
        if mics:
            print(f"   ✅ Microphone detected ({len(mics)} device(s))")
            hardware['microphone'] = True
        else:
            print("   ⚠️  No microphone detected")
            hardware['microphone'] = False
    except:
        print("   ⚠️  Cannot check microphone")
        hardware['microphone'] = False
    
    # Check camera
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("   ✅ Camera detected")
            cap.release()
            hardware['camera'] = True
        else:
            print("   ⚠️  No camera detected")
            hardware['camera'] = False
    except:
        print("   ⚠️  Cannot check camera")
        hardware['camera'] = False
    
    return hardware


def check_features() -> Dict[str, str]:
    """Check which features are available."""
    print("\n✨ Feature Availability:")
    
    features = {
        "Voice Control": "wake_word_detector.py",
        "Voice Feedback": "voice_feedback.py",
        "AI Brain": "ai_brain.py",
        "Context Awareness": "context_awareness.py",
        "Proactive Assistant": "proactive_assistant.py",
        "Workflow Automation": "workflow_automation.py",
        "System Tray": "system_tray.py",
        "API Server": "api_server.py",
        "Mobile Client": "mobile_client.py",
        "Gesture Control": "gesture_ai.py",
        "Face Recognition": "facereg_ai.py",
        "File Search": "filesearch_ai.py",
    }
    
    status = {}
    for feature, file in features.items():
        if os.path.exists(file):
            print(f"   ✅ {feature}")
            status[feature] = "available"
        else:
            print(f"   ❌ {feature}")
            status[feature] = "missing"
    
    return status


def generate_report(
    python_ok: bool,
    installed: List[str],
    missing: List[str],
    files_present: List[str],
    files_missing: List[str],
    ollama_ok: bool,
    hardware: Dict[str, bool],
    features: Dict[str, str]
):
    """Generate installation report."""
    print("\n" + "=" * 60)
    print("📊 INSTALLATION REPORT")
    print("=" * 60)
    
    # Overall status
    all_deps_ok = len(missing) == 0
    all_files_ok = len(files_missing) == 0
    
    print(f"\n✅ Python Version: {'OK' if python_ok else 'FAILED'}")
    print(f"✅ Dependencies: {len(installed)}/{len(installed) + len(missing)} installed")
    print(f"✅ Files: {len(files_present)}/{len(files_present) + len(files_missing)} present")
    print(f"{'✅' if ollama_ok else '⚠️ '} Ollama: {'Running' if ollama_ok else 'Not available'}")
    print(f"{'✅' if hardware.get('microphone') else '⚠️ '} Microphone: {'Available' if hardware.get('microphone') else 'Not detected'}")
    print(f"{'✅' if hardware.get('camera') else '⚠️ '} Camera: {'Available' if hardware.get('camera') else 'Not detected'}")
    
    # Feature summary
    available_features = sum(1 for s in features.values() if s == "available")
    total_features = len(features)
    print(f"\n✨ Features: {available_features}/{total_features} available")
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    if missing:
        print(f"\n   Install missing dependencies:")
        print(f"   pip install {' '.join(missing)}")
    
    if files_missing:
        print(f"\n   Missing files detected:")
        for file in files_missing:
            print(f"   • {file}")
    
    if not ollama_ok:
        print(f"\n   Install Ollama for AI features:")
        print(f"   1. Download from https://ollama.com")
        print(f"   2. Run: ollama pull llama3")
    
    if not hardware.get('microphone'):
        print(f"\n   Connect microphone for voice features")
    
    if not hardware.get('camera'):
        print(f"\n   Connect camera for face/gesture features")
    
    # Ready to use?
    print("\n" + "=" * 60)
    if python_ok and all_deps_ok and all_files_ok:
        print("🎉 READY TO USE!")
        print("\nQuick start:")
        print("   python quick_start.py")
        print("\nOr launch specific mode:")
        print("   python christa_launcher.py --mode voice")
        print("   python christa_launcher.py --mode chat")
        print("   python christa_launcher.py --mode api")
    else:
        print("⚠️  SETUP INCOMPLETE")
        print("\nPlease address the issues above before using Christa AI")
    print("=" * 60)


def main():
    """Main verification function."""
    print("╔" + "═" * 58 + "╗")
    print("║" + "  🔍 Christa AI - Installation Verification".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Run all checks
    python_ok = check_python_version()
    installed, missing = check_dependencies()
    check_optional_dependencies()
    files_present, files_missing = check_files()
    ollama_ok = check_ollama()
    hardware = check_hardware()
    features = check_features()
    
    # Generate report
    generate_report(
        python_ok,
        installed,
        missing,
        files_present,
        files_missing,
        ollama_ok,
        hardware,
        features
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Verification cancelled")
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()

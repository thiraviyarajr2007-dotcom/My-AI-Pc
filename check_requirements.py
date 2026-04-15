#!/usr/bin/env python3
"""
Christa AI - Requirements Verification Script
Tests all dependencies from requirements.txt
"""

import sys
import importlib
import subprocess

def check_module(module_name, display_name=None, import_name=None):
    """Check if a Python module can be imported"""
    if display_name is None:
        display_name = module_name
    if import_name is None:
        import_name = module_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {display_name}")
        return True
    except ImportError as e:
        print(f"❌ {display_name} - {str(e)}")
        return False
    except Exception as e:
        print(f"⚠️  {display_name} - {str(e)}")
        return False

def check_binary(command, display_name):
    """Check if a binary/executable is available"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✅ {display_name}")
            return True
        else:
            print(f"❌ {display_name} - not found")
            return False
    except FileNotFoundError:
        print(f"❌ {display_name} - not installed")
        return False
    except Exception as e:
        print(f"⚠️  {display_name} - {str(e)}")
        return False

print("=" * 70)
print("🔍 CHRISTA AI - DEPENDENCY VERIFICATION")
print("=" * 70)

results = {"passed": 0, "failed": 0, "warnings": 0}

# Core
print("\n🆓 CORE DEPENDENCIES")
print("-" * 70)
if check_module("requests"): results["passed"] += 1
else: results["failed"] += 1
if check_module("pyautogui"): results["passed"] += 1
else: results["failed"] += 1

# Voice System
print("\n🎤 VOICE SYSTEM")
print("-" * 70)
if check_module("whisper", "openai-whisper"): results["passed"] += 1
else: results["failed"] += 1
if check_module("speech_recognition", "SpeechRecognition"): results["passed"] += 1
else: results["failed"] += 1
if check_module("pyttsx3"): results["passed"] += 1
else: results["failed"] += 1
if check_module("pyaudio"): results["passed"] += 1
else: results["failed"] += 1

# Vision System
print("\n👁️  VISION SYSTEM")
print("-" * 70)
if check_module("cv2", "opencv-python"): results["passed"] += 1
else: results["failed"] += 1
if check_module("mediapipe"): results["passed"] += 1
else: results["failed"] += 1
if check_module("pytesseract"): results["passed"] += 1
else: results["failed"] += 1

# Check Tesseract binary
if check_binary("tesseract", "Tesseract OCR (binary)"): results["passed"] += 1
else: results["failed"] += 1

if check_module("ultralytics", "ultralytics (YOLOv8)"): results["passed"] += 1
else: results["failed"] += 1

# AI Brain
print("\n🧠 AI BRAIN")
print("-" * 70)
if check_module("sentence_transformers", "sentence-transformers"): results["passed"] += 1
else: results["failed"] += 1
if check_module("faiss", "faiss-cpu"): results["passed"] += 1
else: results["failed"] += 1
if check_module("langchain"): results["passed"] += 1
else: results["failed"] += 1
if check_module("langchain_community", "langchain-community"): results["passed"] += 1
else: results["failed"] += 1

# Check Ollama
if check_binary("ollama", "Ollama (binary)"): results["passed"] += 1
else: results["failed"] += 1

# Memory System
print("\n💾 MEMORY SYSTEM")
print("-" * 70)
if check_module("sqlite3", "SQLite (built-in)"): results["passed"] += 1
else: results["failed"] += 1

# Cross-Device API
print("\n🌐 CROSS-DEVICE API")
print("-" * 70)
if check_module("flask", "Flask"): results["passed"] += 1
else: results["failed"] += 1
if check_module("flask_cors", "flask-cors"): results["passed"] += 1
else: results["failed"] += 1
if check_module("flask_socketio", "flask-socketio"): results["passed"] += 1
else: results["failed"] += 1
if check_module("socketio", "python-socketio"): results["passed"] += 1
else: results["failed"] += 1
if check_module("fastapi", "FastAPI"): results["passed"] += 1
else: results["failed"] += 1
if check_module("uvicorn"): results["passed"] += 1
else: results["failed"] += 1
if check_module("websockets"): results["passed"] += 1
else: results["failed"] += 1

# Security
print("\n🔐 SECURITY")
print("-" * 70)
if check_module("cryptography"): results["passed"] += 1
else: results["failed"] += 1

# Utilities
print("\n🛠️  UTILITIES")
print("-" * 70)
if check_module("schedule"): results["passed"] += 1
else: results["failed"] += 1
if check_module("pyperclip"): results["passed"] += 1
else: results["failed"] += 1
if check_module("psutil"): results["passed"] += 1
else: results["failed"] += 1

# Windows-specific
if sys.platform == "win32":
    if check_module("win32api", "pywin32", "win32api"): results["passed"] += 1
    else: results["failed"] += 1
else:
    print("⏭️  pywin32 (Windows only - skipped)")

if check_module("PIL", "Pillow"): results["passed"] += 1
else: results["failed"] += 1
if check_module("pystray"): results["passed"] += 1
else: results["failed"] += 1

# Summary
print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"✅ Passed: {results['passed']}")
print(f"❌ Failed: {results['failed']}")
print(f"⚠️  Warnings: {results['warnings']}")
print()

if results['failed'] == 0:
    print("🎉 All dependencies are working!")
    sys.exit(0)
else:
    print("⚠️  Some dependencies are missing. Install them with:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

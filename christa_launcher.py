"""
Christa AI - Complete Advanced Launcher
Integrates all advanced features with easy access
"""

import os
import sys
import time
import argparse
from typing import Optional


def check_dependencies():
    """Check and report on installed dependencies."""
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
        }
    }
    
    print("\n📦 Dependency Check:")
    all_installed = True
    missing = []
    
    for category, modules in deps.items():
        print(f"\n  {category}:")
        for module, pip_name in modules.items():
            try:
                __import__(module)
                print(f"    ✅ {pip_name}")
            except ImportError:
                print(f"    ❌ {pip_name}")
                missing.append(pip_name)
                all_installed = False
    
    if missing:
        print(f"\n  Install missing: pip install {' '.join(missing)}")
    else:
        print("\n  ✅ All dependencies installed!")
    
    return all_installed


def launch_basic_system():
    """Launch basic Christa AI (original modules)."""
    print("\n[▶] Launching Basic Christa AI...")
    import main
    main.main()


def launch_advanced_voice():
    """Launch advanced voice system with wake word."""
    print("\n[▶] Launching Advanced Voice System...")
    try:
        from christa_advanced import ChristaAdvanced
        christa = ChristaAdvanced(enable_voice_feedback=True)
        christa.start()
    except ImportError as e:
        print(f"[✗] Could not launch: {e}")
        print("    Make sure all advanced modules are present")


def launch_chat_mode():
    """Launch text-based chat mode."""
    print("\n[▶] Launching Chat Mode...")
    try:
        from christa_advanced import ChristaAdvanced
        christa = ChristaAdvanced(enable_voice_feedback=True)
        christa.chat_mode()
    except ImportError as e:
        print(f"[✗] Could not launch: {e}")


def launch_workflow_builder():
    """Launch workflow automation builder."""
    print("\n[▶] Launching Workflow Builder...")
    try:
        import workflow_automation
        manager = workflow_automation.WorkflowManager()
        
        print("\n" + "=" * 55)
        print("  🔄 Workflow Automation")
        print("=" * 55)
        print("\n  Commands:")
        print("    • 'list' - List workflows")
        print("    • 'record <name>' - Start recording")
        print("    • 'stop' - Stop recording")
        print("    • 'execute <name>' - Execute workflow")
        print("    • 'exit' - Quit")
        print("\n" + "=" * 55)
        
        while True:
            try:
                cmd = input("\n🔄 > ").strip()
                if not cmd:
                    continue
                
                if cmd == "exit":
                    break
                
                parts = cmd.split(maxsplit=1)
                action = parts[0].lower()
                
                if action == "list":
                    manager.list_workflows()
                elif action == "record" and len(parts) > 1:
                    manager.recorder.start_recording(parts[1])
                elif action == "stop":
                    wf = manager.recorder.stop_recording()
                    if wf:
                        manager.save_workflow(wf)
                elif action == "execute" and len(parts) > 1:
                    if parts[1] in manager.workflows:
                        manager.executor.execute(manager.workflows[parts[1]])
                else:
                    print("[!] Unknown command")
            
            except (EOFError, KeyboardInterrupt):
                break
        
        print("\n👋 Workflow builder closed")
    
    except ImportError as e:
        print(f"[✗] Could not launch: {e}")


def launch_context_monitor():
    """Launch context awareness monitor."""
    print("\n[▶] Launching Context Monitor...")
    try:
        from context_awareness import ContextAwarenessSystem
        from datetime import datetime
        
        context = ContextAwarenessSystem(update_interval=2.0)
        context.start()
        
        print("\n  Monitoring your activity...")
        print("  Press Ctrl+C to stop and see summary\n")
        
        try:
            while True:
                time.sleep(5)
                ctx = context.get_current_context()
                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] {ctx['active_window']}", end="")
        
        except KeyboardInterrupt:
            print("\n\n[!] Stopping...")
            context.stop()
            
            # Show summary
            ctx = context.get_current_context()
            print("\n📊 Activity Summary:")
            print(f"\n  Most used applications:")
            for app, duration in ctx["most_used_apps"]:
                minutes = int(duration / 60)
                print(f"    • {app}: {minutes} minutes")
            
            print("\n👋 Context monitor closed")
    
    except ImportError as e:
        print(f"[✗] Could not launch: {e}")


def launch_system_tray():
    """Launch system tray icon."""
    print("\n[▶] Launching System Tray...")
    try:
        from system_tray import ChristaTrayIcon, SimpleTrayMenu, PIL_AVAILABLE
        
        if not PIL_AVAILABLE:
            print("[!] GUI tray not available. Using simple menu...")
            menu = SimpleTrayMenu()
            menu.start()
        else:
            tray = ChristaTrayIcon()
            tray.start()
            
            print("\n  System tray icon is running")
            print("  Right-click the icon in your system tray")
            print("  Press Ctrl+C to stop\n")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                tray.stop()
                print("\n👋 System tray closed")
    
    except ImportError as e:
        print(f"[✗] Could not launch: {e}")


def launch_ai_brain_test():
    """Test AI brain functionality."""
    print("\n[▶] Launching AI Brain Test...")
    try:
        from ai_brain import AIBrain
        
        brain = AIBrain()
        
        print("\n" + "=" * 55)
        print("  🧠 AI Brain Test")
        print("=" * 55)
        
        if brain.ollama_available:
            print("  ✅ Ollama connected")
        else:
            print("  ⚠️  Ollama not available (using fallback)")
        
        print("\n  Test commands:")
        print("    • 'open chrome'")
        print("    • 'find my documents'")
        print("    • 'take a screenshot'")
        print("    • Type 'exit' to quit")
        print("\n" + "=" * 55)
        
        while True:
            try:
                user_input = input("\n👤 You > ").strip()
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                result = brain.process_input(user_input)
                print(f"\n🧠 Intent: {result['intent']} ({result['confidence']:.0%})")
                print(f"🤖 Christa: {result['response']}")
                
                if result['action']['module']:
                    print(f"⚡ Action: {result['action']['module']}.{result['action']['function']}")
            
            except (EOFError, KeyboardInterrupt):
                break
        
        print("\n👋 AI brain test closed")
    
    except ImportError as e:
        print(f"[✗] Could not launch: {e}")


def launch_api_server():
    """Launch cross-device API server."""
    print("\n[▶] Launching API Server...")
    try:
        import api_server
        api_server.run_server(host='0.0.0.0', port=5000, debug=False)
    except ImportError as e:
        print(f"[✗] Could not launch: {e}")
        print("    Make sure Flask is installed: pip install flask flask-cors flask-socketio")


def main():
    """Main launcher interface."""
    parser = argparse.ArgumentParser(
        description="Christa AI - Advanced Personal Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python christa_launcher.py --mode voice    # Launch with wake word
  python christa_launcher.py --mode chat     # Launch chat mode
  python christa_launcher.py --check-deps    # Check dependencies
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["basic", "voice", "chat", "workflow", "context", "tray", "brain", "api"],
        help="Launch mode"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check dependencies and exit"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  🤖 Christa AI - Advanced Personal Assistant".center(58) + "║")
    print("║" + "  Your Intelligent Laptop Copilot".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Check dependencies if requested
    if args.check_deps:
        check_dependencies()
        return
    
    # Launch specific mode if provided
    if args.mode:
        modes = {
            "basic": launch_basic_system,
            "voice": launch_advanced_voice,
            "chat": launch_chat_mode,
            "workflow": launch_workflow_builder,
            "context": launch_context_monitor,
            "tray": launch_system_tray,
            "brain": launch_ai_brain_test,
            "api": launch_api_server,
        }
        modes[args.mode]()
        return
    
    # Show interactive menu
    while True:
        print("\n  🚀 Launch Options:")
        print()
        print("    [1] 🎤 Advanced Voice Mode (with wake word)")
        print("    [2] 💬 Chat Mode (text-based)")
        print("    [3] 📋 Basic System (original modules)")
        print("    [4] 🔄 Workflow Builder")
        print("    [5] 👁️  Context Monitor")
        print("    [6] 🖼️  System Tray")
        print("    [7] 🧠 AI Brain Test")
        print("    [8] 🌐 API Server (cross-device)")
        print()
        print("    [D] 📦 Check Dependencies")
        print("    [Q] ❌ Quit")
        print()
        
        try:
            choice = input("  ▸ Choose (1-8, D, Q): ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            return
        
        if choice == "Q":
            print("\n👋 Goodbye!")
            return
        elif choice == "D":
            check_dependencies()
        elif choice == "1":
            launch_advanced_voice()
        elif choice == "2":
            launch_chat_mode()
        elif choice == "3":
            launch_basic_system()
        elif choice == "4":
            launch_workflow_builder()
        elif choice == "5":
            launch_context_monitor()
        elif choice == "6":
            launch_system_tray()
        elif choice == "7":
            launch_ai_brain_test()
        elif choice == "8":
            launch_api_server()
        else:
            print("  [!] Invalid choice")


if __name__ == "__main__":
    main()

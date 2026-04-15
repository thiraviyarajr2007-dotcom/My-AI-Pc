"""
Christa AI - Advanced Integrated System
Combines: Wake word detection, AI brain, voice feedback, and all modules
"""

import os
import sys
import time
import threading
from typing import Optional

# Import core modules
try:
    from ai_brain import AIBrain
    from wake_word_detector import ContinuousVoiceAssistant
    from voice_feedback import VoiceFeedback
    import control_ai
    import aiscreencontrol_ai
    import filesearch_ai
except ImportError as e:
    print(f"[✗] Missing module: {e}")
    print("    Make sure all required files are in the same directory")
    sys.exit(1)


class ChristaAdvanced:
    """Advanced Christa AI with full integration."""
    
    def __init__(self, enable_voice_feedback: bool = True):
        """Initialize Christa Advanced system."""
        print("=" * 60)
        print("  🤖 Christa AI - Advanced System")
        print("=" * 60)
        
        # Initialize components
        print("\n[⏳] Initializing AI Brain...")
        self.brain = AIBrain()
        
        print("[⏳] Initializing Voice Feedback...")
        self.voice = VoiceFeedback() if enable_voice_feedback else None
        
        print("[⏳] Initializing Wake Word Detector...")
        self.assistant = ContinuousVoiceAssistant(on_command=self.handle_command)
        
        self.is_running = False
        
        print("\n[✓] Christa AI initialized successfully!")
        print("=" * 60)
    
    def handle_command(self, command: str):
        """Process voice command through AI brain."""
        print(f"\n🗣️  You said: '{command}'")
        
        # Process through AI brain
        result = self.brain.process_input(command)
        
        print(f"🧠 Intent: {result['intent']} ({result['confidence']:.0%} confidence)")
        print(f"🤖 Christa: {result['response']}")
        
        # Speak response
        if self.voice:
            self.voice.speak_async(result['response'])
        
        # Execute action
        self._execute_action(result['action'])
    
    def _execute_action(self, action: dict):
        """Execute the determined action."""
        if not action or not action.get('module'):
            return
        
        module_name = action['module']
        function_name = action['function']
        params = action['params']
        
        print(f"⚡ Executing: {module_name}.{function_name}")
        
        try:
            if module_name == "control_ai":
                if function_name == "open_app":
                    app_name = params.get('app_name', '')
                    control_ai.open_app(app_name)
                elif function_name == "run_system_command":
                    cmd = params.get('command', '')
                    control_ai.run_system_command(cmd)
            
            elif module_name == "aiscreencontrol_ai":
                if function_name == "take_screenshot":
                    aiscreencontrol_ai.take_screenshot()
                elif function_name == "type_text":
                    text = params.get('text', '')
                    aiscreencontrol_ai.type_text(text)
                elif function_name == "parse_and_execute":
                    # This would need the full command
                    pass
            
            elif module_name == "filesearch_ai":
                if function_name == "search_by_name":
                    query = params.get('query', '')
                    results = filesearch_ai.search_by_name(query, max_results=5)
                    print(f"[✓] Found {len(results)} files")
                    for r in results[:3]:
                        print(f"    • {r['name']}")
        
        except Exception as e:
            print(f"[✗] Action execution error: {e}")
            if self.voice:
                self.voice.speak_async("Sorry, I encountered an error.")
    
    def start(self):
        """Start Christa AI system."""
        self.is_running = True
        
        print("\n🎤 Say 'Hey Christa' to activate")
        print("   Press Ctrl+C to stop\n")
        
        # Greet user
        if self.voice:
            self.voice.speak("Hello! I'm Christa. Say Hey Christa to activate me.")
        
        # Start wake word detection
        self.assistant.start()
        
        try:
            # Keep main thread alive
            while self.is_running:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n[!] Stopping Christa AI...")
            self.stop()
    
    def stop(self):
        """Stop Christa AI system."""
        self.is_running = False
        self.assistant.stop()
        
        if self.voice:
            self.voice.speak("Goodbye!")
            time.sleep(1)
        
        print("👋 Christa AI stopped. Goodbye!")
    
    def chat_mode(self):
        """Interactive chat mode (text-based)."""
        print("\n💬 Chat Mode - Type your commands")
        print("   Type 'voice' to switch to voice mode")
        print("   Type 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("👤 You > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                if self.voice:
                    self.voice.speak("Goodbye!")
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == "voice":
                print("\n[▶] Switching to voice mode...")
                self.start()
                break
            
            # Process command
            result = self.brain.process_input(user_input)
            print(f"🤖 Christa: {result['response']}")
            
            if self.voice:
                self.voice.speak_async(result['response'])
            
            self._execute_action(result['action'])


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Christa AI - Advanced System")
    parser.add_argument(
        "--mode",
        choices=["voice", "chat"],
        default="voice",
        help="Start mode: voice (wake word) or chat (text)"
    )
    parser.add_argument(
        "--no-voice-feedback",
        action="store_true",
        help="Disable voice feedback (text only)"
    )
    
    args = parser.parse_args()
    
    # Initialize Christa
    christa = ChristaAdvanced(enable_voice_feedback=not args.no_voice_feedback)
    
    # Start in selected mode
    if args.mode == "voice":
        christa.start()
    else:
        christa.chat_mode()


if __name__ == "__main__":
    main()

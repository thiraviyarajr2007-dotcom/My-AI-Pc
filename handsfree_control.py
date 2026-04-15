"""
Hands-Free PC Control System
Complete touchless control using voice, gestures, and face recognition
"""

import os
import sys
import threading
import time
import queue
from datetime import datetime
from typing import Optional, Dict, List

# Import all control modules
try:
    from ai_brain import AIBrain
    from memory_system import MemorySystem
    from whisper_voice_enhanced import HybridVoiceEnhanced
    import control_ai
    import filesearch_ai
    import aiscreencontrol_ai
    from workflow_automation import WorkflowManager
    from context_awareness import ContextAwarenessSystem
    
    # Optional modules
    try:
        import gesture_ai
        GESTURE_AVAILABLE = True
    except ImportError:
        GESTURE_AVAILABLE = False
        print("[!] Gesture AI not available")
    
    try:
        import facereg_ai
        FACE_AVAILABLE = True
    except ImportError:
        FACE_AVAILABLE = False
        print("[!] Face recognition not available")
        
except ImportError as e:
    print(f"[!] Import error: {e}")
    sys.exit(1)


class HandsFreeController:
    """Main hands-free control system."""
    
    def __init__(self):
        self.running = False
        self.command_queue = queue.Queue()
        
        # Initialize components
        print("[🤖] Initializing Hands-Free Control System...")
        
        self.memory = MemorySystem()
        print("[✓] Memory system ready")
        
        self.brain = AIBrain(use_sqlite=True)
        print("[✓] AI Brain ready")
        
        self.voice = HybridVoiceEnhanced(prefer_offline=True, model_size="small")
        print("[✓] Voice system ready")
        
        self.workflow_manager = WorkflowManager()
        print("[✓] Workflow manager ready")
        
        self.context_system = ContextAwarenessSystem(update_interval=3.0)
        print("[✓] Context awareness ready")
        
        # Control modes
        self.voice_enabled = True
        self.gesture_enabled = GESTURE_AVAILABLE
        self.face_enabled = FACE_AVAILABLE
        
        # Threads
        self.voice_thread = None
        self.gesture_thread = None
        self.face_thread = None
        self.executor_thread = None
        
        print("[✓] Hands-Free Control System initialized!")
    
    def start(self):
        """Start all control systems."""
        if self.running:
            print("[!] Already running")
            return
        
        self.running = True
        
        # Start context awareness
        self.context_system.start()
        
        # Start command executor
        self.executor_thread = threading.Thread(target=self._command_executor, daemon=True)
        self.executor_thread.start()
        
        # Start voice control
        if self.voice_enabled:
            self.voice_thread = threading.Thread(target=self._voice_loop, daemon=True)
            self.voice_thread.start()
            print("[✓] Voice control started")
        
        # Start gesture control
        if self.gesture_enabled:
            self.gesture_thread = threading.Thread(target=self._gesture_loop, daemon=True)
            self.gesture_thread.start()
            print("[✓] Gesture control started")
        
        # Start face recognition
        if self.face_enabled:
            self.face_thread = threading.Thread(target=self._face_loop, daemon=True)
            self.face_thread.start()
            print("[✓] Face recognition started")
        
        print("\n[🎉] All systems active! You can now control your PC hands-free!")
        self._print_instructions()
    
    def stop(self):
        """Stop all control systems."""
        print("\n[⏹️] Stopping hands-free control...")
        self.running = False
        self.context_system.stop()
        time.sleep(1)
        print("[✓] Hands-free control stopped")
    
    def _voice_loop(self):
        """Continuous voice listening loop."""
        print("[🎤] Voice control active - speak commands...")
        
        while self.running:
            try:
                # Listen for voice input
                text = self.voice.listen(timeout=5, auto_stop=True)
                
                if text:
                    print(f"\n[🗣️] You said: {text}")
                    self.command_queue.put({
                        'type': 'voice',
                        'command': text,
                        'timestamp': datetime.now()
                    })
                
                time.sleep(0.5)
            
            except Exception as e:
                print(f"[!] Voice error: {e}")
                time.sleep(2)
    
    def _gesture_loop(self):
        """Continuous gesture recognition loop."""
        if not GESTURE_AVAILABLE:
            return
        
        print("[🖐️] Gesture control active - use hand gestures...")
        
        import cv2
        import mediapipe as mp
        
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[!] Cannot open camera for gestures")
            return
        
        prev_gesture = -1
        gesture_hold_count = 0
        TRIGGER_THRESHOLD = 15
        
        while self.running:
            try:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        finger_count = gesture_ai.count_fingers(hand_landmarks, mp_hands, "Right")
                        
                        if finger_count == prev_gesture:
                            gesture_hold_count += 1
                        else:
                            gesture_hold_count = 0
                            prev_gesture = finger_count
                        
                        if gesture_hold_count == TRIGGER_THRESHOLD:
                            gesture_name = gesture_ai.detect_gesture(finger_count)
                            print(f"\n[🖐️] Gesture detected: {gesture_name}")
                            
                            self.command_queue.put({
                                'type': 'gesture',
                                'fingers': finger_count,
                                'gesture': gesture_name,
                                'timestamp': datetime.now()
                            })
                            
                            gesture_hold_count = 0
                
                if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
                    break
            
            except Exception as e:
                print(f"[!] Gesture error: {e}")
                time.sleep(2)
        
        cap.release()
        hands.close()
    
    def _face_loop(self):
        """Continuous face recognition loop."""
        if not FACE_AVAILABLE:
            return
        
        print("[👤] Face recognition active...")
        
        # This would run face recognition
        # For now, we'll keep it simple
        while self.running:
            try:
                # Face recognition logic here
                time.sleep(5)
            except Exception as e:
                print(f"[!] Face recognition error: {e}")
                time.sleep(2)
    
    def _command_executor(self):
        """Execute commands from the queue."""
        while self.running:
            try:
                if not self.command_queue.empty():
                    cmd = self.command_queue.get(timeout=1)
                    self._execute_command(cmd)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"[!] Executor error: {e}")
            
            time.sleep(0.1)
    
    def _execute_command(self, cmd: Dict):
        """Execute a command based on type."""
        cmd_type = cmd.get('type')
        
        try:
            if cmd_type == 'voice':
                self._execute_voice_command(cmd['command'])
            
            elif cmd_type == 'gesture':
                self._execute_gesture_command(cmd['fingers'])
            
            elif cmd_type == 'face':
                self._execute_face_command(cmd)
        
        except Exception as e:
            print(f"[!] Command execution error: {e}")
    
    def _execute_voice_command(self, text: str):
        """Execute voice command."""
        # Process with AI brain
        result = self.brain.process_input(text)
        
        print(f"[🤖] Intent: {result['intent']} ({result['confidence']*100:.0f}%)")
        print(f"[💬] Response: {result['response']}")
        
        # Execute action
        intent = result['intent']
        
        if intent == 'open_app':
            # Extract app name from text
            text_lower = text.lower()
            for app in control_ai.APP_COMMANDS.keys():
                if app in text_lower:
                    control_ai.open_app(app)
                    return
        
        elif intent == 'system_command':
            # Check for system commands
            text_lower = text.lower()
            for cmd in control_ai.SYSTEM_COMMANDS.keys():
                if cmd in text_lower:
                    control_ai.run_system_command(cmd)
                    return
        
        elif intent == 'search_files':
            # Extract search query
            if 'find' in text.lower() or 'search' in text.lower():
                words = text.split()
                if len(words) > 1:
                    query = ' '.join(words[1:])
                    results = filesearch_ai.search_by_name(query, max_results=5)
                    print(f"[📁] Found {len(results)} files")
                    for r in results[:3]:
                        print(f"    • {r['name']}")
        
        elif intent == 'take_screenshot':
            aiscreencontrol_ai.take_screenshot()
        
        elif intent == 'control_mouse':
            # Parse mouse commands
            if 'click' in text.lower():
                aiscreencontrol_ai.parse_and_execute('click')
            elif 'move' in text.lower():
                aiscreencontrol_ai.parse_and_execute(text)
        
        else:
            # Try to parse as general command
            control_ai.parse_command(text)
    
    def _execute_gesture_command(self, fingers: int):
        """Execute gesture command."""
        gesture_actions = {
            0: None,  # Fist - no action
            1: lambda: control_ai.open_app('chrome'),  # Point - open Chrome
            2: lambda: aiscreencontrol_ai.take_screenshot(),  # Peace - screenshot
            3: lambda: control_ai.open_app('notepad'),  # Three - open Notepad
            4: lambda: control_ai.open_app('calculator'),  # Four - calculator
            5: lambda: control_ai.open_app('file explorer'),  # Open palm - explorer
        }
        
        action = gesture_actions.get(fingers)
        if action:
            action()
    
    def _execute_face_command(self, cmd: Dict):
        """Execute face recognition command."""
        # Face-based commands (e.g., unlock, personalization)
        pass
    
    def _print_instructions(self):
        """Print usage instructions."""
        print("\n" + "=" * 60)
        print("  🎮 HANDS-FREE CONTROL ACTIVE")
        print("=" * 60)
        
        if self.voice_enabled:
            print("\n  🎤 VOICE COMMANDS:")
            print("    • 'open chrome' - Open Chrome browser")
            print("    • 'open notepad' - Open Notepad")
            print("    • 'find my documents' - Search files")
            print("    • 'take screenshot' - Capture screen")
            print("    • 'lock screen' - Lock computer")
            print("    • 'volume up/down' - Control volume")
            print("    • 'click' - Click mouse")
            print("    • 'move mouse to 500 300' - Move mouse")
        
        if self.gesture_enabled:
            print("\n  🖐️ HAND GESTURES:")
            print("    • 0 fingers (Fist) - No action")
            print("    • 1 finger (Point) - Open Chrome")
            print("    • 2 fingers (Peace) - Take screenshot")
            print("    • 3 fingers - Open Notepad")
            print("    • 4 fingers - Open Calculator")
            print("    • 5 fingers (Open palm) - Open File Explorer")
        
        print("\n  ⌨️ KEYBOARD:")
        print("    • Press 'Q' to quit")
        print("    • Press 'V' to toggle voice")
        print("    • Press 'G' to toggle gestures")
        
        print("\n" + "=" * 60)
        print("  Control your PC without touching keyboard!")
        print("=" * 60 + "\n")


def main():
    """Main entry point."""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║        🤖 HANDS-FREE PC CONTROL SYSTEM 🤖                 ║")
    print("║                                                            ║")
    print("║     Control your PC using Voice, Gestures & Face!         ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    controller = HandsFreeController()
    
    try:
        controller.start()
        
        # Keep running until user quits
        print("\n[ℹ️] Press Ctrl+C to stop\n")
        
        while controller.running:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    
    finally:
        controller.stop()
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()

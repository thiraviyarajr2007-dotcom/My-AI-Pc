"""
Christa AI - Complete Enhanced System
All modules linked, all issues debugged, production-ready
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import os
import uuid
import threading
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

# Import all Christa components
try:
    from ai_brain import AIBrain
    from memory_system import MemorySystem
    from whisper_voice_enhanced import HybridVoiceEnhanced
    import control_ai
    import filesearch_ai
    import aiscreencontrol_ai
    from workflow_automation import WorkflowManager
    from context_awareness import ContextAwarenessSystem
    
    MODULES_LOADED = True
except ImportError as e:
    print(f"[!] Import error: {e}")
    MODULES_LOADED = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'christa-complete-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global components
brain = None
memory = None
voice = None
workflow_manager = None
context_system = None
active_sessions = {}
ollama_process = None


def check_ollama():
    """Check if Ollama is running."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def start_ollama():
    """Start Ollama server if not running."""
    global ollama_process
    
    if check_ollama():
        print("[✓] Ollama already running")
        return True
    
    print("[⏳] Starting Ollama server...")
    try:
        # Start Ollama in background
        ollama_process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Wait for Ollama to start
        for i in range(10):
            time.sleep(1)
            if check_ollama():
                print("[✓] Ollama started successfully")
                return True
        
        print("[!] Ollama started but not responding")
        return False
    
    except FileNotFoundError:
        print("[!] Ollama not installed. Install from: https://ollama.ai")
        return False
    except Exception as e:
        print(f"[!] Error starting Ollama: {e}")
        return False


def initialize_components():
    """Initialize all AI components with error handling."""
    global brain, memory, voice, workflow_manager, context_system
    
    print("\n" + "=" * 60)
    print("  🤖 Initializing Christa AI Complete System")
    print("=" * 60 + "\n")
    
    # Start Ollama first
    ollama_running = start_ollama()
    
    # Initialize Memory System
    try:
        memory = MemorySystem()
        print("[✓] Memory system initialized")
    except Exception as e:
        print(f"[!] Memory system error: {e}")
        memory = None
    
    # Initialize AI Brain
    try:
        brain = AIBrain(use_sqlite=True)
        if brain.ollama_available:
            print(f"[✓] AI Brain initialized (Ollama: {brain.model})")
        else:
            print("[✓] AI Brain initialized (Fallback mode)")
    except Exception as e:
        print(f"[!] AI Brain error: {e}")
        brain = None
    
    # Initialize Voice System
    try:
        voice = HybridVoiceEnhanced(prefer_offline=True, model_size="small")
        print("[✓] Voice system initialized (Whisper small)")
    except Exception as e:
        print(f"[!] Voice system error: {e}")
        voice = None
    
    # Initialize Workflow Manager
    try:
        workflow_manager = WorkflowManager()
        print(f"[✓] Workflow manager initialized ({len(workflow_manager.workflows)} workflows)")
    except Exception as e:
        print(f"[!] Workflow manager error: {e}")
        workflow_manager = None
    
    # Initialize Context Awareness
    try:
        if os.name == 'nt':  # Windows only
            context_system = ContextAwarenessSystem(update_interval=3.0)
            context_system.start()
            print("[✓] Context awareness started")
        else:
            print("[!] Context awareness (Windows only)")
            context_system = None
    except Exception as e:
        print(f"[!] Context awareness error: {e}")
        context_system = None
    
    print("\n[✓] Christa AI Complete System ready!")
    print("=" * 60 + "\n")


@app.route('/')
def index():
    """Main interface."""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get comprehensive system status."""
    status = {
        'brain': brain is not None,
        'brain_ollama': brain.ollama_available if brain else False,
        'memory': memory is not None,
        'voice': voice is not None,
        'voice_whisper': voice.whisper_available if voice else False,
        'workflows': workflow_manager is not None,
        'context': context_system is not None and context_system.is_running if context_system else False,
        'ollama_running': check_ollama(),
        'modules_loaded': MODULES_LOADED
    }
    return jsonify(status)


@app.route('/api/stats')
def get_stats():
    """Get comprehensive statistics."""
    stats = {}
    
    if brain and brain.use_sqlite:
        try:
            stats['brain'] = brain.get_statistics()
            stats['most_used'] = brain.get_most_used_commands(limit=5)
        except:
            stats['brain'] = {'total_commands': 0, 'successful_commands': 0}
            stats['most_used'] = []
    
    if workflow_manager:
        try:
            stats['workflows'] = {
                'total': len(workflow_manager.workflows),
                'list': [
                    {
                        'name': w.name,
                        'actions': len(w.actions),
                        'executions': w.execution_count
                    }
                    for w in list(workflow_manager.workflows.values())[:5]
                ]
            }
        except:
            stats['workflows'] = {'total': 0, 'list': []}
    
    if context_system:
        try:
            context = context_system.get_current_context()
            stats['context'] = {
                'current_app': context.get('current_app'),
                'most_used_apps': context.get('most_used_apps', [])[:3]
            }
        except:
            stats['context'] = {}
    
    return jsonify(stats)


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    active_sessions[session_id] = {
        'connected_at': datetime.now().isoformat(),
        'messages': []
    }
    emit('connected', {'session_id': session_id})
    print(f"[+] Client connected: {session_id}")


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    session_id = session.get('session_id')
    if session_id in active_sessions:
        del active_sessions[session_id]
    print(f"[-] Client disconnected: {session_id}")


@socketio.on('send_message')
def handle_message(data):
    """Handle text message with full action execution."""
    message = data.get('message', '').strip()
    session_id = session.get('session_id', 'unknown')
    
    if not message:
        return
    
    print(f"\n[📝] Message: {message}")
    
    # Process with AI brain
    if brain:
        try:
            result = brain.process_input(message, device_id=session_id)
            
            # Execute the action
            action_result = execute_action(message, result, session_id)
            
            response = {
                'message': result['response'],
                'intent': result['intent'],
                'confidence': result['confidence'],
                'action': result.get('action'),
                'action_result': action_result,
                'timestamp': datetime.now().isoformat()
            }
            
            emit('receive_message', response)
            
        except Exception as e:
            print(f"[!] Error processing message: {e}")
            emit('receive_message', {
                'message': f'Error: {str(e)}',
                'intent': 'error',
                'confidence': 0,
                'timestamp': datetime.now().isoformat()
            })
    else:
        emit('receive_message', {
            'message': 'AI Brain not initialized. Please restart the system.',
            'intent': 'error',
            'confidence': 0,
            'timestamp': datetime.now().isoformat()
        })


@socketio.on('start_voice')
def handle_start_voice():
    """Handle voice recording with full execution."""
    emit('voice_status', {'status': 'listening'})
    
    def listen_and_respond():
        if voice:
            print("\n[🎤] Listening...")
            text = voice.listen(timeout=10, auto_stop=True)
            
            if text:
                print(f"[🗣️] Recognized: {text}")
                
                if brain:
                    try:
                        result = brain.process_input(text, device_id=session.get('session_id', 'unknown'))
                        
                        # Execute the action
                        action_result = execute_action(text, result, session.get('session_id'))
                        
                        socketio.emit('voice_recognized', {
                            'text': text,
                            'response': result['response'],
                            'intent': result['intent'],
                            'confidence': result['confidence'],
                            'action_result': action_result,
                            'timestamp': datetime.now().isoformat()
                        }, room=request.sid)
                        
                    except Exception as e:
                        print(f"[!] Error: {e}")
                        socketio.emit('voice_error', {'error': str(e)}, room=request.sid)
                else:
                    socketio.emit('voice_error', {
                        'error': 'AI Brain not available'
                    }, room=request.sid)
            else:
                socketio.emit('voice_error', {
                    'error': 'No speech detected'
                }, room=request.sid)
        else:
            socketio.emit('voice_error', {
                'error': 'Voice system not available'
            }, room=request.sid)
    
    thread = threading.Thread(target=listen_and_respond)
    thread.daemon = True
    thread.start()


def execute_action(original_text: str, result: Dict, session_id: str) -> Dict:
    """Execute action based on AI brain result with comprehensive error handling."""
    intent = result.get('intent')
    text_lower = original_text.lower()
    
    action_result = {
        'executed': False,
        'action_type': None,
        'details': None,
        'error': None
    }
    
    try:
        # Open Application
        if 'open' in text_lower:
            for app_name in control_ai.APP_COMMANDS.keys():
                if app_name in text_lower:
                    print(f"[▶️] Opening {app_name}...")
                    control_ai.open_app(app_name)
                    action_result['executed'] = True
                    action_result['action_type'] = 'open_app'
                    action_result['details'] = app_name
                    
                    socketio.emit('action_executed', {
                        'action': 'open_app',
                        'app': app_name,
                        'success': True
                    }, room=session_id)
                    return action_result
        
        # System Commands
        for cmd_name in control_ai.SYSTEM_COMMANDS.keys():
            if cmd_name in text_lower:
                print(f"[▶️] System command: {cmd_name}")
                control_ai.run_system_command(cmd_name)
                action_result['executed'] = True
                action_result['action_type'] = 'system_command'
                action_result['details'] = cmd_name
                
                socketio.emit('action_executed', {
                    'action': 'system_command',
                    'command': cmd_name,
                    'success': True
                }, room=session_id)
                return action_result
        
        # File Search
        if 'find' in text_lower or 'search' in text_lower:
            words = text_lower.split()
            query_words = [w for w in words if w not in ['find', 'search', 'for', 'my', 'the', 'a', 'an']]
            if query_words:
                query = ' '.join(query_words)
                print(f"[🔍] Searching: {query}")
                results = filesearch_ai.search_by_name(query, max_results=10)
                
                action_result['executed'] = True
                action_result['action_type'] = 'file_search'
                action_result['details'] = {'query': query, 'count': len(results)}
                
                socketio.emit('search_results', {
                    'query': query,
                    'results': [{'name': r['name'], 'path': r['path']} for r in results[:5]],
                    'count': len(results)
                }, room=session_id)
                return action_result
        
        # Screenshot
        if 'screenshot' in text_lower:
            print("[📸] Taking screenshot...")
            filepath = aiscreencontrol_ai.take_screenshot()
            action_result['executed'] = True
            action_result['action_type'] = 'screenshot'
            action_result['details'] = filepath
            
            socketio.emit('action_executed', {
                'action': 'screenshot',
                'filepath': filepath,
                'success': True
            }, room=session_id)
            return action_result
        
        # Mouse Click
        if 'click' in text_lower:
            print("[🖱️] Clicking...")
            aiscreencontrol_ai.parse_and_execute('click')
            action_result['executed'] = True
            action_result['action_type'] = 'mouse_click'
            
            socketio.emit('action_executed', {
                'action': 'mouse_click',
                'success': True
            }, room=session_id)
            return action_result
        
        # Type Text
        if 'type' in text_lower and 'type ' in text_lower:
            text_to_type = original_text.split('type ', 1)[1]
            print(f"[⌨️] Typing: {text_to_type}")
            aiscreencontrol_ai.type_text(text_to_type)
            action_result['executed'] = True
            action_result['action_type'] = 'type_text'
            action_result['details'] = text_to_type
            
            socketio.emit('action_executed', {
                'action': 'type_text',
                'text': text_to_type,
                'success': True
            }, room=session_id)
            return action_result
        
        # Press Key
        if 'press' in text_lower:
            # Extract key combination
            if 'press ' in text_lower:
                key = text_lower.split('press ', 1)[1].strip()
                print(f"[⌨️] Pressing: {key}")
                aiscreencontrol_ai.press_key(key)
                action_result['executed'] = True
                action_result['action_type'] = 'press_key'
                action_result['details'] = key
                
                socketio.emit('action_executed', {
                    'action': 'press_key',
                    'key': key,
                    'success': True
                }, room=session_id)
                return action_result
        
        # Move Mouse
        if 'move mouse' in text_lower or 'move to' in text_lower:
            print(f"[🖱️] Moving mouse...")
            aiscreencontrol_ai.parse_and_execute(original_text)
            action_result['executed'] = True
            action_result['action_type'] = 'move_mouse'
            
            socketio.emit('action_executed', {
                'action': 'move_mouse',
                'success': True
            }, room=session_id)
            return action_result
        
        # Scroll
        if 'scroll' in text_lower:
            print(f"[🖱️] Scrolling...")
            aiscreencontrol_ai.parse_and_execute(original_text)
            action_result['executed'] = True
            action_result['action_type'] = 'scroll'
            
            socketio.emit('action_executed', {
                'action': 'scroll',
                'success': True
            }, room=session_id)
            return action_result
    
    except Exception as e:
        print(f"[!] Action execution error: {e}")
        action_result['error'] = str(e)
        socketio.emit('action_error', {'error': str(e)}, room=session_id)
    
    return action_result


if __name__ == '__main__':
    # Initialize components
    initialize_components()
    
    # Start server
    print("\n" + "=" * 60)
    print("  🤖 Christa AI - Complete Enhanced System")
    print("=" * 60)
    print("\n  ✨ All Features:")
    print("  • Voice control (hands-free)")
    print("  • Text commands")
    print("  • File search")
    print("  • System control")
    print("  • Screen automation")
    print("  • Context awareness")
    print("  • Workflow automation")
    print("\n  🌐 Open your browser:")
    print("  👉 http://localhost:5000")
    print("\n  ⌨️ Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n[!] Shutting down...")
    finally:
        if context_system:
            context_system.stop()
        if ollama_process:
            ollama_process.terminate()
        print("[✓] Christa AI stopped. Goodbye!")

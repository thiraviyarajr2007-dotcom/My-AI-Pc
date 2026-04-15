"""
Christa AI - Hands-Free Web UI
Complete touchless control with voice, gestures, and face recognition
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import os
import uuid
import threading
import time
import json
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
except ImportError as e:
    print(f"[!] Import error: {e}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'christa-handsfree-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global components
brain = None
memory = None
voice = None
workflow_manager = None
context_system = None
active_sessions = {}

# Hands-free control state
handsfree_active = False
voice_listening = False


def initialize_components():
    """Initialize all AI components."""
    global brain, memory, voice, workflow_manager, context_system
    
    print("[🤖] Initializing Christa AI Hands-Free System...")
    
    try:
        memory = MemorySystem()
        print("[✓] Memory system initialized")
    except Exception as e:
        print(f"[!] Memory system error: {e}")
    
    try:
        brain = AIBrain(use_sqlite=True)
        print("[✓] AI Brain initialized")
    except Exception as e:
        print(f"[!] AI Brain error: {e}")
    
    try:
        voice = HybridVoiceEnhanced(prefer_offline=True, model_size="small")
        print("[✓] Voice system initialized")
    except Exception as e:
        print(f"[!] Voice system error: {e}")
    
    try:
        workflow_manager = WorkflowManager()
        print("[✓] Workflow manager initialized")
    except Exception as e:
        print(f"[!] Workflow manager error: {e}")
    
    try:
        context_system = ContextAwarenessSystem(update_interval=3.0)
        context_system.start()
        print("[✓] Context awareness started")
    except Exception as e:
        print(f"[!] Context awareness error: {e}")
    
    print("[✓] Christa AI Hands-Free System ready!")


@app.route('/')
def index():
    """Main interface."""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get system status."""
    status = {
        'brain': brain is not None,
        'memory': memory is not None,
        'voice': voice is not None,
        'workflows': workflow_manager is not None,
        'context': context_system is not None and context_system.is_running,
        'handsfree_active': handsfree_active,
        'voice_listening': voice_listening
    }
    return jsonify(status)


@app.route('/api/stats')
def get_stats():
    """Get statistics."""
    stats = {}
    
    if brain and brain.use_sqlite:
        stats['brain'] = brain.get_statistics()
        stats['most_used'] = brain.get_most_used_commands(limit=5)
    
    if context_system:
        context = context_system.get_current_context()
        stats['context'] = {
            'current_app': context.get('current_app'),
            'most_used_apps': context.get('most_used_apps', [])[:3]
        }
    
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
    """Handle text message."""
    message = data.get('message', '').strip()
    session_id = session.get('session_id', 'unknown')
    
    if not message:
        return
    
    print(f"[📝] Message from {session_id}: {message}")
    
    # Process with AI brain
    if brain:
        result = brain.process_input(message, device_id=session_id)
        
        # Execute the action
        execute_action(result, session_id)
        
        response = {
            'message': result['response'],
            'intent': result['intent'],
            'confidence': result['confidence'],
            'action': result['action'],
            'timestamp': datetime.now().isoformat()
        }
        
        emit('receive_message', response)
    else:
        emit('receive_message', {
            'message': 'AI Brain not initialized',
            'intent': 'error',
            'confidence': 0,
            'timestamp': datetime.now().isoformat()
        })


@socketio.on('start_voice')
def handle_start_voice():
    """Handle voice recording start."""
    global voice_listening
    voice_listening = True
    emit('voice_status', {'status': 'listening'})
    
    def listen_and_respond():
        global voice_listening
        
        if voice:
            print("[🎤] Listening for voice input...")
            text = voice.listen(timeout=10, auto_stop=True)
            
            if text:
                print(f"[🗣️] Recognized: {text}")
                
                if brain:
                    result = brain.process_input(text, device_id=session.get('session_id', 'unknown'))
                    
                    # Execute the action
                    execute_action(result, session.get('session_id'))
                    
                    socketio.emit('voice_recognized', {
                        'text': text,
                        'response': result['response'],
                        'intent': result['intent'],
                        'confidence': result['confidence'],
                        'timestamp': datetime.now().isoformat()
                    }, room=request.sid)
            else:
                socketio.emit('voice_error', {
                    'error': 'No speech detected'
                }, room=request.sid)
        
        voice_listening = False
    
    thread = threading.Thread(target=listen_and_respond)
    thread.daemon = True
    thread.start()


def execute_action(result: Dict, session_id: str):
    """Execute action based on AI brain result."""
    intent = result.get('intent')
    action = result.get('action')
    
    try:
        # Extract app/command from the original input
        original_text = result.get('original_input', '').lower()
        
        if intent == 'open_app' or 'open' in original_text:
            # Try to find app name in the text
            for app_name in control_ai.APP_COMMANDS.keys():
                if app_name in original_text:
                    print(f"[▶️] Opening {app_name}...")
                    control_ai.open_app(app_name)
                    
                    # Notify client
                    socketio.emit('action_executed', {
                        'action': 'open_app',
                        'app': app_name,
                        'success': True
                    }, room=session_id)
                    return
        
        elif intent == 'system_command':
            # Check for system commands
            for cmd_name in control_ai.SYSTEM_COMMANDS.keys():
                if cmd_name in original_text:
                    print(f"[▶️] Executing system command: {cmd_name}")
                    control_ai.run_system_command(cmd_name)
                    
                    socketio.emit('action_executed', {
                        'action': 'system_command',
                        'command': cmd_name,
                        'success': True
                    }, room=session_id)
                    return
        
        elif intent == 'search_files' or 'find' in original_text or 'search' in original_text:
            # Extract search query
            words = original_text.split()
            if len(words) > 1:
                # Remove command words
                query_words = [w for w in words if w not in ['find', 'search', 'for', 'my', 'the']]
                query = ' '.join(query_words)
                
                print(f"[🔍] Searching for: {query}")
                results = filesearch_ai.search_by_name(query, max_results=10)
                
                socketio.emit('search_results', {
                    'query': query,
                    'results': [{'name': r['name'], 'path': r['path']} for r in results[:5]],
                    'count': len(results)
                }, room=session_id)
        
        elif intent == 'take_screenshot' or 'screenshot' in original_text:
            print("[📸] Taking screenshot...")
            filepath = aiscreencontrol_ai.take_screenshot()
            
            socketio.emit('action_executed', {
                'action': 'screenshot',
                'filepath': filepath,
                'success': True
            }, room=session_id)
        
        elif 'click' in original_text:
            print("[🖱️] Clicking mouse...")
            aiscreencontrol_ai.parse_and_execute('click')
            
            socketio.emit('action_executed', {
                'action': 'mouse_click',
                'success': True
            }, room=session_id)
        
        elif 'type' in original_text:
            # Extract text to type
            if 'type ' in original_text:
                text_to_type = original_text.split('type ', 1)[1]
                print(f"[⌨️] Typing: {text_to_type}")
                aiscreencontrol_ai.type_text(text_to_type)
                
                socketio.emit('action_executed', {
                    'action': 'type_text',
                    'text': text_to_type,
                    'success': True
                }, room=session_id)
        
        else:
            # Try to parse as general command
            print(f"[🔧] Trying general command: {original_text}")
            control_ai.parse_command(original_text)
    
    except Exception as e:
        print(f"[!] Action execution error: {e}")
        socketio.emit('action_error', {
            'error': str(e)
        }, room=session_id)


if __name__ == '__main__':
    # Initialize components
    initialize_components()
    
    # Start server
    print("\n" + "=" * 60)
    print("  🤖 Christa AI - Hands-Free Control UI")
    print("=" * 60)
    print("\n  Features:")
    print("  • Voice control (hands-free)")
    print("  • Text commands")
    print("  • File search")
    print("  • System control")
    print("  • Screen automation")
    print("  • Context awareness")
    print("\n  Open your browser and go to:")
    print("  👉 http://localhost:5000")
    print("\n  Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    finally:
        if context_system:
            context_system.stop()

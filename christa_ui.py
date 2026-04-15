"""
Christa AI - Modern Web UI (Copilot-style)
Beautiful chat interface with voice support
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import os
import uuid
import threading
import time
from datetime import datetime

# Import Christa components
try:
    from ai_brain import AIBrain
    from memory_system import MemorySystem
    from whisper_voice_enhanced import HybridVoiceEnhanced
except ImportError as e:
    print(f"[!] Import error: {e}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'christa-ai-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global components
brain = None
memory = None
voice = None
active_sessions = {}


def initialize_components():
    """Initialize AI components."""
    global brain, memory, voice
    
    print("[🤖] Initializing Christa AI components...")
    
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
    
    print("[✓] Christa AI ready!")


@app.route('/')
def index():
    """Main chat interface."""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get system status."""
    status = {
        'brain': brain is not None and brain.ollama_available,
        'memory': memory is not None,
        'voice': voice is not None,
        'ollama_model': brain.model if brain else None,
        'voice_model': voice.whisper.model_size if voice and voice.whisper_available else None
    }
    return jsonify(status)


@app.route('/api/stats')
def get_stats():
    """Get usage statistics."""
    if brain and brain.use_sqlite:
        stats = brain.get_statistics()
        most_used = brain.get_most_used_commands(limit=5)
        return jsonify({
            'stats': stats,
            'most_used': most_used
        })
    return jsonify({'error': 'Statistics not available'})


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
    """Handle text message from user."""
    message = data.get('message', '').strip()
    session_id = session.get('session_id', 'unknown')
    
    if not message:
        return
    
    print(f"[📝] Message from {session_id}: {message}")
    
    # Process with AI brain
    if brain:
        result = brain.process_input(message, device_id=session_id)
        
        response = {
            'message': result['response'],
            'intent': result['intent'],
            'confidence': result['confidence'],
            'action': result['action'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in session
        if session_id in active_sessions:
            active_sessions[session_id]['messages'].append({
                'user': message,
                'assistant': result['response'],
                'timestamp': datetime.now().isoformat()
            })
        
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
    emit('voice_status', {'status': 'listening'})
    
    def listen_and_respond():
        if voice:
            print("[🎤] Listening for voice input...")
            text = voice.listen(timeout=10, auto_stop=True)
            
            if text:
                print(f"[🗣️] Recognized: {text}")
                
                # Process the recognized text
                if brain:
                    result = brain.process_input(text, device_id=session.get('session_id', 'unknown'))
                    
                    socketio.emit('voice_recognized', {
                        'text': text,
                        'response': result['response'],
                        'intent': result['intent'],
                        'confidence': result['confidence'],
                        'timestamp': datetime.now().isoformat()
                    }, room=request.sid)
                else:
                    socketio.emit('voice_recognized', {
                        'text': text,
                        'response': 'AI Brain not available',
                        'timestamp': datetime.now().isoformat()
                    }, room=request.sid)
            else:
                socketio.emit('voice_error', {
                    'error': 'No speech detected'
                }, room=request.sid)
        else:
            socketio.emit('voice_error', {
                'error': 'Voice system not available'
            }, room=request.sid)
    
    # Run in background thread
    thread = threading.Thread(target=listen_and_respond)
    thread.daemon = True
    thread.start()


@socketio.on('clear_history')
def handle_clear_history():
    """Clear chat history."""
    session_id = session.get('session_id')
    if session_id in active_sessions:
        active_sessions[session_id]['messages'] = []
    emit('history_cleared', {'status': 'success'})


if __name__ == '__main__':
    # Initialize components
    initialize_components()
    
    # Start server
    print("\n" + "=" * 60)
    print("  🤖 Christa AI - Web UI")
    print("=" * 60)
    print("\n  Open your browser and go to:")
    print("  👉 http://localhost:5000")
    print("\n  Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

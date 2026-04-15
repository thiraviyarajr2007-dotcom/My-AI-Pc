"""
Christa AI - Advanced Multitasking UI
Enhanced web interface with all features integrated
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
    from control_ai import open_app, run_system_command, open_website, parse_command
    from filesearch_ai import search_by_name, search_by_extension, search_by_content, search_recent_files
    from workflow_automation import WorkflowManager, WorkflowAction
    from context_awareness import ContextAwarenessSystem
    import aiscreencontrol_ai
except ImportError as e:
    print(f"[!] Import error: {e}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'christa-advanced-ai-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global components
brain = None
memory = None
voice = None
workflow_manager = None
context_system = None
active_sessions = {}
active_tasks = {}  # Track running tasks


class TaskManager:
    """Manages concurrent tasks and operations."""
    
    def __init__(self):
        self.tasks = {}
        self.task_counter = 0
        self.lock = threading.Lock()
    
    def create_task(self, name: str, func, *args, **kwargs):
        """Create and start a new task."""
        with self.lock:
            self.task_counter += 1
            task_id = f"task_{self.task_counter}"
            
            task_info = {
                'id': task_id,
                'name': name,
                'status': 'running',
                'started_at': datetime.now().isoformat(),
                'progress': 0,
                'result': None,
                'error': None
            }
            
            self.tasks[task_id] = task_info
            
            def task_wrapper():
                try:
                    result = func(*args, **kwargs)
                    task_info['status'] = 'completed'
                    task_info['result'] = result
                    task_info['progress'] = 100
                except Exception as e:
                    task_info['status'] = 'failed'
                    task_info['error'] = str(e)
                finally:
                    task_info['completed_at'] = datetime.now().isoformat()
            
            thread = threading.Thread(target=task_wrapper, daemon=True)
            thread.start()
            
            return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task information."""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks."""
        return list(self.tasks.values())
    
    def cancel_task(self, task_id: str):
        """Cancel a running task."""
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = 'cancelled'


task_manager = TaskManager()


def initialize_components():
    """Initialize all AI components."""
    global brain, memory, voice, workflow_manager, context_system
    
    print("[🤖] Initializing Christa AI Advanced System...")
    
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
    
    print("[✓] Christa AI Advanced System ready!")


@app.route('/')
def index():
    """Main advanced interface."""
    return render_template('advanced_index.html')


@app.route('/api/status')
def get_status():
    """Get comprehensive system status."""
    status = {
        'brain': brain is not None and brain.ollama_available,
        'memory': memory is not None,
        'voice': voice is not None,
        'workflows': workflow_manager is not None,
        'context': context_system is not None and context_system.is_running,
        'ollama_model': brain.model if brain else None,
        'voice_model': voice.whisper.model_size if voice and voice.whisper_available else None,
        'active_tasks': len([t for t in task_manager.get_all_tasks() if t['status'] == 'running'])
    }
    return jsonify(status)


@app.route('/api/stats')
def get_stats():
    """Get comprehensive statistics."""
    stats = {}
    
    if brain and brain.use_sqlite:
        stats['brain'] = brain.get_statistics()
        stats['most_used'] = brain.get_most_used_commands(limit=5)
    
    if workflow_manager:
        stats['workflows'] = {
            'total': len(workflow_manager.workflows),
            'list': [
                {
                    'name': w.name,
                    'actions': len(w.actions),
                    'executions': w.execution_count
                }
                for w in workflow_manager.workflows.values()
            ]
        }
    
    if context_system:
        context = context_system.get_current_context()
        stats['context'] = {
            'current_app': context.get('current_app'),
            'most_used_apps': context.get('most_used_apps', [])[:3]
        }
    
    return jsonify(stats)


@app.route('/api/context')
def get_context():
    """Get current context information."""
    if context_system:
        context = context_system.get_current_context()
        suggestions = context_system.get_suggestions()
        return jsonify({
            'context': context,
            'suggestions': suggestions
        })
    return jsonify({'error': 'Context system not available'})


@app.route('/api/tasks')
def get_tasks():
    """Get all tasks."""
    return jsonify({'tasks': task_manager.get_all_tasks()})


@app.route('/api/tasks/<task_id>')
def get_task(task_id):
    """Get specific task."""
    task = task_manager.get_task(task_id)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    active_sessions[session_id] = {
        'connected_at': datetime.now().isoformat(),
        'messages': [],
        'tasks': []
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
    """Handle text message with advanced processing."""
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
        
        # Execute action if needed
        if result['action']:
            execute_action(result['action'], result.get('parameters', {}), session_id)
        
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
                
                if brain:
                    result = brain.process_input(text, device_id=session.get('session_id', 'unknown'))
                    
                    # Execute action
                    if result['action']:
                        execute_action(result['action'], result.get('parameters', {}), session.get('session_id'))
                    
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
    
    thread = threading.Thread(target=listen_and_respond)
    thread.daemon = True
    thread.start()


@socketio.on('file_search')
def handle_file_search(data):
    """Handle file search request."""
    query = data.get('query', '')
    search_type = data.get('type', 'name')
    
    def search_task():
        try:
            if search_type == 'name':
                results = search_by_name(query, max_results=20)
            elif search_type == 'extension':
                results = search_by_extension(query, max_results=20)
            elif search_type == 'content':
                results = search_by_content(query, max_results=10)
            elif search_type == 'recent':
                hours = int(query) if query.isdigit() else 24
                results = search_recent_files(hours=hours, max_results=20)
            else:
                results = []
            
            # Format results
            formatted = []
            for r in results:
                formatted.append({
                    'name': r['name'],
                    'path': r['path'],
                    'size': r['size'],
                    'modified': r.get('modified', '').isoformat() if 'modified' in r else None
                })
            
            socketio.emit('file_search_results', {
                'results': formatted,
                'count': len(formatted)
            }, room=request.sid)
        
        except Exception as e:
            socketio.emit('file_search_error', {
                'error': str(e)
            }, room=request.sid)
    
    thread = threading.Thread(target=search_task)
    thread.daemon = True
    thread.start()


@socketio.on('execute_workflow')
def handle_execute_workflow(data):
    """Execute a workflow."""
    workflow_name = data.get('name')
    
    if not workflow_manager or workflow_name not in workflow_manager.workflows:
        emit('workflow_error', {'error': 'Workflow not found'})
        return
    
    def execute_task():
        workflow = workflow_manager.workflows[workflow_name]
        
        def on_action(action, index):
            socketio.emit('workflow_progress', {
                'workflow': workflow_name,
                'action': index + 1,
                'total': len(workflow.actions),
                'current': f"{action.module}.{action.function}"
            }, room=request.sid)
        
        success = workflow_manager.executor.execute(workflow, on_action=on_action)
        
        socketio.emit('workflow_complete', {
            'workflow': workflow_name,
            'success': success
        }, room=request.sid)
    
    thread = threading.Thread(target=execute_task)
    thread.daemon = True
    thread.start()


@socketio.on('screen_control')
def handle_screen_control(data):
    """Handle screen control commands."""
    command = data.get('command', '')
    
    try:
        aiscreencontrol_ai.parse_and_execute(command)
        emit('screen_control_result', {
            'success': True,
            'command': command
        })
    except Exception as e:
        emit('screen_control_error', {
            'error': str(e)
        })


def execute_action(action: str, parameters: Dict, session_id: str):
    """Execute an action based on intent."""
    try:
        if action == 'open_app':
            app_name = parameters.get('app_name', '')
            if app_name:
                open_app(app_name)
        
        elif action == 'system_command':
            command = parameters.get('command', '')
            if command:
                run_system_command(command)
        
        elif action == 'open_website':
            url = parameters.get('url', '')
            if url:
                open_website(url)
        
        elif action == 'search_files':
            query = parameters.get('query', '')
            if query:
                results = search_by_name(query, max_results=5)
                socketio.emit('action_result', {
                    'action': 'file_search',
                    'results': results
                }, room=session_id)
        
        elif action == 'take_screenshot':
            aiscreencontrol_ai.take_screenshot()
    
    except Exception as e:
        print(f"[!] Action execution error: {e}")


if __name__ == '__main__':
    # Initialize components
    initialize_components()
    
    # Start server
    print("\n" + "=" * 60)
    print("  🤖 Christa AI - Advanced Multitasking UI")
    print("=" * 60)
    print("\n  Features:")
    print("  • Real-time chat with AI")
    print("  • Voice input and control")
    print("  • File search across system")
    print("  • Workflow automation")
    print("  • Context awareness")
    print("  • Screen control")
    print("  • Multitasking support")
    print("\n  Open your browser and go to:")
    print("  👉 http://localhost:5000")
    print("\n  Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    finally:
        if context_system:
            context_system.stop()

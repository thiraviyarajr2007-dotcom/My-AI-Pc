"""
Christa AI - FREE Stack Launcher
Starts the complete FREE AI assistant with all features
"""

import sys
import time
from typing import Optional

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    """Print startup banner."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║              🤖 Christa AI - FREE Edition                  ║")
    print("║                                                            ║")
    print("║          Enterprise-level AI • Zero Cost • Offline         ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")


def check_dependencies():
    """Check if all required modules are available."""
    print(f"{Colors.BOLD}Checking dependencies...{Colors.RESET}\n")
    
    required = {
        "memory_system": "Memory System",
        "ai_brain": "AI Brain",
        "whisper_voice": "Voice Recognition",
        "rag_system": "RAG System"
    }
    
    missing = []
    
    for module, name in required.items():
        try:
            __import__(module)
            print(f"{Colors.GREEN}✅ {name}{Colors.RESET}")
        except ImportError:
            print(f"{Colors.RED}❌ {name} - Missing!{Colors.RESET}")
            missing.append(module)
    
    if missing:
        print(f"\n{Colors.RED}Missing modules: {', '.join(missing)}{Colors.RESET}")
        print(f"{Colors.YELLOW}Run: pip install -r requirements.txt{Colors.RESET}\n")
        return False
    
    print(f"\n{Colors.GREEN}All dependencies available!{Colors.RESET}\n")
    return True


def initialize_system():
    """Initialize all system components."""
    print(f"{Colors.BOLD}Initializing system...{Colors.RESET}\n")
    
    components = {}
    
    # Initialize Memory System
    try:
        from memory_system import MemorySystem
        components['memory'] = MemorySystem()
        print(f"{Colors.GREEN}✅ Memory System initialized{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ Memory System failed: {e}{Colors.RESET}")
        return None
    
    # Initialize AI Brain
    try:
        from ai_brain import AIBrain
        components['brain'] = AIBrain(use_sqlite=True)
        print(f"{Colors.GREEN}✅ AI Brain initialized{Colors.RESET}")
        
        if components['brain'].ollama_available:
            print(f"{Colors.GREEN}   → Ollama connected{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}   → Ollama not available (using fallback){Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ AI Brain failed: {e}{Colors.RESET}")
        return None
    
    # Initialize Voice System
    try:
        from whisper_voice import HybridVoice
        components['voice'] = HybridVoice(prefer_offline=True)
        status = components['voice'].get_status()
        print(f"{Colors.GREEN}✅ Voice System initialized{Colors.RESET}")
        
        if status['whisper_available']:
            print(f"{Colors.GREEN}   → Whisper ready (offline mode){Colors.RESET}")
        elif status['google_available']:
            print(f"{Colors.YELLOW}   → Google Speech ready (online mode){Colors.RESET}")
        else:
            print(f"{Colors.RED}   → No voice recognition available{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Voice System: {e}{Colors.RESET}")
        components['voice'] = None
    
    # Initialize RAG System
    try:
        from rag_system import RAGSystem
        components['rag'] = RAGSystem()
        stats = components['rag'].get_statistics()
        print(f"{Colors.GREEN}✅ RAG System initialized{Colors.RESET}")
        
        if stats['ready']:
            print(f"{Colors.GREEN}   → Document search ready{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}   → RAG not fully ready (missing dependencies){Colors.RESET}")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  RAG System: {e}{Colors.RESET}")
        components['rag'] = None
    
    print(f"\n{Colors.GREEN}System ready!{Colors.RESET}\n")
    return components


def show_menu():
    """Show main menu."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}What would you like to do?{Colors.RESET}\n")
    print(f"  {Colors.CYAN}1.{Colors.RESET} Voice Command (speak to Christa)")
    print(f"  {Colors.CYAN}2.{Colors.RESET} Text Command (type to Christa)")
    print(f"  {Colors.CYAN}3.{Colors.RESET} Search Documents (RAG)")
    print(f"  {Colors.CYAN}4.{Colors.RESET} View Statistics")
    print(f"  {Colors.CYAN}5.{Colors.RESET} System Status")
    print(f"  {Colors.CYAN}6.{Colors.RESET} Exit")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─' * 60}{Colors.RESET}\n")


def voice_command(components):
    """Handle voice command."""
    if not components.get('voice'):
        print(f"{Colors.RED}Voice system not available{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}🎤 Listening... (speak now){Colors.RESET}")
    
    text = components['voice'].listen(timeout=5)
    
    if text:
        print(f"{Colors.GREEN}You said: {text}{Colors.RESET}\n")
        
        # Process with AI brain
        result = components['brain'].process_input(text, device_id="laptop")
        
        print(f"{Colors.MAGENTA}Intent: {result['intent']} (confidence: {result['confidence']:.1%}){Colors.RESET}")
        print(f"{Colors.CYAN}Christa: {result['response']}{Colors.RESET}")
        
        if result['action']['module']:
            print(f"{Colors.YELLOW}Action: {result['action']['module']}.{result['action']['function']}{Colors.RESET}")
    else:
        print(f"{Colors.RED}No speech detected{Colors.RESET}")


def text_command(components):
    """Handle text command."""
    text = input(f"\n{Colors.CYAN}You: {Colors.RESET}").strip()
    
    if not text:
        return
    
    # Process with AI brain
    result = components['brain'].process_input(text, device_id="laptop")
    
    print(f"{Colors.MAGENTA}Intent: {result['intent']} (confidence: {result['confidence']:.1%}){Colors.RESET}")
    print(f"{Colors.CYAN}Christa: {result['response']}{Colors.RESET}")
    
    if result['action']['module']:
        print(f"{Colors.YELLOW}Action: {result['action']['module']}.{result['action']['function']}{Colors.RESET}")


def search_documents(components):
    """Search documents using RAG."""
    if not components.get('rag'):
        print(f"{Colors.RED}RAG system not available{Colors.RESET}")
        return
    
    stats = components['rag'].get_statistics()
    
    if stats['total_documents'] == 0:
        print(f"\n{Colors.YELLOW}No documents indexed yet{Colors.RESET}")
        print(f"{Colors.CYAN}Add documents: rag.add_directory('./your_folder'){Colors.RESET}")
        return
    
    query = input(f"\n{Colors.CYAN}Search query: {Colors.RESET}").strip()
    
    if not query:
        return
    
    print(f"\n{Colors.CYAN}Searching...{Colors.RESET}\n")
    
    results = components['rag'].search(query, top_k=3)
    
    if results:
        print(f"{Colors.GREEN}Found {len(results)} results:{Colors.RESET}\n")
        
        for result in results:
            doc = result['document']
            print(f"{Colors.BOLD}Rank {result['rank']} (score: {result['score']:.4f}){Colors.RESET}")
            print(f"  {doc['content'][:200]}...")
            if doc.get('metadata', {}).get('filename'):
                print(f"  {Colors.YELLOW}File: {doc['metadata']['filename']}{Colors.RESET}")
            print()
    else:
        print(f"{Colors.RED}No results found{Colors.RESET}")


def view_statistics(components):
    """View system statistics."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}System Statistics{Colors.RESET}\n")
    
    # AI Brain stats
    if components['brain'].use_sqlite:
        stats = components['brain'].get_statistics()
        print(f"{Colors.CYAN}AI Brain:{Colors.RESET}")
        print(f"  Total commands: {stats.get('total_commands', 0)}")
        print(f"  Successful: {stats.get('successful_commands', 0)}")
        print(f"  Learned patterns: {stats.get('learned_patterns', 0)}")
        print(f"  Context entries: {stats.get('context_entries', 0)}")
        
        # Most used commands
        most_used = components['brain'].get_most_used_commands(limit=5)
        if most_used:
            print(f"\n{Colors.CYAN}Most Used Commands:{Colors.RESET}")
            for cmd in most_used:
                print(f"  • {cmd['command']} ({cmd['count']} times)")
    
    # RAG stats
    if components.get('rag'):
        rag_stats = components['rag'].get_statistics()
        print(f"\n{Colors.CYAN}RAG System:{Colors.RESET}")
        print(f"  Documents: {rag_stats['total_documents']}")
        print(f"  Vectors: {rag_stats['total_vectors']}")
        print(f"  Model: {rag_stats['model']}")
    
    print(f"{Colors.BOLD}{Colors.BLUE}{'─' * 60}{Colors.RESET}")


def system_status(components):
    """Show system status."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}System Status{Colors.RESET}\n")
    
    # Memory
    status = f"{Colors.GREEN}✅ Active{Colors.RESET}" if components.get('memory') else f"{Colors.RED}❌ Inactive{Colors.RESET}"
    print(f"Memory System: {status}")
    
    # AI Brain
    status = f"{Colors.GREEN}✅ Active{Colors.RESET}" if components.get('brain') else f"{Colors.RED}❌ Inactive{Colors.RESET}"
    print(f"AI Brain: {status}")
    if components.get('brain'):
        mode = "SQLite" if components['brain'].use_sqlite else "JSON"
        print(f"  Mode: {mode}")
        ollama = "Connected" if components['brain'].ollama_available else "Not available"
        print(f"  Ollama: {ollama}")
    
    # Voice
    if components.get('voice'):
        voice_status = components['voice'].get_status()
        status = f"{Colors.GREEN}✅ Active{Colors.RESET}"
        print(f"Voice System: {status}")
        print(f"  Whisper: {'Available' if voice_status['whisper_available'] else 'Not available'}")
        print(f"  Google: {'Available' if voice_status['google_available'] else 'Not available'}")
        print(f"  Offline: {'Yes' if voice_status['offline_capable'] else 'No'}")
    else:
        print(f"Voice System: {Colors.YELLOW}⚠️  Not available{Colors.RESET}")
    
    # RAG
    if components.get('rag'):
        rag_stats = components['rag'].get_statistics()
        status = f"{Colors.GREEN}✅ Active{Colors.RESET}" if rag_stats['ready'] else f"{Colors.YELLOW}⚠️  Partial{Colors.RESET}"
        print(f"RAG System: {status}")
        print(f"  Embeddings: {'Available' if rag_stats['embeddings_available'] else 'Not available'}")
        print(f"  FAISS: {'Available' if rag_stats['faiss_available'] else 'Not available'}")
    else:
        print(f"RAG System: {Colors.YELLOW}⚠️  Not available{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}Cost: $0/month (100% FREE!){Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─' * 60}{Colors.RESET}")


def main():
    """Main application loop."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print(f"{Colors.RED}Please install missing dependencies first{Colors.RESET}\n")
        sys.exit(1)
    
    # Initialize system
    components = initialize_system()
    
    if not components:
        print(f"{Colors.RED}System initialization failed{Colors.RESET}\n")
        sys.exit(1)
    
    # Main loop
    try:
        while True:
            show_menu()
            
            choice = input(f"{Colors.CYAN}Enter choice (1-6): {Colors.RESET}").strip()
            
            if choice == '1':
                voice_command(components)
            elif choice == '2':
                text_command(components)
            elif choice == '3':
                search_documents(components)
            elif choice == '4':
                view_statistics(components)
            elif choice == '5':
                system_status(components)
            elif choice == '6':
                print(f"\n{Colors.CYAN}Shutting down...{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}Invalid choice{Colors.RESET}")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}Interrupted by user{Colors.RESET}")
    
    finally:
        # Cleanup
        if components.get('brain'):
            components['brain'].close()
        if components.get('memory'):
            components['memory'].close()
        
        print(f"\n{Colors.GREEN}Goodbye! 👋{Colors.RESET}\n")


if __name__ == "__main__":
    main()

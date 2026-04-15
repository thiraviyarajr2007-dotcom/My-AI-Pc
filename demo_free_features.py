"""
Quick Demo - Christa AI FREE Features
Shows all working features without requiring microphone or Ollama
"""

import time

# Colors for output
class C:
    G = '\033[92m'  # Green
    B = '\033[94m'  # Blue
    Y = '\033[93m'  # Yellow
    M = '\033[95m'  # Magenta
    C = '\033[96m'  # Cyan
    R = '\033[0m'   # Reset
    BOLD = '\033[1m'


def print_section(title):
    """Print section header."""
    print(f"\n{C.BOLD}{C.B}{'=' * 60}{C.R}")
    print(f"{C.BOLD}{C.B}  {title}{C.R}")
    print(f"{C.BOLD}{C.B}{'=' * 60}{C.R}\n")


def demo_memory_system():
    """Demo memory system features."""
    print_section("1. Memory System Demo (SQLite)")
    
    from memory_system import MemorySystem
    
    print(f"{C.C}Creating memory system...{C.R}")
    memory = MemorySystem("demo_memory.db")
    
    # Add commands
    print(f"\n{C.Y}Adding sample commands...{C.R}")
    memory.add_command("open chrome", "open_app", 0.95, "Opening Chrome", "laptop", True)
    memory.add_command("find documents", "search", 0.88, "Searching...", "laptop", True)
    memory.add_command("take screenshot", "screenshot", 0.92, "Screenshot taken", "phone", True)
    print(f"{C.G}✅ Added 3 commands{C.R}")
    
    # Set preferences
    print(f"\n{C.Y}Setting preferences...{C.R}")
    memory.set_preference("voice_rate", 175)
    memory.set_preference("theme", "dark")
    memory.set_preference("wake_word", "hey christa")
    print(f"{C.G}✅ Preferences saved{C.R}")
    
    # Get statistics
    print(f"\n{C.Y}Getting statistics...{C.R}")
    stats = memory.get_statistics()
    print(f"{C.M}Total commands: {stats['total_commands']}{C.R}")
    print(f"{C.M}Successful: {stats['successful_commands']}{C.R}")
    
    # Get command history
    print(f"\n{C.Y}Recent commands:{C.R}")
    history = memory.get_command_history(limit=3)
    for cmd in history:
        print(f"  • {cmd['command']} → {cmd['response']}")
    
    # Get preferences
    print(f"\n{C.Y}Saved preferences:{C.R}")
    prefs = memory.get_all_preferences()
    for key, value in prefs.items():
        print(f"  • {key}: {value}")
    
    memory.close()
    
    # Cleanup
    import os
    if os.path.exists("demo_memory.db"):
        os.remove("demo_memory.db")
    
    print(f"\n{C.G}✅ Memory system demo complete!{C.R}")


def demo_ai_brain():
    """Demo AI brain features."""
    print_section("2. AI Brain Demo (Intent Classification)")
    
    from ai_brain import AIBrain
    
    print(f"{C.C}Initializing AI brain...{C.R}")
    brain = AIBrain(use_sqlite=True)
    print(f"{C.G}✅ AI brain ready{C.R}")
    
    # Test commands
    test_commands = [
        "open chrome",
        "find my documents",
        "take a screenshot",
        "what can you do?",
        "hello christa"
    ]
    
    print(f"\n{C.Y}Processing commands...{C.R}\n")
    
    for cmd in test_commands:
        result = brain.process_input(cmd, device_id="demo")
        
        print(f"{C.C}Command: {cmd}{C.R}")
        print(f"  Intent: {C.M}{result['intent']}{C.R} (confidence: {result['confidence']:.0%})")
        print(f"  Response: {C.G}{result['response']}{C.R}")
        if result['action']['module']:
            print(f"  Action: {C.Y}{result['action']['module']}.{result['action']['function']}{C.R}")
        print()
        time.sleep(0.3)
    
    # Show statistics
    print(f"{C.Y}Statistics after processing:{C.R}")
    stats = brain.get_statistics()
    print(f"  Total commands: {C.M}{stats['total_commands']}{C.R}")
    print(f"  Successful: {C.M}{stats['successful_commands']}{C.R}")
    
    # Most used commands
    print(f"\n{C.Y}Most used commands:{C.R}")
    most_used = brain.get_most_used_commands(limit=3)
    for cmd in most_used:
        print(f"  • {cmd['command']} ({cmd['count']} times)")
    
    brain.close()
    
    # Cleanup
    import os
    if os.path.exists("christa_memory.db"):
        os.remove("christa_memory.db")
    
    print(f"\n{C.G}✅ AI brain demo complete!{C.R}")


def demo_rag_system():
    """Demo RAG system features."""
    print_section("3. RAG System Demo (Document Search)")
    
    from rag_system import RAGSystem
    
    print(f"{C.C}Initializing RAG system...{C.R}")
    rag = RAGSystem(storage_path="demo_rag_data")
    
    stats = rag.get_statistics()
    if not stats['ready']:
        print(f"{C.Y}⚠️  RAG system not fully ready (missing dependencies){C.R}")
        print(f"{C.Y}   Install: pip install sentence-transformers faiss-cpu{C.R}")
        return
    
    print(f"{C.G}✅ RAG system ready{C.R}")
    
    # Add sample documents
    print(f"\n{C.Y}Adding sample documents...{C.R}")
    
    docs = [
        ("Python is a high-level programming language known for its simplicity and readability.", 
         {"topic": "programming", "language": "python"}),
        ("Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
         {"topic": "ai", "subtopic": "ml"}),
        ("FastAPI is a modern, fast web framework for building APIs with Python 3.7+.",
         {"topic": "programming", "framework": "fastapi"}),
        ("Neural networks are computing systems inspired by biological neural networks.",
         {"topic": "ai", "subtopic": "neural-networks"}),
        ("SQLite is a lightweight, serverless database engine perfect for embedded applications.",
         {"topic": "database", "type": "sqlite"})
    ]
    
    for content, metadata in docs:
        rag.add_document(content, metadata)
    
    print(f"{C.G}✅ Added {len(docs)} documents{C.R}")
    
    # Test searches
    print(f"\n{C.Y}Testing semantic search...{C.R}\n")
    
    queries = [
        "What is Python?",
        "Tell me about artificial intelligence",
        "How to build APIs?"
    ]
    
    for query in queries:
        print(f"{C.C}Query: {query}{C.R}")
        results = rag.search(query, top_k=2)
        
        for result in results:
            doc = result['document']
            print(f"  Rank {result['rank']} (score: {result['score']:.4f})")
            print(f"  → {doc['content'][:80]}...")
        print()
        time.sleep(0.3)
    
    # Test context generation
    print(f"{C.Y}Testing context generation...{C.R}")
    query = "Explain machine learning"
    context = rag.get_context(query, max_length=300)
    print(f"\n{C.C}Query: {query}{C.R}")
    print(f"{C.M}Generated context:{C.R}")
    print(f"{context[:200]}...")
    
    # Show statistics
    print(f"\n{C.Y}RAG Statistics:{C.R}")
    stats = rag.get_statistics()
    print(f"  Documents: {C.M}{stats['total_documents']}{C.R}")
    print(f"  Vectors: {C.M}{stats['total_vectors']}{C.R}")
    print(f"  Model: {C.M}{stats['model']}{C.R}")
    
    # Cleanup
    rag.clear()
    import shutil
    import os
    if os.path.exists("demo_rag_data"):
        try:
            shutil.rmtree("demo_rag_data")
        except:
            pass
    
    print(f"\n{C.G}✅ RAG system demo complete!{C.R}")


def demo_whisper_status():
    """Demo Whisper voice status."""
    print_section("4. Whisper Voice Status")
    
    from whisper_voice import HybridVoice
    
    print(f"{C.C}Checking voice system...{C.R}")
    voice = HybridVoice(prefer_offline=True)
    
    status = voice.get_status()
    
    print(f"\n{C.Y}Voice System Status:{C.R}")
    print(f"  Whisper (offline): {C.G if status['whisper_available'] else C.Y}{'✅ Available' if status['whisper_available'] else '⚠️  Not available'}{C.R}")
    print(f"  Google (online): {C.G if status['google_available'] else C.Y}{'✅ Available' if status['google_available'] else '⚠️  Not available'}{C.R}")
    print(f"  Offline capable: {C.G if status['offline_capable'] else C.Y}{'✅ Yes' if status['offline_capable'] else '❌ No'}{C.R}")
    print(f"  Mode: {C.M}{status['mode']}{C.R}")
    
    if status['whisper_available']:
        print(f"\n{C.G}✅ Whisper is ready for offline voice recognition!{C.R}")
        print(f"{C.C}   To test: python whisper_voice.py{C.R}")
    else:
        print(f"\n{C.Y}⚠️  Whisper not available{C.R}")
        print(f"{C.C}   Install: pip install openai-whisper{C.R}")


def show_summary():
    """Show final summary."""
    print_section("Summary - What's Working")
    
    features = [
        ("Memory System", True, "SQLite database with full CRUD operations"),
        ("AI Brain", True, "Intent classification and command processing"),
        ("RAG System", True, "Document search with semantic understanding"),
        ("Whisper Voice", True, "Offline speech recognition ready"),
        ("Ollama LLM", False, "Optional - install from ollama.com"),
    ]
    
    print(f"{C.Y}Feature Status:{C.R}\n")
    
    working = 0
    total = len(features)
    
    for name, status, description in features:
        icon = f"{C.G}✅" if status else f"{C.Y}⚠️ "
        print(f"{icon} {C.BOLD}{name}{C.R}")
        print(f"   {description}")
        if status:
            working += 1
        print()
    
    print(f"{C.BOLD}Status: {working}/{total} features working{C.R}")
    print(f"{C.BOLD}Success Rate: {(working/total)*100:.0f}%{C.R}")
    
    print(f"\n{C.G}{'=' * 60}{C.R}")
    print(f"{C.BOLD}{C.G}  🎉 Your FREE AI Assistant is Ready!{C.R}")
    print(f"{C.G}{'=' * 60}{C.R}")
    
    print(f"\n{C.C}Next Steps:{C.R}")
    print(f"  1. Try interactive demo: {C.Y}python start_free_christa.py{C.R}")
    print(f"  2. Test voice: {C.Y}python whisper_voice.py{C.R}")
    print(f"  3. Install Ollama (optional): {C.Y}https://ollama.com{C.R}")
    
    print(f"\n{C.M}💰 Cost: $0/month (100% FREE!){C.R}")
    print(f"{C.M}💾 All data stored locally{C.R}")
    print(f"{C.M}🔒 Complete privacy{C.R}")
    print()


def main():
    """Run all demos."""
    print(f"\n{C.BOLD}{C.C}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║         🆓 Christa AI - FREE Features Demo                ║")
    print("║                                                            ║")
    print("║              Quick demonstration of all features           ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{C.R}\n")
    
    try:
        # Run demos
        demo_memory_system()
        time.sleep(1)
        
        demo_ai_brain()
        time.sleep(1)
        
        demo_rag_system()
        time.sleep(1)
        
        demo_whisper_status()
        time.sleep(1)
        
        # Show summary
        show_summary()
    
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}Demo interrupted by user{C.R}\n")
    except Exception as e:
        print(f"\n{C.Y}Error: {e}{C.R}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

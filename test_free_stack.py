"""
Test Script for FREE Stack Components
Tests: Memory System, Whisper Voice, RAG System, AI Brain Integration
"""

import sys
import os
from typing import Dict, List

# Color codes for terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")


def test_imports() -> Dict[str, bool]:
    """Test if all required modules can be imported."""
    print_header("Testing Imports")
    
    results = {}
    
    # Core modules
    modules = {
        "memory_system": "Memory System (SQLite)",
        "whisper_voice": "Whisper Voice Recognition",
        "rag_system": "RAG System",
        "ai_brain": "AI Brain (updated)",
    }
    
    for module, name in modules.items():
        try:
            __import__(module)
            print_success(f"{name} - Import OK")
            results[module] = True
        except ImportError as e:
            print_error(f"{name} - Import Failed: {e}")
            results[module] = False
    
    # Optional dependencies
    print("\nOptional Dependencies:")
    
    optional = {
        "whisper": "OpenAI Whisper",
        "sentence_transformers": "Sentence Transformers",
        "faiss": "FAISS",
        "langchain": "LangChain",
    }
    
    for module, name in optional.items():
        try:
            __import__(module)
            print_success(f"{name} - Available")
            results[f"opt_{module}"] = True
        except ImportError:
            print_warning(f"{name} - Not installed (optional)")
            results[f"opt_{module}"] = False
    
    return results


def test_memory_system() -> bool:
    """Test memory system functionality."""
    print_header("Testing Memory System")
    
    try:
        from memory_system import MemorySystem
        
        # Initialize
        print_info("Initializing memory system...")
        memory = MemorySystem("test_memory.db")
        print_success("Memory system initialized")
        
        # Test commands
        print_info("Testing command storage...")
        memory.add_command("test command", "test_intent", 0.95, "test response")
        history = memory.get_command_history(limit=1)
        assert len(history) > 0, "No commands in history"
        print_success("Command storage works")
        
        # Test preferences
        print_info("Testing preferences...")
        memory.set_preference("test_key", "test_value")
        value = memory.get_preference("test_key")
        assert value == "test_value", "Preference not stored correctly"
        print_success("Preferences work")
        
        # Test context
        print_info("Testing context...")
        memory.add_context("user", "test message")
        context = memory.get_recent_context(limit=1)
        assert len(context) > 0, "No context stored"
        print_success("Context storage works")
        
        # Test statistics
        print_info("Testing statistics...")
        stats = memory.get_statistics()
        assert "total_commands" in stats, "Statistics incomplete"
        print_success(f"Statistics work - {stats['total_commands']} commands")
        
        # Cleanup
        memory.close()
        if os.path.exists("test_memory.db"):
            os.remove("test_memory.db")
        
        print_success("Memory system: ALL TESTS PASSED")
        return True
    
    except Exception as e:
        print_error(f"Memory system test failed: {e}")
        return False


def test_whisper_voice() -> bool:
    """Test Whisper voice recognition."""
    print_header("Testing Whisper Voice")
    
    try:
        from whisper_voice import HybridVoice
        
        # Initialize
        print_info("Initializing voice system...")
        voice = HybridVoice(prefer_offline=True)
        print_success("Voice system initialized")
        
        # Check status
        status = voice.get_status()
        print_info(f"Whisper available: {status['whisper_available']}")
        print_info(f"Google available: {status['google_available']}")
        print_info(f"Offline capable: {status['offline_capable']}")
        
        if status['whisper_available']:
            print_success("Whisper is ready (offline mode)")
        elif status['google_available']:
            print_warning("Only Google Speech available (online mode)")
        else:
            print_error("No voice recognition available")
            return False
        
        print_success("Whisper voice: TESTS PASSED")
        return True
    
    except Exception as e:
        print_error(f"Whisper voice test failed: {e}")
        return False


def test_rag_system() -> bool:
    """Test RAG system functionality."""
    print_header("Testing RAG System")
    
    try:
        from rag_system import RAGSystem
        
        # Initialize
        print_info("Initializing RAG system...")
        rag = RAGSystem(storage_path="test_rag_data")
        
        # Check status
        stats = rag.get_statistics()
        print_info(f"Embeddings available: {stats['embeddings_available']}")
        print_info(f"FAISS available: {stats['faiss_available']}")
        print_info(f"System ready: {stats['ready']}")
        
        if not stats['ready']:
            print_warning("RAG system not fully ready (missing dependencies)")
            print_info("Install: pip install sentence-transformers faiss-cpu")
            return False
        
        print_success("RAG system initialized")
        
        # Test document addition
        print_info("Testing document addition...")
        success = rag.add_document(
            "This is a test document about Python programming.",
            {"topic": "test"}
        )
        assert success, "Failed to add document"
        print_success("Document addition works")
        
        # Test search
        print_info("Testing search...")
        results = rag.search("Python", top_k=1)
        assert len(results) > 0, "Search returned no results"
        print_success(f"Search works - found {len(results)} results")
        
        # Test context generation
        print_info("Testing context generation...")
        context = rag.get_context("Python programming")
        assert len(context) > 0, "Context generation failed"
        print_success("Context generation works")
        
        # Cleanup
        rag.clear()
        import shutil
        if os.path.exists("test_rag_data"):
            shutil.rmtree("test_rag_data")
        
        print_success("RAG system: ALL TESTS PASSED")
        return True
    
    except Exception as e:
        print_error(f"RAG system test failed: {e}")
        return False


def test_ai_brain_integration() -> bool:
    """Test AI brain with new memory system."""
    print_header("Testing AI Brain Integration")
    
    try:
        from ai_brain import AIBrain
        
        # Initialize with SQLite
        print_info("Initializing AI brain with SQLite...")
        brain = AIBrain(use_sqlite=True)
        print_success("AI brain initialized")
        
        # Test processing
        print_info("Testing command processing...")
        result = brain.process_input("open chrome", device_id="test_device")
        assert "intent" in result, "Processing failed"
        assert "response" in result, "No response generated"
        print_success(f"Processing works - Intent: {result['intent']}")
        
        # Test statistics (SQLite only)
        if brain.use_sqlite:
            print_info("Testing statistics...")
            stats = brain.get_statistics()
            assert "total_commands" in stats, "Statistics incomplete"
            print_success(f"Statistics work - {stats['total_commands']} commands")
        
        # Test preferences
        if brain.use_sqlite:
            print_info("Testing preferences...")
            brain.set_preference("test_pref", "test_value")
            value = brain.get_preference("test_pref")
            assert value == "test_value", "Preference not stored"
            print_success("Preferences work")
        
        # Cleanup
        brain.close()
        if os.path.exists("christa_memory.db"):
            os.remove("christa_memory.db")
        
        print_success("AI Brain integration: ALL TESTS PASSED")
        return True
    
    except Exception as e:
        print_error(f"AI brain integration test failed: {e}")
        return False


def test_ollama_connection() -> bool:
    """Test Ollama LLM connection."""
    print_header("Testing Ollama Connection")
    
    try:
        import requests
        
        print_info("Checking Ollama server...")
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        
        if response.status_code == 200:
            print_success("Ollama server is running")
            
            # List models
            data = response.json()
            models = data.get("models", [])
            
            if models:
                print_info(f"Available models: {len(models)}")
                for model in models[:3]:  # Show first 3
                    print(f"  • {model.get('name', 'unknown')}")
                print_success("Ollama: READY")
            else:
                print_warning("No models installed")
                print_info("Install a model: ollama pull llama3")
            
            return True
        else:
            print_error("Ollama server not responding correctly")
            return False
    
    except requests.exceptions.ConnectionError:
        print_error("Ollama server not running")
        print_info("Start Ollama and run: ollama run llama3")
        return False
    except Exception as e:
        print_error(f"Ollama test failed: {e}")
        return False


def generate_report(results: Dict[str, bool]):
    """Generate final test report."""
    print_header("Test Report")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
    print(f"Success Rate: {(passed/total)*100:.1f}%\n")
    
    # Detailed results
    print("Detailed Results:")
    for test, result in results.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if result else f"{Colors.RED}❌ FAIL{Colors.RESET}"
        print(f"  {test}: {status}")
    
    # Recommendations
    print(f"\n{Colors.BOLD}Recommendations:{Colors.RESET}")
    
    if not results.get("opt_whisper", False):
        print_warning("Install Whisper for offline voice: pip install openai-whisper")
    
    if not results.get("opt_sentence_transformers", False):
        print_warning("Install Sentence Transformers: pip install sentence-transformers")
    
    if not results.get("opt_faiss", False):
        print_warning("Install FAISS: pip install faiss-cpu")
    
    if not results.get("ollama", False):
        print_warning("Install and start Ollama: https://ollama.com")
    
    # Overall status
    print(f"\n{Colors.BOLD}Overall Status:{Colors.RESET}")
    
    core_tests = ["memory_system", "ai_brain"]
    core_passed = all(results.get(t, False) for t in core_tests)
    
    if core_passed:
        print_success("Core system is working!")
    else:
        print_error("Core system has issues - check failed tests")
    
    optional_tests = ["opt_whisper", "opt_sentence_transformers", "opt_faiss"]
    optional_passed = sum(1 for t in optional_tests if results.get(t, False))
    
    if optional_passed == len(optional_tests):
        print_success("All optional features available!")
    elif optional_passed > 0:
        print_warning(f"Some optional features available ({optional_passed}/{len(optional_tests)})")
    else:
        print_warning("No optional features installed")


def main():
    """Run all tests."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║        🆓 Christa AI - FREE Stack Test Suite              ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    results = {}
    
    # Run tests
    import_results = test_imports()
    results.update(import_results)
    
    if results.get("memory_system", False):
        results["memory_system_test"] = test_memory_system()
    
    if results.get("whisper_voice", False):
        results["whisper_voice_test"] = test_whisper_voice()
    
    if results.get("rag_system", False):
        results["rag_system_test"] = test_rag_system()
    
    if results.get("ai_brain", False):
        results["ai_brain_test"] = test_ai_brain_integration()
    
    results["ollama"] = test_ollama_connection()
    
    # Generate report
    generate_report(results)
    
    print(f"\n{Colors.BOLD}Test suite completed!{Colors.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        sys.exit(1)

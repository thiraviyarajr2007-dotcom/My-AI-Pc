"""Test Ollama integration with AI Brain"""

from ai_brain import AIBrain

print("=" * 60)
print("  Testing Ollama Integration")
print("=" * 60)

# Initialize AI Brain
brain = AIBrain(use_sqlite=True)

print(f"\nOllama Status: {'✅ Connected' if brain.ollama_available else '❌ Not connected'}")
print(f"Model: {brain.model}")

# Test with a simple command
print("\n" + "─" * 60)
print("Test 1: Simple greeting")
print("─" * 60)
result = brain.process_input("hello", device_id="laptop")
print(f"Input: hello")
print(f"Intent: {result['intent']}")
print(f"Response: {result['response']}")

# Test with a command
print("\n" + "─" * 60)
print("Test 2: Command")
print("─" * 60)
result = brain.process_input("open chrome", device_id="laptop")
print(f"Input: open chrome")
print(f"Intent: {result['intent']}")
print(f"Response: {result['response']}")

# Test with a question
print("\n" + "─" * 60)
print("Test 3: Question")
print("─" * 60)
result = brain.process_input("what can you do?", device_id="laptop")
print(f"Input: what can you do?")
print(f"Intent: {result['intent']}")
print(f"Response: {result['response']}")

# Show statistics
print("\n" + "=" * 60)
print("  Statistics")
print("=" * 60)
stats = brain.get_statistics()
print(f"Total commands: {stats['total_commands']}")
print(f"Successful: {stats['successful_commands']}")

brain.close()

print("\n✅ Test complete!")
print("=" * 60)

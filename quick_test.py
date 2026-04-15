"""Quick test of Christa AI features"""

from ai_brain import AIBrain

print("=" * 60)
print("  🧪 Quick Feature Test")
print("=" * 60)

# Initialize
brain = AIBrain(use_sqlite=True)

# Test commands
test_commands = [
    "open chrome",
    "find my documents",
    "take a screenshot",
    "what can you do?"
]

for cmd in test_commands:
    print(f"\n📝 Input: '{cmd}'")
    result = brain.process_input(cmd, device_id="laptop")
    print(f"   Intent: {result['intent']} ({result['confidence']:.0%})")
    print(f"   Response: {result['response']}")
    if result['action']['module']:
        print(f"   Action: {result['action']['module']}.{result['action']['function']}")

# Show statistics
print("\n" + "=" * 60)
print("  📊 Statistics")
print("=" * 60)
stats = brain.get_statistics()
print(f"Total commands: {stats['total_commands']}")
print(f"Successful: {stats['successful_commands']}")

brain.close()
print("\n✅ Test complete!")

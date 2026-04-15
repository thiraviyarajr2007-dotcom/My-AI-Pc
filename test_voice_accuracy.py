"""
Voice Recognition Accuracy Test
Test different settings to find what works best for you
"""

import sys
from whisper_voice_enhanced import HybridVoiceEnhanced, WHISPER_AVAILABLE, SR_AVAILABLE

def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def test_accuracy():
    """Test voice recognition accuracy with different settings."""
    
    print_header("🎤 Voice Recognition Accuracy Test")
    
    if not WHISPER_AVAILABLE and not SR_AVAILABLE:
        print("❌ No voice recognition available!")
        print("Install: pip install openai-whisper")
        return
    
    print("This test will help you find the best settings for accuracy.\n")
    
    # Test phrases
    test_phrases = [
        "open chrome",
        "find my documents",
        "take a screenshot",
        "what can you do",
        "search for python files"
    ]
    
    print("📝 Test Phrases:")
    for i, phrase in enumerate(test_phrases, 1):
        print(f"   {i}. {phrase}")
    
    print("\n" + "=" * 60)
    print("  Choose Whisper Model:")
    print("  1. small (RECOMMENDED) - Best accuracy/speed balance")
    print("  2. medium - Higher accuracy, slower")
    print("  3. base - Faster, lower accuracy")
    print("  4. Use Google Speech (online)")
    print("=" * 60)
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "4":
        # Use Google
        print("\n[ℹ️] Using Google Speech Recognition (online)")
        voice = HybridVoiceEnhanced(prefer_offline=False, model_size="base")
    else:
        # Use Whisper
        model_map = {"1": "small", "2": "medium", "3": "base"}
        model_size = model_map.get(choice, "small")
        print(f"\n[ℹ️] Using Whisper '{model_size}' model")
        voice = HybridVoiceEnhanced(prefer_offline=True, model_size=model_size)
    
    print("\n" + "=" * 60)
    print("  🎯 Tips for Best Results:")
    print("=" * 60)
    print("  • Speak clearly at normal pace")
    print("  • Reduce background noise")
    print("  • Position mic 6-12 inches from mouth")
    print("  • Wait for 'Listening...' before speaking")
    print("  • Speak the phrase exactly as shown")
    print("=" * 60)
    
    # Test each phrase
    results = []
    
    for i, expected_phrase in enumerate(test_phrases, 1):
        print(f"\n\n{'─' * 60}")
        print(f"Test {i}/{len(test_phrases)}")
        print(f"{'─' * 60}")
        print(f"\n📢 Say: '{expected_phrase}'")
        
        input("Press Enter when ready to speak...")
        
        # Listen
        recognized = voice.listen(timeout=10, auto_stop=True)
        
        if recognized:
            print(f"\n✅ You said: '{recognized}'")
            
            # Check accuracy
            recognized_lower = recognized.lower().strip()
            expected_lower = expected_phrase.lower().strip()
            
            if recognized_lower == expected_lower:
                print("🎯 PERFECT MATCH!")
                accuracy = 100
            elif expected_lower in recognized_lower or recognized_lower in expected_lower:
                print("✓ Close match")
                accuracy = 80
            else:
                print("⚠️ Different from expected")
                accuracy = 50
            
            results.append({
                "expected": expected_phrase,
                "recognized": recognized,
                "accuracy": accuracy
            })
        else:
            print("\n❌ No speech detected")
            results.append({
                "expected": expected_phrase,
                "recognized": None,
                "accuracy": 0
            })
    
    # Show results
    print_header("📊 Test Results")
    
    total_accuracy = 0
    successful = 0
    
    for i, result in enumerate(results, 1):
        print(f"\nTest {i}:")
        print(f"  Expected:   '{result['expected']}'")
        if result['recognized']:
            print(f"  Recognized: '{result['recognized']}'")
            print(f"  Accuracy:   {result['accuracy']}%")
            total_accuracy += result['accuracy']
            successful += 1
        else:
            print(f"  Recognized: (none)")
            print(f"  Accuracy:   0%")
    
    # Overall score
    print(f"\n{'─' * 60}")
    print(f"Overall Results:")
    print(f"  Successful: {successful}/{len(test_phrases)}")
    if successful > 0:
        avg_accuracy = total_accuracy / len(test_phrases)
        print(f"  Average Accuracy: {avg_accuracy:.1f}%")
        
        if avg_accuracy >= 90:
            print(f"\n  🎉 EXCELLENT! Your setup is working great!")
        elif avg_accuracy >= 70:
            print(f"\n  ✓ GOOD! Consider using 'medium' model for better accuracy")
        elif avg_accuracy >= 50:
            print(f"\n  ⚠️ FAIR. Try these improvements:")
            print(f"     • Use 'small' or 'medium' Whisper model")
            print(f"     • Reduce background noise")
            print(f"     • Speak more clearly")
            print(f"     • Use a better microphone")
        else:
            print(f"\n  ❌ NEEDS IMPROVEMENT. Suggestions:")
            print(f"     • Check microphone is working")
            print(f"     • Reduce background noise significantly")
            print(f"     • Try Google Speech (option 4)")
            print(f"     • Speak louder and clearer")
    else:
        print(f"\n  ❌ No successful recognitions")
        print(f"\n  Troubleshooting:")
        print(f"     • Check microphone permissions")
        print(f"     • Test microphone in other apps")
        print(f"     • Reduce background noise")
        print(f"     • Try Google Speech (option 4)")
    
    print(f"{'─' * 60}\n")
    
    # Recommendations
    print_header("💡 Recommendations")
    
    if successful == 0:
        print("❌ Voice recognition not working properly")
        print("\n1. Check microphone:")
        print("   • Is it plugged in?")
        print("   • Does it work in other apps?")
        print("   • Check Windows sound settings")
        print("\n2. Try Google Speech:")
        print("   • Run test again and choose option 4")
        print("\n3. Check permissions:")
        print("   • Allow microphone access in Windows settings")
    
    elif avg_accuracy < 70:
        print("⚠️ Accuracy can be improved")
        print("\n1. Use better Whisper model:")
        print("   • Run test again and choose option 1 (small)")
        print("   • Or option 2 (medium) for best accuracy")
        print("\n2. Improve environment:")
        print("   • Close windows/doors")
        print("   • Turn off fans/AC")
        print("   • Use in quiet room")
        print("\n3. Better microphone:")
        print("   • Use headset mic")
        print("   • Position 6-12 inches from mouth")
    
    else:
        print("✅ Your setup is working well!")
        print("\nFor even better accuracy:")
        print("  • Use 'medium' model (slower but more accurate)")
        print("  • Ensure quiet environment")
        print("  • Speak at consistent pace")
    
    print("\n" + "=" * 60)


def quick_test():
    """Quick single test."""
    print_header("🎤 Quick Voice Test")
    
    print("Choose model:")
    print("  1. small (RECOMMENDED)")
    print("  2. medium (better accuracy)")
    print("  3. Google (online)")
    
    choice = input("\nChoice (1-3): ").strip() or "1"
    
    if choice == "3":
        voice = HybridVoiceEnhanced(prefer_offline=False)
    else:
        model = "medium" if choice == "2" else "small"
        voice = HybridVoiceEnhanced(prefer_offline=True, model_size=model)
    
    print("\n[ℹ️] Speak clearly when prompted...")
    input("Press Enter to start...")
    
    text = voice.listen(timeout=10, auto_stop=True)
    
    if text:
        print(f"\n✅ You said: '{text}'")
    else:
        print("\n❌ No speech detected")


if __name__ == "__main__":
    print("\n🎤 Voice Recognition Accuracy Tester\n")
    print("Choose test mode:")
    print("  1. Full accuracy test (5 phrases)")
    print("  2. Quick test (1 phrase)")
    
    mode = input("\nChoice (1-2): ").strip() or "1"
    
    if mode == "2":
        quick_test()
    else:
        test_accuracy()
    
    print("\n👋 Test complete!\n")

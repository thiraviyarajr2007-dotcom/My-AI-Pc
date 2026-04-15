"""
Simple Gesture Control Test
Works with MediaPipe 0.10.32+ (new API)
"""

import cv2
import os
import sys
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Import control modules
try:
    import control_ai
    import aiscreencontrol_ai
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    sys.exit(1)


def execute_gesture_action(gesture_name):
    """Execute action based on gesture."""
    actions = {
        "Pointing_Up": ("Open Chrome", lambda: control_ai.open_app('chrome')),
        "Victory": ("Take Screenshot", lambda: aiscreencontrol_ai.take_screenshot()),
        "ILoveYou": ("Open Notepad", lambda: control_ai.open_app('notepad')),
        "Open_Palm": ("Open File Explorer", lambda: control_ai.open_app('file explorer')),
    }
    
    if gesture_name in actions:
        action_name, action_func = actions[gesture_name]
        print()
        print(f"[OK] Executing: {action_name}")
        try:
            action_func()
            return action_name
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    return None


def main():
    """Main gesture control test."""
    print("=" * 60)
    print("        SIMPLE GESTURE CONTROL TEST")
    print("=" * 60)
    print()
    
    print("  Gesture Actions:")
    print("  " + "-" * 56)
    print("  Point Up       -> Open Chrome")
    print("  Victory (V)    -> Take Screenshot")
    print("  I Love You     -> Open Notepad")
    print("  Open Palm      -> Open File Explorer")
    print("  " + "-" * 56)
    print()
    print("  Instructions:")
    print("  * Hold gesture steady for 2-3 seconds")
    print("  * Keep hand in camera view")
    print("  * Good lighting helps accuracy")
    print("  * Press ESC to quit")
    print()
    print("=" * 60)
    print()
    
    # Check if gesture recognizer model exists
    model_path = "gesture_recognizer.task"
    if not os.path.exists(model_path):
        print("[INFO] Downloading gesture recognizer model...")
        print("[INFO] This may take a moment...")
        
        import urllib.request
        model_url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
        
        try:
            urllib.request.urlretrieve(model_url, model_path)
            print("[OK] Model downloaded successfully!")
        except Exception as e:
            print(f"[ERROR] Could not download model: {e}")
            print("[INFO] Please download manually from:")
            print(f"       {model_url}")
            input("Press Enter to exit...")
            return
    
    # Create gesture recognizer
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)
    
    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open camera. Make sure webcam is connected.")
        print("Press any key to exit...")
        input()
        return
    
    print("[OK] Camera opened successfully!")
    print("[>>] Starting gesture recognition...")
    print()
    
    # Gesture detection variables
    prev_gesture = None
    gesture_hold_count = 0
    TRIGGER_THRESHOLD = 30  # Frames to hold
    last_action_time = 0
    COOLDOWN_TIME = 3  # Seconds between actions
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to read from camera.")
                break
            
            # Flip for mirror view
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # Recognize gestures
            recognition_result = recognizer.recognize(mp_image)
            
            gesture_name = "No gesture"
            current_action = None
            
            if recognition_result.gestures:
                top_gesture = recognition_result.gestures[0][0]
                gesture_name = top_gesture.category_name
                confidence = top_gesture.score
                
                # Gesture hold detection
                if gesture_name == prev_gesture and gesture_name != "None":
                    gesture_hold_count += 1
                else:
                    gesture_hold_count = 0
                    prev_gesture = gesture_name
                
                # Trigger action if held long enough and cooldown passed
                current_time = time.time()
                if (gesture_hold_count == TRIGGER_THRESHOLD and 
                    current_time - last_action_time > COOLDOWN_TIME):
                    
                    current_action = execute_gesture_action(gesture_name)
                    if current_action:
                        last_action_time = current_time
                        gesture_hold_count = 0
            
            # Draw UI overlay
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, 100), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            # Title
            cv2.putText(frame, "Gesture Control Test", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Gesture name
            cv2.putText(frame, f"Gesture: {gesture_name}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Progress bar for gesture hold
            if gesture_hold_count > 0 and gesture_hold_count < TRIGGER_THRESHOLD:
                progress_width = int((gesture_hold_count / TRIGGER_THRESHOLD) * (w - 40))
                cv2.rectangle(frame, (20, 80), (20 + progress_width, 90), (0, 255, 255), -1)
                cv2.rectangle(frame, (20, 80), (w - 20, 90), (255, 255, 255), 2)
            
            # Action executed notification
            if current_action:
                cv2.rectangle(frame, (w//2 - 150, h - 80), (w//2 + 150, h - 30), (0, 255, 0), -1)
                cv2.putText(frame, f"OK: {current_action}", (w//2 - 140, h - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            
            # Instructions
            cv2.putText(frame, "Press ESC to quit", (w - 200, h - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Show frame
            cv2.imshow("Gesture Control Test", frame)
            
            # Check for ESC key
            if cv2.waitKey(1) & 0xFF == 27:
                break
    
    except KeyboardInterrupt:
        print()
        print("[STOP] Interrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print()
        print("[OK] Gesture control test stopped")
        print("Goodbye!")


if __name__ == "__main__":
    main()

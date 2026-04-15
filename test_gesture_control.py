"""
Test Gesture Control - Simple gesture recognition test
Shows live camera feed with gesture detection and executes actions
"""

import cv2
import os
import sys
import time

try:
    import mediapipe as mp
except ImportError:
    print("[!] MediaPipe not installed. Run: pip install mediapipe")
    sys.exit(1)

# Import control modules
try:
    import control_ai
    import aiscreencontrol_ai
except ImportError as e:
    print(f"[!] Import error: {e}")
    sys.exit(1)


def count_fingers(hand_landmarks, mp_hands, handedness="Right"):
    """Count the number of extended fingers."""
    if not hand_landmarks:
        return 0

    # Finger tip and pip landmark indices
    tip_ids = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]
    pip_ids = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP,
    ]

    landmarks = hand_landmarks.landmark
    fingers_up = 0

    # Thumb: check x-axis (direction depends on which hand)
    if handedness == "Right":
        if landmarks[tip_ids[0]].x < landmarks[pip_ids[0]].x:
            fingers_up += 1
    else:
        if landmarks[tip_ids[0]].x > landmarks[pip_ids[0]].x:
            fingers_up += 1

    # Other 4 fingers: tip above pip means finger is extended
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
            fingers_up += 1

    return fingers_up


def execute_gesture_action(fingers):
    """Execute action based on finger count."""
    actions = {
        1: ("Open Chrome", lambda: control_ai.open_app('chrome')),
        2: ("Take Screenshot", lambda: aiscreencontrol_ai.take_screenshot()),
        3: ("Open Notepad", lambda: control_ai.open_app('notepad')),
        4: ("Open Calculator", lambda: control_ai.open_app('calculator')),
        5: ("Open File Explorer", lambda: control_ai.open_app('file explorer')),
    }
    
    if fingers in actions:
        action_name, action_func = actions[fingers]
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
    print("        GESTURE CONTROL TEST")
    print("=" * 60)
    print()
    
    print("  Gesture Actions:")
    print("  " + "-" * 56)
    print("  1 finger  (Point)      -> Open Chrome")
    print("  2 fingers (Peace)      -> Take Screenshot")
    print("  3 fingers              -> Open Notepad")
    print("  4 fingers              -> Open Calculator")
    print("  5 fingers (Open Palm)  -> Open File Explorer")
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
    
    # Initialize MediaPipe
    try:
        # Try new API first (mediapipe >= 0.10.8)
        import mediapipe.python.solutions as solutions
        mp_hands = solutions.hands
        mp_drawing = solutions.drawing_utils
    except (ImportError, AttributeError):
        # Fallback to old API
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
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
    prev_gesture = -1
    gesture_hold_count = 0
    TRIGGER_THRESHOLD = 30  # Frames to hold (about 2 seconds at 15 fps)
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
            
            # Process hand landmarks
            results = hands.process(rgb_frame)
            
            finger_count = 0
            gesture_name = "No hand detected"
            current_action = None
            
            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Draw landmarks on frame
                    mp_drawing.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2)
                    )
                    
                    # Determine handedness
                    handedness = "Right"
                    if results.multi_handedness:
                        handedness = results.multi_handedness[idx].classification[0].label
                    
                    # Count fingers
                    finger_count = count_fingers(hand_landmarks, mp_hands, handedness)
                    
                    # Gesture names
                    gesture_names = {
                        0: "FIST (No action)",
                        1: "POINT → Chrome",
                        2: "PEACE → Screenshot",
                        3: "THREE → Notepad",
                        4: "FOUR → Calculator",
                        5: "OPEN PALM → Explorer"
                    }
                    gesture_name = gesture_names.get(finger_count, "Unknown")
                    
                    # Gesture hold detection
                    if finger_count == prev_gesture and finger_count > 0:
                        gesture_hold_count += 1
                    else:
                        gesture_hold_count = 0
                        prev_gesture = finger_count
                    
                    # Trigger action if held long enough and cooldown passed
                    current_time = time.time()
                    if (gesture_hold_count == TRIGGER_THRESHOLD and 
                        current_time - last_action_time > COOLDOWN_TIME):
                        
                        current_action = execute_gesture_action(finger_count)
                        if current_action:
                            last_action_time = current_time
                            gesture_hold_count = 0  # Reset after action
            
            # Draw UI overlay
            overlay = frame.copy()
            
            # Dark background for text
            cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            # Title
            cv2.putText(frame, "Gesture Control Test", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Finger count
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Gesture name
            cv2.putText(frame, f"Gesture: {gesture_name}", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Progress bar for gesture hold
            if gesture_hold_count > 0 and gesture_hold_count < TRIGGER_THRESHOLD:
                progress_width = int((gesture_hold_count / TRIGGER_THRESHOLD) * (w - 40))
                cv2.rectangle(frame, (20, 100), (20 + progress_width, 110), (0, 255, 255), -1)
                cv2.rectangle(frame, (20, 100), (w - 20, 110), (255, 255, 255), 2)
                
                # Progress text
                progress_pct = int((gesture_hold_count / TRIGGER_THRESHOLD) * 100)
                cv2.putText(frame, f"Hold: {progress_pct}%", (w - 150, 108),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Action executed notification
            if current_action:
                cv2.rectangle(frame, (w//2 - 150, h - 80), (w//2 + 150, h - 30), (0, 255, 0), -1)
                cv2.putText(frame, f"✓ {current_action}", (w//2 - 140, h - 50),
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
        hands.close()
        print()
        print("[OK] Gesture control test stopped")
        print("Goodbye!")


if __name__ == "__main__":
    main()

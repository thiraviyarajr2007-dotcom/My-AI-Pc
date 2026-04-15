"""
Gesture AI Module - Hand Gesture Recognition & Control
Uses MediaPipe Hands for real-time hand tracking and gesture-to-action mapping.
"""

import cv2
import sys
import os


def _get_mediapipe_hands():
    """
    Initialize MediaPipe Hands with compatibility for both old and new API versions.
    Returns (hands_detector, mp_hands_module, mp_drawing_module) or raises ImportError.
    """
    try:
        import mediapipe as mp

        # Try the legacy solutions API first (works for most installed versions)
        if hasattr(mp, 'solutions') and hasattr(mp.solutions, 'hands'):
            mp_hands = mp.solutions.hands
            mp_drawing = mp.solutions.drawing_utils
            hands = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5,
            )
            return hands, mp_hands, mp_drawing
        else:
            raise AttributeError("mp.solutions.hands not available")

    except (ImportError, AttributeError) as e:
        print(f"[✗] MediaPipe error: {e}")
        print("    Install a compatible version: pip install mediapipe==0.10.9")
        sys.exit(1)


def count_fingers(hand_landmarks, mp_hands, handedness="Right"):
    """
    Count the number of extended fingers given hand landmarks.
    Returns an integer 0-5.
    """
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


def detect_gesture(fingers):
    """
    Map finger count to a gesture name.
    """
    gestures = {
        0: "FIST (closed)",
        1: "POINTING (index up)",
        2: "PEACE / VICTORY",
        3: "THREE",
        4: "FOUR",
        5: "OPEN PALM (all up)",
    }
    return gestures.get(fingers, "UNKNOWN")


# ─── Gesture-to-Action Map ─────────────────────────────────────
def _action_none():
    pass


def _action_open_chrome():
    os.system("start chrome")
    print("[▶] Opening Chrome...")


def _action_screenshot():
    try:
        import pyautogui
        path = os.path.join(os.path.expanduser("~"), "Desktop", "gesture_screenshot.png")
        pyautogui.screenshot(path)
        print(f"[▶] Screenshot saved to {path}")
    except ImportError:
        print("[✗] pyautogui not installed for screenshot")


def _action_open_notepad():
    os.system("start notepad")
    print("[▶] Opening Notepad...")


GESTURE_ACTIONS = {
    0: ("Fist — No action", _action_none),
    1: ("Point — Open Chrome", _action_open_chrome),
    2: ("Peace — Take Screenshot", _action_screenshot),
    3: ("Three — Open Notepad", _action_open_notepad),
    4: ("Four — No action", _action_none),
    5: ("Open Palm — No action", _action_none),
}


def run_gesture_control():
    """
    Main gesture control loop with camera feed and real-time hand tracking.
    """
    hands, mp_hands, mp_drawing = _get_mediapipe_hands()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[✗] Cannot open camera. Make sure a webcam is connected.")
        return

    print("=" * 50)
    print("  🖐️  Gesture AI Controller - Ready")
    print("=" * 50)
    print("  Gesture Actions:")
    for fingers, (desc, _) in GESTURE_ACTIONS.items():
        print(f"    {fingers} finger(s) → {desc}")
    print("  Press ESC to quit")
    print("=" * 50)

    prev_gesture = -1
    gesture_hold_count = 0
    GESTURE_TRIGGER_THRESHOLD = 15  # frames to hold before triggering action

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[!] Failed to read from camera.")
                break

            # Flip for mirror view
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process hand landmarks
            results = hands.process(rgb_frame)

            finger_count = 0
            gesture_name = "No hand detected"

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Draw landmarks on frame
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    # Determine handedness
                    handedness = "Right"
                    if results.multi_handedness:
                        handedness = results.multi_handedness[idx].classification[0].label

                    finger_count = count_fingers(hand_landmarks, mp_hands, handedness)
                    gesture_name = detect_gesture(finger_count)

                    # Gesture hold detection — only trigger after holding gesture
                    if finger_count == prev_gesture:
                        gesture_hold_count += 1
                    else:
                        gesture_hold_count = 0
                        prev_gesture = finger_count

                    if gesture_hold_count == GESTURE_TRIGGER_THRESHOLD:
                        action_desc, action_func = GESTURE_ACTIONS.get(
                            finger_count, ("Unknown", _action_none)
                        )
                        print(f"[✓] Gesture triggered: {action_desc}")
                        action_func()

            # Draw UI overlay
            cv2.rectangle(frame, (0, 0), (350, 90), (0, 0, 0), -1)
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Gesture: {gesture_name}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Progress bar for gesture hold
            if gesture_hold_count > 0 and gesture_hold_count < GESTURE_TRIGGER_THRESHOLD:
                progress = int((gesture_hold_count / GESTURE_TRIGGER_THRESHOLD) * 300)
                cv2.rectangle(frame, (10, 80), (10 + progress, 85), (0, 255, 255), -1)

            cv2.imshow("Gesture AI Controller", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        print("👋 Gesture control stopped.")


if __name__ == "__main__":
    run_gesture_control()
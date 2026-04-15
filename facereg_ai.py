"""
Face Recognition AI Module - Face Detection & Recognition
Uses OpenCV Haar Cascades for detection and optionally face_recognition library for identification.
"""

import cv2
import os
import sys
import json
import numpy as np
from datetime import datetime


# ─── Paths ─────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(SCRIPT_DIR, "known_faces")
FACE_LOG_FILE = os.path.join(SCRIPT_DIR, "face_log.json")


def _load_haar_cascade():
    """Load OpenCV's built-in Haar cascade for face detection."""
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        print(f"[✗] Failed to load Haar cascade from: {cascade_path}")
        sys.exit(1)
    return cascade


def _try_load_face_recognition():
    """Try to import face_recognition library. Returns None if not available."""
    try:
        import face_recognition
        return face_recognition
    except ImportError:
        print("[!] face_recognition library not installed.")
        print("    For face ID features, install: pip install face_recognition")
        print("    Falling back to detection-only mode.\n")
        return None


def load_known_faces(face_rec_lib):
    """
    Load known face encodings from the known_faces directory.
    Each subfolder name = person name, containing their face images.
    
    Structure:
        known_faces/
            John/
                photo1.jpg
                photo2.jpg
            Jane/
                photo1.jpg
    """
    known_encodings = []
    known_names = []

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
        print(f"[!] Created known_faces directory: {KNOWN_FACES_DIR}")
        print(f"    Add subdirectories with person names containing their photos.")
        return known_encodings, known_names

    for person_name in os.listdir(KNOWN_FACES_DIR):
        person_dir = os.path.join(KNOWN_FACES_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue

        for img_file in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_file)
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                continue

            try:
                image = face_rec_lib.load_image_file(img_path)
                encodings = face_rec_lib.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_names.append(person_name)
                    print(f"  [✓] Loaded face: {person_name} ({img_file})")
                else:
                    print(f"  [!] No face found in: {img_path}")
            except Exception as e:
                print(f"  [✗] Error loading {img_path}: {e}")

    print(f"  Total known faces loaded: {len(known_encodings)}")
    return known_encodings, known_names


def log_face_detection(name, timestamp):
    """Log detected face to a JSON file."""
    log_entry = {"name": name, "timestamp": timestamp}
    log = []
    if os.path.exists(FACE_LOG_FILE):
        try:
            with open(FACE_LOG_FILE, "r") as f:
                log = json.load(f)
        except (json.JSONDecodeError, IOError):
            log = []

    log.append(log_entry)

    # Keep last 100 entries
    log = log[-100:]

    try:
        with open(FACE_LOG_FILE, "w") as f:
            json.dump(log, f, indent=2)
    except IOError as e:
        print(f"[!] Could not write face log: {e}")


def run_face_detection():
    """
    Main face detection/recognition loop.
    - Always does face DETECTION (Haar cascade — no extra deps)
    - Does face RECOGNITION if face_recognition library is installed
    """
    print("=" * 50)
    print("  👤 Face Recognition AI - Starting")
    print("=" * 50)

    face_cascade = _load_haar_cascade()
    face_rec = _try_load_face_recognition()

    known_encodings = []
    known_names = []
    recognition_mode = False

    if face_rec:
        print("\n[⏳] Loading known faces...")
        known_encodings, known_names = load_known_faces(face_rec)
        recognition_mode = len(known_encodings) > 0
        if recognition_mode:
            print(f"[✓] Recognition mode: ON ({len(known_encodings)} faces)")
        else:
            print("[!] No known faces loaded. Running detection-only mode.")
            print(f"    Add face photos to: {KNOWN_FACES_DIR}/<PersonName>/photo.jpg")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[✗] Cannot open camera. Make sure a webcam is connected.")
        return

    print("\n  Press ESC to quit")
    print("  Press 'S' to save a snapshot")
    print("=" * 50)

    face_count_total = 0
    frame_skip = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[!] Failed to read from camera.")
                break

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces using Haar cascade
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60),
            )

            # Recognition (every 3rd frame for performance)
            names_for_faces = []
            if recognition_mode and face_rec and frame_skip % 3 == 0:
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                face_locations = face_rec.face_locations(rgb_small)
                face_encodings = face_rec.face_encodings(rgb_small, face_locations)

                for encoding in face_encodings:
                    matches = face_rec.compare_faces(known_encodings, encoding, tolerance=0.6)
                    name = "Unknown"

                    if True in matches:
                        face_distances = face_rec.face_distance(known_encodings, encoding)
                        best_match_idx = np.argmin(face_distances)
                        if matches[best_match_idx]:
                            name = known_names[best_match_idx]
                            confidence = round((1 - face_distances[best_match_idx]) * 100, 1)
                            name = f"{name} ({confidence}%)"

                    names_for_faces.append(name)
            frame_skip += 1

            # Draw bounding boxes
            for i, (x, y, w, h) in enumerate(faces):
                # Color: green for known, red for unknown
                label = "Face Detected"
                color = (0, 255, 0)

                if i < len(names_for_faces):
                    label = names_for_faces[i]
                    if "Unknown" in label:
                        color = (0, 0, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # UI overlay
            cv2.rectangle(frame, (0, 0), (300, 50), (0, 0, 0), -1)
            mode_text = "Mode: Recognition" if recognition_mode else "Mode: Detection"
            cv2.putText(frame, f"Faces: {len(faces)} | {mode_text}", (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            face_count_total += len(faces)

            cv2.imshow("Face Recognition AI", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('s') or key == ord('S'):
                snap_path = os.path.join(
                    os.path.expanduser("~"), "Desktop",
                    f"face_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                cv2.imwrite(snap_path, frame)
                print(f"[✓] Snapshot saved: {snap_path}")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"👋 Face detection stopped. Total face detections: {face_count_total}")


if __name__ == "__main__":
    run_face_detection()
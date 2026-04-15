"""
Simple Camera Test - Just opens camera to verify it works
"""

import cv2
import sys

print("=" * 60)
print("        CAMERA TEST")
print("=" * 60)
print()
print("Testing camera...")
print()

# Try to open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] Cannot open camera!")
    print()
    print("Possible reasons:")
    print("  1. Camera is not connected")
    print("  2. Camera is being used by another application")
    print("  3. Camera drivers not installed")
    print()
    print("Please check your camera and try again.")
    input("Press Enter to exit...")
    sys.exit(1)

print("[OK] Camera opened successfully!")
print()
print("Camera window will open...")
print("Press ESC to close")
print()

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("[ERROR] Cannot read from camera")
            break
        
        # Flip for mirror view
        frame = cv2.flip(frame, 1)
        
        # Add text
        cv2.putText(frame, "Camera Test - Press ESC to quit", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow("Camera Test", frame)
        
        # Check for ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break

except KeyboardInterrupt:
    print()
    print("[STOP] Interrupted")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print()
    print("[OK] Camera test completed")
    print("Goodbye!")

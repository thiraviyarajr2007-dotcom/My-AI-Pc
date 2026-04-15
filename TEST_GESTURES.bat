@echo off
echo ========================================
echo   Gesture Control Test
echo ========================================
echo.
echo   Testing gesture recognition...
echo.
echo   Gestures:
echo   1 finger  = Open Chrome
echo   2 fingers = Take Screenshot
echo   3 fingers = Open Notepad
echo   4 fingers = Open Calculator
echo   5 fingers = Open File Explorer
echo.
echo   Hold gesture for 2-3 seconds
echo   Press ESC to quit
echo.
echo ========================================
echo.

python test_gesture_simple.py

pause

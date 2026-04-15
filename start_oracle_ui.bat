@echo off
echo ========================================
echo   Starting Christa AI - Oracle UI
echo ========================================
echo.

REM Check if Ollama is running
echo [1/3] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Ollama not running. Starting Ollama...
    start "Ollama Server" cmd /k "ollama serve"
    timeout /t 3 >nul
) else (
    echo [OK] Ollama is running
)

echo.
echo [2/3] Starting Christa UI Server...
echo.
echo ========================================
echo   Open your browser and go to:
echo   http://localhost:5000
echo ========================================
echo.
echo [3/3] Launching UI...
echo.

python christa_ui.py

pause

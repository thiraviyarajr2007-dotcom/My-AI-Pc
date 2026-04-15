@echo off
echo ========================================
echo   Christa AI - Web UI Launcher
echo ========================================
echo.

REM Check if Ollama is running
echo [1/2] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama not running. Starting Ollama server...
    start /B ollama serve
    timeout /t 3 /nobreak >nul
    echo Ollama started!
) else (
    echo Ollama is already running!
)

echo.
echo [2/2] Starting Christa AI Web UI...
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.

REM Start the web UI
python christa_ui.py

pause

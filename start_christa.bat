@echo off
echo ========================================
echo   Starting Christa AI Complete System
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
echo [2/2] Starting Christa AI...
echo.

REM Start the complete system
python christa_complete.py

pause

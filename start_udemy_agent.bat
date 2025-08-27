@echo off
REM Udemy Agent Startup Script
REM This script starts the Udemy agent in production mode

echo ========================================
echo Udemy Free Course Monitor Agent
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists and activate it
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your email settings
    echo.
    echo The agent will continue anyway, but email notifications may not work.
)

echo Starting Udemy Agent in production mode...
echo Press Ctrl+C to stop the agent
echo.

python udemy_agent_production.py

echo.
echo Udemy Agent stopped.
pause
@echo off
REM Udemy Agent Daemon Startup Script
REM This script starts the Udemy agent as a background daemon

echo ========================================
echo Udemy Agent Background Daemon
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

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your email settings
    echo.
    echo The agent will continue anyway, but email notifications may not work.
)

echo Starting Udemy Agent Daemon...
echo.

python udemy_daemon.py start

echo.
echo Daemon started! Use these commands to manage it:
echo.
echo   python udemy_daemon.py status    - Check status
echo   python udemy_daemon.py logs      - View logs
echo   python udemy_daemon.py stop      - Stop daemon
echo.
pause
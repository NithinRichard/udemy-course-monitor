@echo off
REM Udemy Agent Deployment Script
REM This script sets up the Udemy agent for daily automated operation

echo ========================================
echo Udemy Agent Deployment
echo ========================================
echo.

echo This will set up your Udemy agent to run daily.
echo The agent will:
echo - Run in the background
echo - Check for new courses every 24 hours
echo - Send email notifications
echo - Handle errors automatically
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

REM Check .env file
if not exist .env (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your email settings:
    echo   - SMTP_USERNAME=your-email@gmail.com
    echo   - SMTP_PASSWORD=your-gmail-app-password
    echo.
    echo The agent will still work but email notifications will be disabled.
    echo.
)

REM Test the agent
echo.
echo Testing the agent...
python udemy_agent_production.py
if %errorlevel% neq 0 (
    echo ERROR: Agent test failed!
    echo Please check the logs and fix any issues.
    pause
    exit /b 1
)

REM Ask user how they want to run it
echo.
echo SUCCESS! Agent is working correctly.
echo.
echo How do you want to run the agent daily?
echo.
echo 1. Background Daemon (Recommended)
echo    - Runs invisibly in background
echo    - Starts automatically with computer
echo    - Easy to manage and monitor
echo.
echo 2. Windows Task Scheduler
echo    - Uses Windows built-in scheduler
echo    - More integrated with Windows
echo    - Can run even when not logged in
echo.
echo 3. Manual Startup
echo    - You start it manually each time
echo    - Good for testing and control
echo.

set /p choice="Choose option (1, 2, or 3): "

if "%choice%"=="1" (
    goto :daemon_setup
) else if "%choice%"=="2" (
    goto :scheduler_setup
) else if "%choice%"=="3" (
    goto :manual_setup
) else (
    echo Invalid choice. Setting up daemon by default.
    goto :daemon_setup
)

:daemon_setup
echo.
echo Setting up Background Daemon...
echo.
echo Starting the Udemy agent daemon...
python udemy_daemon.py start

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Daemon is now running.
    echo.
    echo To manage the daemon:
    echo   python udemy_daemon.py status   - Check status
    echo   python udemy_daemon.py logs     - View logs
    echo   python udemy_daemon.py stop     - Stop daemon
    echo   python udemy_daemon.py restart  - Restart daemon
    echo.
    echo The agent will now run daily in the background!
) else (
    echo ERROR: Failed to start daemon!
    goto :scheduler_setup
)
goto :end

:scheduler_setup
echo.
echo Setting up Windows Task Scheduler...
echo.
echo This will create a scheduled task to run the agent daily.
echo.

REM Create a scheduled task
schtasks /create /tn "Udemy Course Monitor" /tr "%~dp0start_udemy_agent.bat" /sc daily /st 09:00 /rl highest /f

if %errorlevel% equ 0 (
    echo SUCCESS! Scheduled task created.
    echo The agent will run daily at 9:00 AM.
    echo.
    echo To manage the scheduled task:
    echo - Open Task Scheduler (search for it in Start menu)
    echo - Look for "Udemy Course Monitor" in the task list
    echo - Right-click to modify, run, or delete
) else (
    echo ERROR: Failed to create scheduled task.
    echo You may need to run this as Administrator.
    goto :manual_setup
)
goto :end

:manual_setup
echo.
echo Manual Setup Selected
echo.
echo To run the agent daily:
echo.
echo 1. Double-click start_daemon.bat
echo 2. Or run: python udemy_agent_production.py
echo 3. Follow the prompts to start monitoring
echo.
echo You can also create a desktop shortcut to start_daemon.bat for easy access.
goto :end

:end
echo.
echo DEPLOYMENT COMPLETE!
echo.
echo Your Udemy agent is ready to monitor free courses daily.
echo Check your email (nithinrichard1@gmail.com) for notifications.
echo.
pause
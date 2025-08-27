@echo off
REM Setup Udemy Agent Auto-Start
REM This script adds the Udemy agent to Windows startup

echo ========================================
echo Udemy Agent Auto-Start Setup
echo ========================================
echo.

echo This will make the Udemy agent start automatically when you log in to Windows.
echo.

REM Create startup shortcut
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "TARGET_SCRIPT=%~dp0start_daemon.bat"
set "SHORTCUT_NAME=Udemy Agent.lnk"

echo Creating startup shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_FOLDER%\%SHORTCUT_NAME%'); $Shortcut.TargetPath = '%TARGET_SCRIPT%'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Udemy Agent will now start automatically when you log in.
    echo.
    echo The shortcut has been created at:
    echo %STARTUP_FOLDER%\%SHORTCUT_NAME%
    echo.
    echo To test it now, you can:
    echo 1. Log off and log back in
    echo 2. Or run start_daemon.bat manually
    echo.
) else (
    echo.
    echo ERROR: Failed to create startup shortcut.
    echo You can manually add start_daemon.bat to your startup folder.
    echo.
)

echo To manage the agent:
echo   python udemy_daemon.py status   - Check if running
echo   python udemy_daemon.py logs     - View logs
echo   python monitor_agent.py status  - Full status
echo.
pause
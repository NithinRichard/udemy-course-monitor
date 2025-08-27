@echo off
REM Udemy Agent - Push to GitHub Repository

echo ========================================
echo Udemy Agent - GitHub Upload
echo ========================================
echo.

echo This will upload your Udemy agent to GitHub repository:
echo https://github.com/NithinRichard/udemy-course-monitor.git
echo.

REM Check if .env exists (but don't commit it)
if exist .env (
    echo Found .env file (this will NOT be uploaded for security)
) else (
    echo WARNING: .env file not found!
    echo Please create it with your email settings before running this.
    echo.
    echo Copy .env.example to .env and edit it with:
    echo   SMTP_USERNAME=your-email@gmail.com
    echo   SMTP_PASSWORD=your-gmail-app-password
    echo.
    pause
    exit /b 1
)

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo Initializing Git repository...
if exist .git (
    echo Git repository already initialized.
) else (
    git init
    echo Git repository initialized.
)

echo.
echo Adding files to Git (excluding sensitive files)...
git add .

echo.
echo Checking what will be committed...
git status

echo.
echo Do you want to proceed with the commit? (y/n)
set /p proceed=
if /i not "%proceed%"=="y" (
    echo Commit cancelled.
    pause
    exit /b 0
)

echo.
echo Creating commit...
git commit -m "Udemy Free Course Monitor Agent - Production Ready

- Production-ready Udemy course monitoring agent
- Daily automated checks for free programming courses
- Email notifications to nithinrichard1@gmail.com
- GitHub Actions workflow for 24/7 cloud operation
- Multiple deployment options (daemon, service, cloud)
- Comprehensive logging and error handling
- Selenium-based scraping with anti-bot measures
- Health monitoring and auto-recovery features"

if %errorlevel% neq 0 (
    echo ERROR: Commit failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Setting up remote repository...
git remote add origin https://github.com/NithinRichard/udemy-course-monitor.git 2>nul
if %errorlevel% neq 0 (
    echo Remote 'origin' already exists or error occurred.
    git remote set-url origin https://github.com/NithinRichard/udemy-course-monitor.git
)

echo.
echo Pushing to GitHub...
git push -u origin main

if %errorlevel% neq 0 (
    echo ERROR: Push failed!
    echo.
    echo Possible issues:
    echo 1. Repository doesn't exist - Create it on GitHub first
    echo 2. Authentication issues - Make sure you have GitHub access
    echo 3. Branch name mismatch - Repository might use 'master' instead of 'main'
    echo.
    echo Try pushing to master branch instead:
    echo   git push -u origin master
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! UPLOAD COMPLETE
echo ========================================
echo.
echo Your Udemy agent has been uploaded to:
echo https://github.com/NithinRichard/udemy-course-monitor.git
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Go to Settings > Secrets and variables > Actions
echo 3. Add these secrets:
echo    - SMTP_USERNAME: nithinrichard1@gmail.com
echo    - SMTP_PASSWORD: your-gmail-app-password
echo 4. Go to Actions tab
echo 5. Click "Daily Udemy Check"
echo 6. Click "Run workflow" to test it
echo.
echo The agent will then run daily at 4:30 PM IST automatically!
echo.
pause
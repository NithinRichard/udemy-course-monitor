@echo off
REM Complete GitHub Setup for Udemy Agent

echo ========================================
echo Udemy Agent - Complete GitHub Setup
echo ========================================
echo.

echo This will:
echo 1. Upload your agent to GitHub
echo 2. Show you how to set up secrets
echo 3. Test the GitHub Actions deployment
echo.

echo Your repository: https://github.com/NithinRichard/udemy-course-monitor.git
echo.

REM Check prerequisites
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env with your email settings first.
    echo.
    pause
    exit /b 1
)

if not exist ".github\workflows\udemy-daily-check.yml" (
    echo ERROR: GitHub Actions workflow not found!
    echo Please make sure .github\workflows\udemy-daily-check.yml exists.
    echo.
    pause
    exit /b 1
)

echo Step 1: Pushing code to GitHub...
echo ========================================
call push_to_github.bat

if %errorlevel% neq 0 (
    echo Push failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Step 2: GitHub Secrets Setup
echo ================================
echo.
echo IMPORTANT: You need to add email secrets to GitHub:
echo.
echo 1. Go to: https://github.com/NithinRichard/udemy-course-monitor/settings/secrets/actions
echo 2. Click "New repository secret"
echo 3. Add these two secrets:
echo.
echo    Secret Name: SMTP_USERNAME
echo    Value: nithinrichard1@gmail.com
echo.
echo    Secret Name: SMTP_PASSWORD
echo    Value: [your 16-character Gmail app password]
echo.
echo How to get Gmail App Password:
echo - Go to https://myaccount.google.com/security
echo - Enable 2-Step Verification
echo - Go to https://myaccount.google.com/apppasswords
echo - Generate app password for "Mail"
echo - Use the 16-character password (no spaces)
echo.

set /p secrets_done="Have you added the secrets to GitHub? (y/n): "
if /i not "%secrets_done%"=="y" (
    echo.
    echo Please add the secrets first, then run this script again.
    echo Opening GitHub secrets page...
    start https://github.com/NithinRichard/udemy-course-monitor/settings/secrets/actions
    pause
    exit /b 0
)

echo.
echo Step 3: Testing GitHub Actions
echo ================================
echo.
echo Testing your GitHub Actions deployment...
echo.
echo 1. Go to: https://github.com/NithinRichard/udemy-course-monitor/actions
echo 2. Click "Daily Udemy Check" workflow
echo 3. Click "Run workflow" (dropdown) then "Run workflow"
echo 4. The workflow will start running
echo.
echo You should receive a test email when it completes!
echo.

set /p test_done="Have you tested the workflow? (y/n): "

echo.
echo ========================================
echo GITHUB DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo ✅ Code uploaded to GitHub
echo ✅ GitHub Actions workflow configured
echo ✅ Email secrets set up
echo ✅ Ready for 24/7 operation
echo.
echo Your Udemy agent will now run daily at 4:30 PM IST
echo and send email notifications to nithinrichard1@gmail.com
echo.
echo 🎉 Even when your computer is off!
echo.

echo Useful links:
echo =============
echo Repository: https://github.com/NithinRichard/udemy-course-monitor
echo Actions: https://github.com/NithinRichard/udemy-course-monitor/actions
echo Secrets: https://github.com/NithinRichard/udemy-course-monitor/settings/secrets/actions
echo.

echo To modify the schedule:
echo - Edit .github/workflows/udemy-daily-check.yml
echo - Change the cron expression (current: 9 AM UTC = 4:30 PM IST)
echo.

pause
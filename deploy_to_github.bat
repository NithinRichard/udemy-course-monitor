@echo off
REM Udemy Agent - GitHub Actions Deployment Script

echo ========================================
echo Udemy Agent - GitHub Deployment
echo ========================================
echo.

echo This will help you deploy your Udemy agent to GitHub Actions
echo so it runs 24/7 even when your computer is off.
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file with your email settings first.
    echo.
    echo Copy .env.example to .env and edit it with:
    echo   SMTP_USERNAME=your-email@gmail.com
    echo   SMTP_PASSWORD=your-gmail-app-password
    echo.
    pause
    exit /b 1
)

REM Check if workflow file exists
if not exist ".github\workflows\udemy-daily-check.yml" (
    echo Creating GitHub Actions workflow file...
    mkdir ".github\workflows" 2>nul
    copy "GITHUB_DEPLOYMENT_README.md" ".github\workflows\udemy-daily-check.yml" >nul
    echo Workflow file created.
) else (
    echo Workflow file already exists.
)

echo.
echo ========================================
echo DEPLOYMENT STEPS:
echo ========================================
echo.
echo 1. Create a GitHub repository:
echo    - Go to https://github.com
echo    - Click "New repository"
echo    - Name it "udemy-course-monitor" or similar
echo    - Make it Public or Private
echo    - DO NOT initialize with README
echo    - Click "Create repository"
echo.
echo 2. Upload your files to GitHub:
echo    - On your repository page, click "Add file" > "Upload files"
echo    - Upload ALL files from this folder
echo.
echo 3. Add email secrets:
echo    - Go to repository Settings > Secrets and variables > Actions
echo    - Add SMTP_USERNAME: nithinrichard1@gmail.com
echo    - Add SMTP_PASSWORD: your-gmail-app-password
echo.
echo 4. Test the deployment:
echo    - Go to Actions tab
echo    - Click "Daily Udemy Check"
echo    - Click "Run workflow"
echo.
echo 5. Customize schedule (optional):
echo    - Edit .github/workflows/udemy-daily-check.yml
echo    - Change the cron expression for your preferred time
echo.

echo ========================================
echo SCHEDULE EXAMPLES:
echo ========================================
echo.
echo Current: 9 AM UTC = 4:30 PM IST
echo.
echo For 9 AM IST (3:30 AM UTC):
echo   cron: '30 3 * * *'
echo.
echo For 6 PM IST (12:30 PM UTC):
echo   cron: '30 12 * * *'
echo.
echo For twice daily (9 AM and 9 PM IST):
echo   - cron: '30 3 * * *'
echo   - cron: '30 15 * * *'
echo.

echo ========================================
echo FREE TIER INFORMATION:
echo ========================================
echo.
echo GitHub Actions Free Tier:
echo - 2000 minutes per month
echo - Your agent uses ~5-10 minutes per run
echo - Can run ~200 times per month
echo - Daily runs use ~150 minutes per month
echo.
echo This means you can run DAILY with plenty of free time left!
echo.

echo ========================================
echo READY TO DEPLOY!
echo ========================================
echo.
echo Your agent is ready for GitHub Actions deployment.
echo Follow the steps above to get 24/7 operation for FREE!
echo.
echo Questions? Check GITHUB_DEPLOYMENT_README.md for detailed guide.
echo.

pause
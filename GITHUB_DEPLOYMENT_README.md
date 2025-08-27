# 🚀 Udemy Agent - GitHub Actions Cloud Deployment

## 🎯 **Deploy to GitHub Actions (FREE 24/7 Operation)**

This guide will help you deploy your Udemy agent to GitHub Actions so it runs **daily automatically, even when your computer is off**.

### **Why GitHub Actions?**
- ✅ **Completely FREE** (2000 minutes/month for free accounts)
- ✅ Runs daily at set times
- ✅ No server management needed
- ✅ Automatic email notifications
- ✅ Works 24/7 even when your computer is off

---

## 📋 **Step-by-Step Setup**

### **Step 1: Create GitHub Repository**

1. Go to https://github.com
2. Click **"New repository"**
3. Name it: `udemy-course-monitor` (or anything you like)
4. Make it **Public** or **Private** (your choice)
5. **DO NOT** initialize with README (we already have one)
6. Click **"Create repository"**

### **Step 2: Upload Your Files**

#### **Option A: Upload via GitHub Web Interface**
1. On your repository page, click **"Add file"** > **"Upload files"**
2. Upload all your Udemy agent files:
   - `udemy_agent_production.py`
   - `selenium_scraper.py`
   - `email_notifier.py`
   - `config.py`
   - `requirements.txt`
   - `.env`
   - `README.md`
   - All other files in your project

#### **Option B: Use Git (Recommended for developers)**
```bash
# If you have Git installed
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### **Step 3: Add Email Secrets**

1. In your GitHub repository, click **"Settings"** tab
2. In left sidebar, click **"Secrets and variables"** > **"Actions"**
3. Click **"New repository secret"**

#### **Add SMTP_USERNAME:**
- **Name:** `SMTP_USERNAME`
- **Value:** `nithinrichard1@gmail.com`
- Click **"Add secret"**

#### **Add SMTP_PASSWORD:**
- **Name:** `SMTP_PASSWORD`
- **Value:** Your Gmail App Password (16 characters)
- Click **"Add secret"**

### **Step 4: Create Workflow File**

1. In your repository, click **"Add file"** > **"Create new file"**
2. File name: `.github/workflows/udemy-daily-check.yml`
3. Copy and paste this content:

```yaml
name: Daily Udemy Course Check

# Run daily at 9 AM UTC (4:30 PM IST)
on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:  # Allow manual triggering

# Allow only one concurrent run
concurrency:
  group: udemy-daily-check
  cancel-in-progress: false

jobs:
  check-courses:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Create necessary directories
      run: |
        mkdir -p logs

    - name: Run Udemy Agent
      run: |
        echo "Starting Udemy Agent..."
        python udemy_agent_production.py
      env:
        SMTP_USERNAME: ${{ secrets.SMTP_USERNAME }}
        SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}

    - name: Upload logs on failure
      if: failure()
      uses: actions/upload-artifact@v3
      with:
        name: udemy-agent-logs
        path: logs/
        retention-days: 7
```

4. Click **"Commit changes"**

### **Step 5: Test the Deployment**

1. In your repository, click **"Actions"** tab
2. You should see **"Daily Udemy Course Check"** workflow
3. Click on it
4. Click **"Run workflow"** (dropdown) > **"Run workflow"**
5. The workflow will start running

### **Step 6: Monitor Results**

- Go to **"Actions"** tab to see workflow runs
- Each run shows:
  - ✅ Success (green checkmark)
  - ❌ Failure (red X)
  - 📊 Duration and logs

---

## ⏰ **Schedule Customization**

### **Change the Daily Time:**

Edit the cron expression in `.github/workflows/udemy-daily-check.yml`:

```yaml
# Current: 9 AM UTC (4:30 PM IST)
cron: '0 9 * * *'

# Examples:
cron: '0 4 * * *'   # 4 AM UTC (9:30 AM IST)
cron: '30 14 * * *'  # 2:30 PM UTC (8 PM IST)
cron: '0 12 * * *'   # 12 PM UTC (5:30 PM IST)
```

### **Run Multiple Times Per Day:**

```yaml
schedule:
  - cron: '0 9 * * *'   # 9 AM UTC
  - cron: '0 21 * * *'  # 9 PM UTC
```

---

## 📧 **Email Notifications**

The agent will send emails to **nithinrichard1@gmail.com** when:
- ✅ New free programming courses are found
- ✅ Agent starts up (first run)
- ❌ Errors occur (if any)

---

## 🔧 **Troubleshooting**

### **Workflow Not Running:**
1. Check **"Actions"** tab for errors
2. Verify secrets are set correctly
3. Check that all files are uploaded

### **Email Not Working:**
1. Verify Gmail App Password is correct
2. Check spam folder
3. Review workflow logs

### **Scraping Issues:**
- The agent handles Udemy blocks automatically
- Check workflow logs for details
- May take a few minutes to find working method

---

## 📊 **Monitoring Your Agent**

### **View Daily Runs:**
- Go to **"Actions"** tab
- See all workflow runs
- Click any run to see detailed logs

### **Check Email:**
- Agent sends emails when courses are found
- Check spam folder initially
- Emails include course links and details

---

## 🎯 **What Happens Now**

✅ **Daily at your scheduled time:**
- GitHub Actions starts a virtual machine
- Downloads your code
- Runs the Udemy agent
- Sends email notifications
- Cleans up automatically

✅ **Even when your computer is off:**
- GitHub's servers run 24/7
- You get daily email notifications
- No server management needed
- Completely FREE!

---

## 🚨 **Important Notes**

1. **GitHub Actions Free Tier:**
   - 2000 minutes/month free
   - Your agent uses ~5-10 minutes per run
   - Can run ~200 times/month for free

2. **Email Reliability:**
   - Uses your Gmail account
   - Make sure 2-Step Verification is enabled
   - Use App Password (not regular password)

3. **Time Zone:**
   - Schedule is in UTC
   - 9 AM UTC = 4:30 PM IST
   - Adjust cron expression for your preferred time

---

## 🎉 **You're Done!**

Your Udemy agent is now deployed to the cloud and will:
- ✅ Run daily automatically
- ✅ Work even when your computer is off
- ✅ Send you email notifications
- ✅ Monitor free programming courses
- ✅ Cost you $0 per month

**Enjoy your automated Udemy course notifications!** 🚀
# Udemy Agent - Cloud Deployment Guide

## 🚀 **Deploy to Cloud (Runs 24/7 Even When Your Computer is Off)**

Since you want the agent to work when your computer is off, you need to deploy it to the cloud. Here are the easiest options:

## 🎯 **Option 1: GitHub Actions (FREE & Recommended)**

### **Why GitHub Actions?**
- ✅ **Completely FREE** for basic usage
- ✅ Runs every day automatically
- ✅ No credit card required
- ✅ Easy setup

### **Setup Steps:**

1. **Create a GitHub Repository:**
   - Go to https://github.com
   - Create a new repository
   - Upload all your Udemy agent files

2. **Create `.github/workflows/daily-check.yml`:**
   ```yaml
   name: Daily Udemy Check

   on:
     schedule:
       - cron: '0 9 * * *'  # Daily at 9 AM UTC
     workflow_dispatch:     # Manual trigger

   jobs:
     check-courses:
       runs-on: ubuntu-latest

       steps:
       - name: Checkout code
         uses: actions/checkout@v3

       - name: Setup Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.9'

       - name: Install dependencies
         run: |
           pip install -r requirements.txt

       - name: Run Udemy Agent
         run: |
           python udemy_agent_production.py
         env:
           SMTP_USERNAME: ${{ secrets.SMTP_USERNAME }}
           SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
   ```

3. **Add Email Secrets:**
   - Go to your repository Settings > Secrets and variables > Actions
   - Add:
     - `SMTP_USERNAME`: your-email@gmail.com
     - `SMTP_PASSWORD`: your-gmail-app-password

4. **Test:**
   - Go to Actions tab
   - Click "Daily Udemy Check"
   - Click "Run workflow"

### **Result:**
- ✅ Runs daily at 9 AM UTC (customizable)
- ✅ Sends emails when new courses found
- ✅ Works even when your computer is off
- ✅ FREE!

---

## 🎯 **Option 2: Railway (Simple & Paid)**

### **Why Railway?**
- ✅ Simple drag-and-drop deployment
- ✅ Always-on server
- ✅ Affordable pricing

### **Setup Steps:**

1. **Create Railway Account:**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy:**
   - Click "Deploy from GitHub"
   - Connect your repository
   - Railway auto-detects Python and installs dependencies

3. **Add Environment Variables:**
   - SMTP_USERNAME=your-email@gmail.com
   - SMTP_PASSWORD=your-gmail-app-password

4. **Set Up Daily Schedule:**
   - Use Railway's cron job feature or scheduler service

### **Pricing:**
- ✅ Free tier available
- ✅ Paid: ~$5/month for always-on

---

## 🎯 **Option 3: AWS Lambda (Advanced)**

### **Why AWS Lambda?**
- ✅ Pay only for execution time
- ✅ Highly scalable
- ✅ CloudWatch for scheduling

### **Setup Steps:**

1. **Create Lambda Function:**
   - Go to AWS Console > Lambda
   - Create new function
   - Runtime: Python 3.9

2. **Upload Code:**
   - Package your code or use container deployment

3. **Add Environment Variables:**
   - SMTP_USERNAME
   - SMTP_PASSWORD

4. **Create CloudWatch Rule:**
   - Schedule to run daily
   - Trigger Lambda function

### **Pricing:**
- ✅ Very cheap (~$0.20/month for daily runs)

---

## 🎯 **Option 4: Heroku (Traditional)**

### **Why Heroku?**
- ✅ Easy deployment
- ✅ Good documentation
- ✅ Reliable hosting

### **Setup Steps:**

1. **Create Heroku Account:**
   - Go to https://heroku.com

2. **Install Heroku CLI:**
   ```bash
   # Download from heroku.com/cli
   ```

3. **Deploy:**
   ```bash
   heroku create your-udemy-agent
   git push heroku main
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set SMTP_USERNAME=your-email@gmail.com
   heroku config:set SMTP_PASSWORD=your-app-password
   ```

5. **Add Scheduler Add-on:**
   - Use Heroku Scheduler to run daily

### **Pricing:**
- ✅ Free tier available
- ✅ Paid: ~$7/month for basic dyno

---

## 📊 **Comparison Table**

| Service | Setup Difficulty | Cost | Always-On | Scheduling |
|---------|------------------|------|-----------|------------|
| **GitHub Actions** | 🟢 Easy | ✅ FREE | ❌ No | ✅ Built-in |
| **Railway** | 🟢 Easy | 💰 $5/month | ✅ Yes | 🟡 Add-on |
| **AWS Lambda** | 🔴 Hard | 💰 $0.20/month | ❌ No | ✅ Built-in |
| **Heroku** | 🟡 Medium | 💰 $7/month | ✅ Yes | 🟡 Add-on |

---

## 🚀 **Quick Recommendation**

### **For FREE (Recommended):**
**GitHub Actions** - Perfect for your needs, completely free, runs daily.

### **For Always-On Server:**
**Railway** - Simple deployment, reliable 24/7 operation.

### **For Budget:**
**AWS Lambda** - Cheapest option, but more complex setup.

---

## 🎯 **Next Steps**

1. **Choose your platform** (I recommend GitHub Actions for simplicity)
2. **Create a GitHub repository** with your Udemy agent code
3. **Follow the setup steps** above
4. **Test the deployment**
5. **Get daily notifications** even when your computer is off!

---

## 💡 **Pro Tips**

- **GitHub Actions** is perfect for daily email notifications
- **Railway/Heroku** better if you need real-time monitoring
- All options can send emails to nithinrichard1@gmail.com
- Start with GitHub Actions (free) and upgrade later if needed

**Ready to deploy to the cloud?** 🚀
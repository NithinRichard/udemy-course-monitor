# Udemy Free Course Monitor Agent

A Python agent that monitors Udemy for free programming courses and sends email notifications when new courses become available.

## Features

- Monitors Udemy's free programming courses daily
- Sends email notifications with course details
- Tracks previously seen courses to avoid duplicate notifications
- Lightweight and easy to configure

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure email settings:**
   - The `.env` file is already created with your email address
   - You need to set up a Gmail App Password:
     ```
     SMTP_PASSWORD=your-16-character-app-password
     ```
   - **Important:** Use an App Password, not your regular Gmail password
     - Go to Google Account settings > Security > 2-Step Verification > App passwords
     - Generate an app password for this application
     - The app password will be 16 characters (no spaces)

3. **Update email recipient (optional):**
   - Edit `config.py` if you want to change the recipient email address

## 🚀 Daily Operation & Deployment Options

Your Udemy agent can run **daily automatically** using several methods. Choose what works best for you:

## 💻 **IMPORTANT: Computer Shutdown Behavior**

**❌ NO - The agent does NOT run when your computer is completely shut down.**

### **What happens with each option:**

| Option | When Computer is ON | When Computer is OFF |
|--------|-------------------|---------------------|
| **Background Daemon** | ✅ Runs in background | ❌ Stops completely |
| **Auto-Start** | ✅ Restarts when you login | ❌ Stops when shut down |
| **Task Scheduler** | ✅ Runs at scheduled time | ❌ Can't run (computer off) |
| **Manual** | ✅ Runs when you start it | ❌ Not running |

### **For 24/7 Operation:**
If you need the agent to run even when you're not using your computer, you would need a dedicated server/computer that stays on continuously. This is **not necessary** for most users who just want daily email notifications.

### **Normal Daily Use:**
1. Turn on your computer
2. Start the agent (takes 30 seconds)
3. Agent runs in background while you use your computer
4. Get email notifications daily
5. Agent stops when you shut down

### 🎯 **Quick Deployment (Recommended)**

**Run this one command to set everything up:**
```bash
deploy_agent.bat
```

This will:
- ✅ Install all dependencies
- ✅ Test the agent
- ✅ Let you choose how to run it daily
- ✅ Set up automatic operation

### 📅 **Daily Operation Methods**

#### **⚠️ Important: Computer Shutdown Behavior**

**None of these methods run when your computer is completely shut down.** Here's what happens:

- **Background Daemon**: Stops when you shut down/restart
- **Auto-Start**: Restarts when you log back in
- **Task Scheduler**: Runs at scheduled time if computer is on
- **Manual**: You run it when needed

#### **Option 1: Background Daemon (Stops on Shutdown)**
```bash
# Start daemon (runs invisibly in background)
start_daemon.bat
# OR
python udemy_daemon.py start

# Check if running
python udemy_daemon.py status

# View logs
python udemy_daemon.py logs

# Stop daemon
python udemy_daemon.py stop
```

#### **Option 2: Auto-Start on Login (Restarts When You Login)**
```bash
# Set up auto-start with Windows login
setup_autostart.bat
```

#### **Option 3: Windows Task Scheduler (Runs at Set Times)**
```bash
# Create scheduled task to run daily at 9 AM
deploy_agent.bat  # Choose option 2
```

#### **Option 4: Manual Daily Operation**
```bash
# Run interactively (good for monitoring)
python udemy_agent_production.py

# Run in background for session
start_udemy_agent.bat
```

### Option 3: Manual Management

**Test run:**
```bash
python udemy_agent_production.py
```

**Background with PowerShell:**
```powershell
Start-Job -ScriptBlock { python udemy_agent_production.py }
```

## 📊 Monitoring & Management

Use the monitoring script to check agent status and manage it:

```bash
# Check agent status
python monitor_agent.py status

# View recent logs
python monitor_agent.py logs 20

# See seen courses statistics
python monitor_agent.py courses

# Send test email
python monitor_agent.py test-email

# Clean old data
python monitor_agent.py cleanup 30

# Restart agent
python monitor_agent.py restart
```

## 📧 Email Configuration

Your email is already configured! If you need to change it:

1. Edit `.env` file:
   ```
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   ```

2. Test email: `python monitor_agent.py test-email`

## 🔄 What Does "Deploy" Mean?

**Deploy** simply means setting up the agent to run automatically without manual intervention. You have several options:

### **No Deployment (Manual Mode)**
- Run `python udemy_agent_production.py` when you want to check for courses
- Good for testing and occasional use

### **Light Deployment (Background Daemon)**
- Agent runs invisibly in background
- Starts when you start it, stops when you stop it
- Perfect for daily operation

### **Full Deployment (Auto-Start)**
- Agent starts automatically when you log in to Windows
- Always available, runs every day at the same time
- Set-and-forget operation

### **Scheduled Deployment (Task Scheduler)**
- Windows runs the agent automatically at set times
- Can run even when you're not logged in
- Most automated option

## 📊 Choosing the Right Option

| Method | Automation | Visibility | Best For |
|--------|------------|------------|----------|
| Manual | None | Interactive | Testing, occasional use |
| Daemon | When started | Invisible | Daily use, manual start |
| Auto-start | Login | Invisible | Daily use, always available |
| Task Scheduler | Scheduled | Invisible | Set-and-forget operation |

## 🚀 Quick Start Guide

### **For Daily Use (Recommended):**
```bash
# 1. Run deployment setup
deploy_agent.bat

# 2. Choose Option 1 (Background Daemon)

# 3. Start the daemon
python udemy_daemon.py start
```

### **For Always-On Use:**
```bash
# 1. Run deployment setup
deploy_agent.bat

# 2. Choose Option 2 (Auto-start setup)
setup_autostart.bat
```

### **For Testing:**
```bash
# Just run the agent once
python udemy_agent_production.py
```

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
CHECK_INTERVAL_HOURS = 24      # Check frequency
EMAIL_RECIPIENT = "your@email.com"  # Notification recipient
PROGRAMMING_CATEGORY = "?category=Development"  # Course category
```

## 📋 Production Features

- **Health Monitoring**: Automatic health checks every 5 minutes
- **Auto-Recovery**: Restarts scraper if it fails
- **Graceful Shutdown**: Handles Ctrl+C and system shutdown
- **Comprehensive Logging**: Daily log rotation
- **Memory Management**: Automatic cleanup of old data
- **Process Monitoring**: Tracks CPU/memory usage

## 📊 Log Files

All logs are stored in the `logs/` directory:
- `udemy_agent_YYYYMMDD.log` - Daily agent logs
- `udemy_agent_service.log` - Service logs
- `health_status.json` - Real-time health data

## 🚨 Troubleshooting

### Agent Not Starting
```bash
# Check Python installation
python --version

# Verify dependencies
pip install -r requirements.txt

# Test email configuration
python monitor_agent.py test-email
```

### Email Not Working
```bash
# Test email separately
python test_email.py

# Check .env file has correct app password
# Make sure Gmail 2-Step Verification is enabled
```

### Scraping Issues
```bash
# Check agent logs
python monitor_agent.py logs

# The agent handles Udemy blocks automatically
# May take a few minutes to find working method
```

## 🔄 Updates & Maintenance

**To update the agent:**
1. Stop the current agent
2. Pull latest changes
3. Install new dependencies: `pip install -r requirements.txt`
4. Restart agent

**Regular maintenance:**
```bash
# Clean old logs monthly
python monitor_agent.py cleanup 30

# Check agent health weekly
python monitor_agent.py status
```

## 🎯 What's Running in Production

Your production agent includes:
- ✅ Daily course monitoring (every 24 hours)
- ✅ Email notifications to nithinrichard1@gmail.com
- ✅ Programming courses only
- ✅ Duplicate prevention
- ✅ Health monitoring
- ✅ Auto-recovery
- ✅ Comprehensive logging
- ✅ Graceful error handling

**Your Udemy Free Course Monitor Agent is now running in production!** 🎉
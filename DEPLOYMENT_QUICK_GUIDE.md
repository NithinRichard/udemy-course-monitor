# Udemy Agent - Quick Deployment Guide

## ❓ **"Does it run when I shut down my computer?"**

**SHORT ANSWER: NO** ❌

The Udemy agent runs on your local computer and **stops when you shut down or restart**.

## 📋 **What Each Option Does**

### **Background Daemon**
- ✅ Runs invisibly while your computer is on
- ❌ Stops when you shut down/restart
- ❌ Doesn't start automatically

### **Auto-Start**
- ✅ Starts automatically when you log in to Windows
- ✅ Runs invisibly while your computer is on
- ❌ Stops when you shut down/restart

### **Task Scheduler**
- ✅ Runs at scheduled times while computer is on
- ❌ Can't run if computer is off
- ❌ No notifications if computer is off

### **Manual**
- ✅ Runs only when you start it
- ❌ Stops when you close it or shut down

## 🎯 **For Daily Use (Recommended)**

### **Simple Daily Routine:**
1. **Turn on your computer**
2. **Run:** `start_daemon.bat`
3. **Agent runs in background all day**
4. **Get email notifications daily**
5. **Agent stops when you shut down**

### **One-Time Setup:**
```bash
# Run once to set up
deploy_agent.bat

# Then daily:
start_daemon.bat
```

## 🔧 **Management Commands**

```bash
# Start agent
python udemy_daemon.py start

# Check status
python udemy_daemon.py status

# View logs
python udemy_daemon.py logs

# Stop agent
python udemy_daemon.py stop
```

## 🚨 **If You Need 24/7 Operation**

For the agent to run even when you're not using your computer, you would need:
- A dedicated computer/server that stays on
- Cloud hosting (AWS, Google Cloud, etc.)

**This is overkill for most users** who just want daily email notifications.

## 🎉 **Bottom Line**

**Just run `start_daemon.bat` when you turn on your computer each day.** The agent will monitor Udemy and send you emails while you use your computer normally!
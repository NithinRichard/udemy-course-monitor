#!/usr/bin/env python3
"""
Udemy Agent Health Monitor and Management Script

This script provides monitoring and management capabilities for the Udemy agent:
- Check agent health status
- View logs
- Restart agent if needed
- Send test notifications
- Clean up old data
"""

import json
import os
import sys
import psutil
import signal
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_RECIPIENT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT

class AgentMonitor:
    """Monitor and manage the Udemy agent"""

    def __init__(self):
        self.logs_dir = Path("logs")
        self.health_file = self.logs_dir / "health_status.json"
        self.seen_courses_file = Path("seen_courses.json")

    def get_health_status(self) -> Optional[Dict]:
        """Get current agent health status"""
        if not self.health_file.exists():
            print("❌ No health status file found. Agent may not be running.")
            return None

        try:
            with open(self.health_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading health status: {e}")
            return None

    def show_status(self):
        """Display current agent status"""
        print("🔍 Udemy Agent Status")
        print("=" * 40)

        health = self.get_health_status()
        if not health:
            return

        # Basic status
        status = health.get('status', 'unknown')
        if status == 'healthy':
            print(f"📊 Status: 🟢 {status.upper()}")
        elif status == 'degraded':
            print(f"📊 Status: 🟡 {status.upper()}")
        elif status == 'error':
            print(f"📊 Status: 🔴 {status.upper()}")
        else:
            print(f"📊 Status: ⚪ {status.upper()}")

        # Statistics
        print(f"📈 Courses Found: {health.get('courses_found', 0)}")
        print(f"📧 Emails Sent: {health.get('emails_sent', 0)}")
        print(f"❌ Errors: {health.get('errors', 0)}")

        # Timing
        start_time = health.get('start_time')
        if start_time:
            try:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                uptime = datetime.now() - start_dt
                print(f"⏱️  Uptime: {uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m")
            except:
                print(f"⏱️  Started: {start_time}")

        last_check = health.get('last_check')
        if last_check:
            try:
                last_dt = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
                time_since = datetime.now() - last_dt
                print(f"🔍 Last Check: {time_since.seconds // 60}m ago")
            except:
                print(f"🔍 Last Check: {last_check}")

        # Process info
        pid = health.get('pid')
        if pid:
            try:
                process = psutil.Process(pid)
                memory_mb = process.memory_info().rss / 1024 / 1024
                print(f"💾 Memory Usage: {memory_mb:.1f} MB")
                print(f"🔧 Process Status: {'Running' if process.is_running() else 'Not Running'}")
            except:
                print(f"🔧 Process PID: {pid} (may not be running)")

    def show_recent_logs(self, lines: int = 10):
        """Show recent log entries"""
        print(f"\n📋 Recent Log Entries (last {lines} lines)")
        print("=" * 40)

        if not self.logs_dir.exists():
            print("❌ No logs directory found")
            return

        # Find the latest log file
        log_files = list(self.logs_dir.glob("udemy_agent_*.log"))
        if not log_files:
            print("❌ No log files found")
            return

        latest_log = max(log_files, key=lambda f: f.stat().st_mtime)

        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]

                for line in recent_lines:
                    print(line.rstrip())
        except Exception as e:
            print(f"❌ Error reading log file: {e}")

    def show_seen_courses(self):
        """Show statistics about seen courses"""
        print("
📚 Seen Courses Statistics"        print("=" * 40)

        if not self.seen_courses_file.exists():
            print("❌ No seen courses file found")
            return

        try:
            with open(self.seen_courses_file, 'r') as f:
                data = json.load(f)

            seen_courses = data.get('seen_courses', {})
            print(f"📊 Total Courses Tracked: {len(seen_courses)}")
    
            if seen_courses:
                # Most recently seen courses
                recent_courses = sorted(
                    seen_courses.items(),
                    key=lambda x: x[1].get('last_seen', ''),
                    reverse=True
                )[:5]
    
                print("
    🕒 Recently Seen Courses:"            for course_id, metadata in recent_courses:
                    title = metadata.get('title', 'Unknown')[:50]
                    last_seen = metadata.get('last_seen', 'Unknown')
                    seen_count = metadata.get('seen_count', 0)
                    print(f"  • {title}... (seen {seen_count}x, last: {last_seen[:19]})")

        except Exception as e:
            print(f"❌ Error reading seen courses: {e}")

    def send_test_email(self):
        """Send a test email to verify email functionality"""
        print("
📧 Sending Test Email..."        print("=" * 40)

        try:
            msg = MIMEMultipart()
            msg['From'] = SMTP_USERNAME
            msg['To'] = EMAIL_RECIPIENT
            msg['Subject'] = "Udemy Agent - Test Email"

            body = f"""
            This is a test email from your Udemy Agent monitoring script.

            Sent at: {datetime.now()}

            Your Udemy agent is working correctly and can send notifications!

            Agent Health Status: {self.get_health_status() or 'Unknown'}
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(SMTP_USERNAME, EMAIL_RECIPIENT, text)
            server.quit()

            print("✅ Test email sent successfully!")
            print(f"📧 Check your inbox at: {EMAIL_RECIPIENT}")

        except Exception as e:
            print(f"❌ Failed to send test email: {e}")

    def cleanup_old_data(self, days: int = 30):
        """Clean up old log files and data"""
        print(f"\n🧹 Cleaning up data older than {days} days...")
        print("=" * 40)

        cleaned_files = 0
        freed_space = 0

        # Clean old log files
        if self.logs_dir.exists():
            cutoff_date = datetime.now() - timedelta(days=days)

            for log_file in self.logs_dir.glob("*.log"):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    file_size = log_file.stat().st_size
                    freed_space += file_size
                    log_file.unlink()
                    cleaned_files += 1
                    print(f"🗑️  Deleted: {log_file.name}")

        # Clean old seen courses (this is already handled by the agent)
        print(f"📊 Cleaned up {cleaned_files} old log files")
        print(f"💾 Freed approximately {freed_space / 1024 / 1024:.1f} MB")

    def restart_agent(self):
        """Restart the agent if it's running"""
        print("
🔄 Restarting Agent..."        print("=" * 40)

        health = self.get_health_status()
        if not health:
            print("❌ Agent health status not found. Agent may not be running.")
            return

        pid = health.get('pid')
        if pid:
            try:
                process = psutil.Process(pid)
                if process.is_running():
                    print(f"🛑 Stopping agent process (PID: {pid})...")
                    process.terminate()
                    process.wait(timeout=10)
                    print("✅ Agent stopped successfully")
                else:
                    print("📋 Agent process was not running")
            except Exception as e:
                print(f"⚠️  Could not stop agent process: {e}")

        print("🚀 Starting new agent instance...")
        print("💡 Run: python udemy_agent_production.py")
        print("   Or: .\start_udemy_agent.bat")

def show_help():
    """Show help information"""
    print("Udemy Agent Monitor & Management Tool")
    print("=" * 50)
    print()
    print("Usage: python monitor_agent.py [command]")
    print()
    print("Commands:")
    print("  status          Show agent health status")
    print("  logs [n]        Show last n log entries (default: 10)")
    print("  courses         Show seen courses statistics")
    print("  test-email      Send test email")
    print("  cleanup [days]  Clean old data (default: 30 days)")
    print("  restart         Restart agent if running")
    print("  help            Show this help")
    print()
    print("Examples:")
    print("  python monitor_agent.py status")
    print("  python monitor_agent.py logs 20")
    print("  python monitor_agent.py cleanup 7")
    print()

def main():
    """Main function"""
    monitor = AgentMonitor()

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == 'status':
        monitor.show_status()

    elif command == 'logs':
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        monitor.show_recent_logs(lines)

    elif command == 'courses':
        monitor.show_seen_courses()

    elif command == 'test-email':
        monitor.send_test_email()

    elif command == 'cleanup':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        monitor.cleanup_old_data(days)

    elif command == 'restart':
        monitor.restart_agent()

    elif command == 'help':
        show_help()

    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
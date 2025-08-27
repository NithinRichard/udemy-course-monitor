#!/usr/bin/env python3
"""
Udemy Agent Background Daemon

A simple background service for running the Udemy agent continuously.
This doesn't require pywin32 and works on any platform.

Usage:
    python udemy_daemon.py start     # Start in background
    python udemy_daemon.py stop      # Stop background process
    python udemy_daemon.py status    # Check status
    python udemy_daemon.py logs      # Show recent logs
"""

import sys
import os
import signal
import time
import json
import subprocess
import psutil
from pathlib import Path
from datetime import datetime
from udemy_agent_production import ProductionUdemyAgent

class UdemyDaemon:
    """Simple background daemon for Udemy agent"""

    def __init__(self):
        self.pid_file = Path("udemy_daemon.pid")
        self.log_file = Path("logs/daemon.log")
        self.log_file.parent.mkdir(exist_ok=True)

    def log(self, message):
        """Log message to daemon log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')

        print(log_entry)

    def start(self):
        """Start the daemon"""
        if self.is_running():
            print("Daemon is already running!")
            return

        self.log("Starting Udemy Agent Daemon...")

        try:
            # Start the agent in background
            process = subprocess.Popen(
                [sys.executable, "udemy_agent_production.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=os.getcwd()
            )

            # Save PID
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))

            self.log(f"Daemon started with PID: {process.pid}")
            print(f"Daemon started successfully (PID: {process.pid})")
            print("Use 'python udemy_daemon.py status' to check status")
            print("Use 'python udemy_daemon.py stop' to stop")

        except Exception as e:
            self.log(f"Failed to start daemon: {e}")
            print(f"Failed to start daemon: {e}")

    def stop(self):
        """Stop the daemon"""
        if not self.is_running():
            print("Daemon is not running!")
            return

        try:
            pid = self.get_pid()
            process = psutil.Process(pid)

            # Terminate the process
            process.terminate()
            process.wait(timeout=10)

            # Clean up PID file
            if self.pid_file.exists():
                self.pid_file.unlink()

            self.log("Daemon stopped successfully")
            print("Daemon stopped successfully")

        except Exception as e:
            self.log(f"Error stopping daemon: {e}")
            print(f"Error stopping daemon: {e}")

    def status(self):
        """Check daemon status"""
        if not self.is_running():
            print("Daemon Status: STOPPED")
            return

        pid = self.get_pid()
        try:
            process = psutil.Process(pid)
            memory_mb = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent()

            print("Daemon Status: RUNNING")
            print(f"PID: {pid}")
            print(".1f")
            print(".1f")

            # Check agent health
            health_file = Path("logs/health_status.json")
            if health_file.exists():
                try:
                    with open(health_file, 'r') as f:
                        health = json.load(f)

                    print(f"Agent Status: {health.get('status', 'unknown').upper()}")
                    print(f"Courses Found: {health.get('courses_found', 0)}")
                    print(f"Emails Sent: {health.get('emails_sent', 0)}")

                except:
                    print("Agent Health: Unable to read health file")

        except Exception as e:
            print(f"Daemon Status: ERROR - {e}")

    def is_running(self) -> bool:
        """Check if daemon is running"""
        if not self.pid_file.exists():
            return False

        try:
            pid = self.get_pid()
            process = psutil.Process(pid)
            return process.is_running()
        except:
            # PID file exists but process is not running
            if self.pid_file.exists():
                self.pid_file.unlink()
            return False

    def get_pid(self) -> int:
        """Get daemon PID from file"""
        if not self.pid_file.exists():
            return None

        with open(self.pid_file, 'r') as f:
            return int(f.read().strip())

    def show_logs(self, lines: int = 20):
        """Show recent daemon logs"""
        if not self.log_file.exists():
            print("No daemon logs found")
            return

        try:
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]

            print(f"Recent Daemon Logs (last {len(recent_lines)} lines):")
            print("-" * 50)
            for line in recent_lines:
                print(line.rstrip())

        except Exception as e:
            print(f"Error reading logs: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Udemy Agent Daemon")
        print("==================")
        print()
        print("Usage: python udemy_daemon.py <command>")
        print()
        print("Commands:")
        print("  start     Start daemon in background")
        print("  stop      Stop daemon")
        print("  status    Check daemon status")
        print("  logs      Show recent logs")
        print("  restart   Restart daemon")
        print()
        return

    command = sys.argv[1].lower()
    daemon = UdemyDaemon()

    if command == "start":
        daemon.start()
    elif command == "stop":
        daemon.stop()
    elif command == "status":
        daemon.status()
    elif command == "logs":
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        daemon.show_logs(lines)
    elif command == "restart":
        print("Restarting daemon...")
        daemon.stop()
        time.sleep(2)
        daemon.start()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
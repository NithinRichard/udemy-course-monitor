#!/usr/bin/env python3
"""
Production-ready Udemy Free Course Monitor Agent

Features:
- Robust error handling and recovery
- Health monitoring and self-healing
- Background service capabilities
- Enhanced logging and monitoring
- Automatic restart on failures
- Graceful shutdown handling
"""

import json
import logging
import time
import signal
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path
import psutil
from typing import Dict, List, Optional
from selenium_scraper import SeleniumUdemyScraper
from email_notifier import EmailNotifier
from config import (
    SEEN_COURSES_FILE, CHECK_INTERVAL_HOURS, EMAIL_RECIPIENT,
    SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT
)

class ProductionUdemyAgent:
    """Production-ready Udemy agent with monitoring and recovery"""

    def __init__(self):
        # Setup production logging first
        self._setup_production_logging()

        self.scraper = None
        self.notifier = EmailNotifier()
        self.seen_courses = self._load_seen_courses()
        self.is_running = False
        self.last_successful_check = None
        self.consecutive_failures = 0
        self.max_consecutive_failures = 5
        self.health_check_interval = 300  # 5 minutes
        self.restart_on_failure = True

        # Health monitoring
        self.health_status = {
            'status': 'starting',
            'last_check': None,
            'courses_found': 0,
            'emails_sent': 0,
            'errors': 0,
            'start_time': datetime.now(),
            'pid': psutil.Process().pid
        }

        # Graceful shutdown handling
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _setup_production_logging(self):
        """Setup comprehensive logging for production"""

        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger('UdemyAgent')
        self.logger.setLevel(logging.INFO)

        # Remove any existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # File handler with rotation
        log_file = log_dir / f'udemy_agent_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info("Production Udemy Agent initialized")

    def _load_seen_courses(self) -> Dict[str, dict]:
        """Load previously seen courses with metadata"""
        try:
            if Path(SEEN_COURSES_FILE).exists():
                with open(SEEN_COURSES_FILE, 'r') as f:
                    data = json.load(f)
                    seen_courses = data.get('seen_courses', {})

                    # Validate that seen_courses is a dictionary
                    if isinstance(seen_courses, dict):
                        return seen_courses
                    else:
                        self.logger.warning(f"seen_courses is not a dict ({type(seen_courses)}), resetting")
                        return {}
            return {}
        except Exception as e:
            self.logger.error(f"Error loading seen courses: {e}")
            # Backup corrupted file
            if Path(SEEN_COURSES_FILE).exists():
                backup_file = f"{SEEN_COURSES_FILE}.backup"
                import shutil
                shutil.copy(SEEN_COURSES_FILE, backup_file)
                self.logger.info(f"Backed up corrupted file to {backup_file}")
            return {}

    def _save_seen_courses(self, course_ids: Dict[str, dict]):
        """Save seen course IDs with metadata"""
        try:
            data = {
                'seen_courses': course_ids,
                'last_updated': datetime.now().isoformat(),
                'total_courses': len(course_ids)
            }
            with open(SEEN_COURSES_FILE, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            self.logger.info(f"Saved {len(course_ids)} seen courses")
        except Exception as e:
            self.logger.error(f"Error saving seen courses: {e}")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()

    def check_for_new_courses(self) -> bool:
        """Main method to check for new courses with error handling"""
        try:
            self.logger.info("Starting course check...")
            self.health_status['last_check'] = datetime.now()

            # Initialize scraper if needed
            if self.scraper is None:
                self.logger.info("Initializing Selenium scraper...")
                self.scraper = SeleniumUdemyScraper(headless=True)

            # Fetch current free courses
            courses = self.scraper.get_free_programming_courses()

            if courses is None:
                self.logger.warning("Scraper returned None, treating as error")
                courses = []

            self.logger.info(f"Found {len(courses)} free programming courses")
            self.health_status['courses_found'] += len(courses)

            # Find new courses
            new_courses = []
            current_course_ids = {}

            for course in courses:
                course_id = course['id']

                # Safely get existing course data
                existing_course_data = self.seen_courses.get(course_id, {})
                if not isinstance(existing_course_data, dict):
                    self.logger.warning(f"Course {course_id} has invalid data format, resetting")
                    existing_course_data = {}

                current_course_ids[course_id] = {
                    'title': course['title'],
                    'url': course['url'],
                    'first_seen': existing_course_data.get('first_seen', datetime.now().isoformat()),
                    'last_seen': datetime.now().isoformat(),
                    'seen_count': existing_course_data.get('seen_count', 0) + 1
                }

                if course_id not in self.seen_courses:
                    new_courses.append(course)
                    current_course_ids[course_id]['first_seen'] = datetime.now().isoformat()
                    self.logger.info(f"New course found: {course['title'][:50]}...")

            # Send notification if new courses found
            if new_courses:
                self.logger.info(f"Sending notification for {len(new_courses)} new courses")
                success = self.notifier.send_notification(new_courses)

                if success:
                    self.health_status['emails_sent'] += 1
                    self.logger.info("Notification sent successfully")

                    # Update seen courses only if notification was successful
                    for course in new_courses:
                        course_id = course['id']
                        if course_id in current_course_ids:
                            self.seen_courses[course_id] = current_course_ids[course_id]

                    self._save_seen_courses(self.seen_courses)
                    self.logger.info("Seen courses updated")

                    # Reset consecutive failures on success
                    self.consecutive_failures = 0
                else:
                    self.logger.error("Failed to send notification")
                    self.consecutive_failures += 1
                    self.health_status['errors'] += 1
            else:
                self.logger.info("No new courses found")

            # Update seen courses for existing ones
            for course_id, metadata in current_course_ids.items():
                if course_id in self.seen_courses:
                    self.seen_courses[course_id] = metadata

            self._save_seen_courses(self.seen_courses)

            # Clean up old courses (older than 30 days)
            self._cleanup_old_courses()

            # Update health status
            self.health_status['status'] = 'healthy'
            self.last_successful_check = datetime.now()

            return True

        except Exception as e:
            self.logger.error(f"Error during course check: {e}")
            self.consecutive_failures += 1
            self.health_status['errors'] += 1
            self.health_status['status'] = 'error'

            # Check if we should restart
            if self.restart_on_failure and self.consecutive_failures >= self.max_consecutive_failures:
                self.logger.error(f"Too many consecutive failures ({self.consecutive_failures}), restarting scraper...")
                self._restart_scraper()

            return False

    def _restart_scraper(self):
        """Restart the scraper instance"""
        try:
            if self.scraper:
                self.scraper.driver.quit()
                self.scraper = None

            self.scraper = SeleniumUdemyScraper(headless=True)
            self.logger.info("Scraper restarted successfully")
            self.consecutive_failures = 0
        except Exception as e:
            self.logger.error(f"Failed to restart scraper: {e}")

    def _cleanup_old_courses(self):
        """Remove courses that haven't been seen for 30 days"""
        try:
            if not isinstance(self.seen_courses, dict):
                self.logger.warning(f"seen_courses is not a dict: {type(self.seen_courses)}")
                return

            cutoff_date = datetime.now() - timedelta(days=30)
            original_count = len(self.seen_courses)

            courses_to_remove = []
            for course_id, metadata in self.seen_courses.items():
                if isinstance(metadata, dict):
                    last_seen = metadata.get('last_seen')
                    if last_seen:
                        try:
                            last_seen_date = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                            if last_seen_date < cutoff_date:
                                courses_to_remove.append(course_id)
                        except:
                            # If we can't parse the date, keep the course
                            pass

            for course_id in courses_to_remove:
                del self.seen_courses[course_id]

            if courses_to_remove:
                self.logger.info(f"Cleaned up {len(courses_to_remove)} old courses")
                self._save_seen_courses(self.seen_courses)

        except Exception as e:
            self.logger.warning(f"Error during cleanup: {e}")
            # Reinitialize seen_courses if it's corrupted
            if not isinstance(self.seen_courses, dict):
                self.logger.info("Reinitializing seen_courses")
                self.seen_courses = {}
                self._save_seen_courses(self.seen_courses)

    def _health_monitor(self):
        """Monitor agent health and perform periodic checks"""
        while self.is_running:
            try:
                # Check if last successful check is too old
                if self.last_successful_check:
                    time_since_last_check = datetime.now() - self.last_successful_check
                    if time_since_last_check.total_seconds() > (CHECK_INTERVAL_HOURS * 3600 * 1.5):
                        self.logger.warning(f"No successful check for {time_since_last_check}, health check triggered")
                        self.health_status['status'] = 'degraded'

                        # Try a health check
                        if self.scraper and hasattr(self.scraper, 'driver'):
                            try:
                                # Simple health check - try to get page title
                                title = self.scraper.driver.title
                                self.logger.info(f"Health check passed, page title: {title}")
                                self.health_status['status'] = 'healthy'
                            except:
                                self.logger.error("Health check failed, restarting scraper")
                                self._restart_scraper()

                # Log health status periodically
                self.logger.info(f"Health Status: {self.health_status['status']} | "
                               f"Courses: {self.health_status['courses_found']} | "
                               f"Emails: {self.health_status['emails_sent']} | "
                               f"Errors: {self.health_status['errors']}")

                # Save health status to file
                self._save_health_status()

            except Exception as e:
                self.logger.error(f"Error in health monitor: {e}")

            time.sleep(self.health_check_interval)

    def _save_health_status(self):
        """Save health status to file for monitoring"""
        try:
            health_file = Path('logs/health_status.json')
            health_file.parent.mkdir(exist_ok=True)

            with open(health_file, 'w') as f:
                json.dump(self.health_status, f, indent=2, default=str)
        except Exception as e:
            self.logger.warning(f"Could not save health status: {e}")

    def run_once(self) -> bool:
        """Run a single check (useful for testing)"""
        self.logger.info("Running single check...")
        success = self.check_for_new_courses()
        if success:
            self.logger.info("Single check completed successfully")
        else:
            self.logger.error("Single check failed")
        return success

    def run_scheduler(self):
        """Run the agent with daily scheduling"""
        self.logger.info(f"Starting Udemy agent with {CHECK_INTERVAL_HOURS} hour intervals")
        self.is_running = True

        # Start health monitoring thread
        health_thread = threading.Thread(target=self._health_monitor, daemon=True)
        health_thread.start()

        # Run immediately on start
        self.check_for_new_courses()

        try:
            while self.is_running:
                # Calculate next run time
                next_run = datetime.now() + timedelta(hours=CHECK_INTERVAL_HOURS)
                self.logger.info(f"Next check scheduled for: {next_run}")

                # Sleep until next check (with periodic health checks)
                sleep_time = CHECK_INTERVAL_HOURS * 3600
                slept = 0

                while slept < sleep_time and self.is_running:
                    time.sleep(min(60, sleep_time - slept))  # Sleep in 1-minute increments
                    slept += 60

                    # Check if we should stop
                    if not self.is_running:
                        break

                if self.is_running:
                    self.check_for_new_courses()

        except KeyboardInterrupt:
            self.logger.info("Agent stopped by user")
        except Exception as e:
            self.logger.error(f"Agent encountered error: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop the agent gracefully"""
        self.logger.info("Stopping Udemy agent...")
        self.is_running = False
        self.health_status['status'] = 'stopped'

        # Cleanup
        if self.scraper:
            try:
                self.scraper.driver.quit()
            except:
                pass

        self._save_health_status()
        self.logger.info("Udemy agent stopped")

    def get_health_status(self) -> Dict:
        """Get current health status"""
        return self.health_status.copy()

def send_startup_notification():
    """Send a startup notification email"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = "Udemy Agent Started Successfully"

        body = f"""
        Your Udemy Free Course Monitor Agent has started successfully!

        Started at: {datetime.now()}
        Email recipient: {EMAIL_RECIPIENT}
        Check interval: {CHECK_INTERVAL_HOURS} hours

        The agent will now monitor Udemy for free programming courses and send you notifications when new courses become available.

        To stop the agent, press Ctrl+C in the terminal or send a SIGTERM signal.
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, EMAIL_RECIPIENT, text)
        server.quit()

        print("SUCCESS: Startup notification sent!")

    except Exception as e:
        print(f"WARNING: Could not send startup notification: {e}")

def main():
    """Main entry point"""
    agent = ProductionUdemyAgent()

    # Send startup notification
    send_startup_notification()

    # For testing, run once first
    print("Running initial test check...")
    agent.run_once()

    # Then ask if they want to run continuously
    response = input("\nTest completed. Start production monitoring? (y/n): ")
    if response.lower() == 'y':
        agent.run_scheduler()
    else:
        print("Agent stopped. You can run it again anytime.")
        agent.stop()

if __name__ == "__main__":
    main()
import json
import logging
import time
import schedule
from datetime import datetime
from typing import Set
from selenium_scraper import SeleniumUdemyScraper
from email_notifier import EmailNotifier
from config import SEEN_COURSES_FILE, CHECK_INTERVAL_HOURS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('udemy_agent.log'),
        logging.StreamHandler()
    ]
)

class UdemyAgent:
    def __init__(self):
        self.scraper = SeleniumUdemyScraper(headless=True)  # Run headless for background operation
        self.notifier = EmailNotifier()
        self.seen_courses = self._load_seen_courses()

    def _load_seen_courses(self) -> Set[str]:
        """Load previously seen course IDs"""
        try:
            with open(SEEN_COURSES_FILE, 'r') as f:
                data = json.load(f)
                return set(data.get('seen_courses', []))
        except FileNotFoundError:
            logging.info("No seen courses file found, starting fresh")
            return set()
        except Exception as e:
            logging.error(f"Error loading seen courses: {e}")
            return set()

    def _save_seen_courses(self, course_ids: Set[str]):
        """Save seen course IDs to file"""
        try:
            data = {
                'seen_courses': list(course_ids),
                'last_updated': datetime.now().isoformat()
            }
            with open(SEEN_COURSES_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving seen courses: {e}")

    def check_for_new_courses(self):
        """Main method to check for new courses and send notifications"""
        logging.info("Starting course check...")

        try:
            # Fetch current free courses
            courses = self.scraper.get_free_programming_courses()
            logging.info(f"Found {len(courses)} free programming courses")

            # Find new courses
            new_courses = []
            current_course_ids = set()

            for course in courses:
                course_id = course['id']
                current_course_ids.add(course_id)

                if course_id not in self.seen_courses:
                    new_courses.append(course)
                    logging.info(f"New course found: {course['title']}")

            # Send notification if new courses found
            if new_courses:
                logging.info(f"Sending notification for {len(new_courses)} new courses")
                success = self.notifier.send_notification(new_courses)

                if success:
                    # Update seen courses only if notification was successful
                    self.seen_courses.update(course_id for course in new_courses)
                    self._save_seen_courses(self.seen_courses)
                    logging.info("Seen courses updated")
                else:
                    logging.error("Failed to send notification, not updating seen courses")
            else:
                logging.info("No new courses found")

            # Clean up seen courses that are no longer free
            # This prevents the list from growing indefinitely
            self.seen_courses = self.seen_courses.intersection(current_course_ids)
            self._save_seen_courses(self.seen_courses)

        except Exception as e:
            logging.error(f"Error during course check: {e}")

    def run_once(self):
        """Run a single check (useful for testing)"""
        self.check_for_new_courses()

    def run_scheduler(self):
        """Run the agent with daily scheduling"""
        logging.info(f"Starting Udemy agent with {CHECK_INTERVAL_HOURS} hour intervals")

        # Run immediately on start
        self.check_for_new_courses()

        # Schedule daily runs
        schedule.every(CHECK_INTERVAL_HOURS).hours.do(self.check_for_new_courses)

        logging.info("Agent is running. Press Ctrl+C to stop.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
        except KeyboardInterrupt:
            logging.info("Agent stopped by user")
        except Exception as e:
            logging.error(f"Agent encountered error: {e}")

def main():
    agent = UdemyAgent()

    # For testing, run once first
    print("Running initial test check...")
    agent.run_once()

    # Then ask if they want to run continuously
    response = input("\nTest completed. Start daily monitoring? (y/n): ")
    if response.lower() == 'y':
        agent.run_scheduler()
    else:
        print("Agent stopped. You can run it again anytime.")

if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
EMAIL_RECIPIENT = "nithinrichard1@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Your Gmail address
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # App password or regular password

# Udemy configuration
UDEMY_FREE_URL = "https://www.udemy.com/courses/free/"
PROGRAMMING_CATEGORY = "?category=Development"

# Agent configuration
CHECK_INTERVAL_HOURS = 24  # Daily
NOTIFICATION_SUBJECT = "New Free Programming Course Available on Udemy!"

# Data storage
SEEN_COURSES_FILE = "seen_courses.json"
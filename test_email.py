#!/usr/bin/env python3
"""
Test script to verify email functionality
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import EMAIL_RECIPIENT, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_email():
    """Test email sending functionality"""
    print("=== Testing Email Functionality ===\n")

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = "Test Email from Udemy Agent"

        # Create simple test body
        body = """
        This is a test email from your Udemy Free Course Monitor Agent.

        If you receive this email, the email configuration is working correctly!

        The agent will send you notifications when new free programming courses become available on Udemy.
        """
        msg.attach(MIMEText(body, 'plain'))

        print(f"Attempting to send test email...")
        print(f"From: {SMTP_USERNAME}")
        print(f"To: {EMAIL_RECIPIENT}")
        print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

        print("Logging in...")
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        print("Sending email...")
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, EMAIL_RECIPIENT, text)
        server.quit()

        print("✅ SUCCESS! Test email sent successfully!")
        print("Check your inbox for the test message.")

    except Exception as e:
        print(f"❌ FAILED! Error: {e}")

        if "535" in str(e):
            print("\n🔧 Gmail Authentication Issue:")
            print("This usually means:")
            print("1. The App Password is incorrect")
            print("2. The App Password was revoked")
            print("3. 2-Step Verification is not enabled")
            print("4. The app password is not for 'Mail'")
            print("\n📝 To fix:")
            print("1. Go to https://myaccount.google.com/security")
            print("2. Enable 2-Step Verification")
            print("3. Go to https://myaccount.google.com/apppasswords")
            print("4. Generate a new App Password for 'Mail'")
            print("5. Update the SMTP_PASSWORD in .env file")
            print("6. Make sure it's exactly 16 characters (no spaces)")

        return False

    return True

if __name__ == "__main__":
    success = test_email()

    if success:
        print("\n🎉 Email is working! Your Udemy agent will be able to send notifications.")
    else:
        print("\n⚠️  Email is not working. Please fix the Gmail App Password configuration.")
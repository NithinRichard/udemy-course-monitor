import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import List, Dict
from config import EMAIL_RECIPIENT, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

class EmailNotifier:
    def __init__(self):
        self.recipient = EMAIL_RECIPIENT
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = SMTP_USERNAME
        self.password = SMTP_PASSWORD

    def send_notification(self, new_courses: List[Dict]) -> bool:
        """
        Send email notification about new free courses
        """
        if not new_courses:
            logging.info("No new courses to notify about")
            return True

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = self.recipient
            msg['Subject'] = "New Free Programming Courses Available on Udemy!"

            # Create HTML body
            html_body = self._create_email_body(new_courses)
            msg.attach(MIMEText(html_body, 'html'))

            # Send email
            logging.info(f"Sending email notification to {self.recipient}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, self.recipient, text)
            server.quit()

            logging.info(f"Successfully sent notification about {len(new_courses)} new courses")
            return True

        except Exception as e:
            logging.error(f"Failed to send email notification: {e}")
            return False

    def _create_email_body(self, courses: List[Dict]) -> str:
        """
        Create HTML email body with course information
        """
        html = f"""
        <html>
        <body>
            <h2>New Free Programming Courses Available!</h2>
            <p>I've found {len(courses)} new free programming course(s) on Udemy:</p>

            <div style="margin: 20px 0;">
        """

        for course in courses:
            html += f"""
                <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <h3><a href="{course['url']}" style="color: #007bff; text-decoration: none;">{course['title']}</a></h3>
                    <p><strong>Instructor:</strong> {course['instructor']}</p>
                    <p><strong>Rating:</strong> {course['rating']}</p>
                    <p><strong>Students:</strong> {course['students']}</p>
                    <p><a href="{course['url']}" style="background-color: #007bff; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px;">Enroll Now</a></p>
                </div>
            """

        html += """
            </div>

            <p>This email was sent by your Udemy Free Course Monitor Agent.</p>
            <p>To stop receiving these notifications, simply stop the agent.</p>
        </body>
        </html>
        """

        return html
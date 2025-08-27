import requests
from bs4 import BeautifulSoup
import json
import logging
from typing import List, Dict
import time

class UdemyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_free_programming_courses(self) -> List[Dict]:
        """
        Scrape free programming courses from Udemy
        """
        url = "https://www.udemy.com/courses/free/?category=Development"

        try:
            logging.info(f"Fetching courses from: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            courses = []
            course_cards = soup.find_all('div', class_='course-card')

            logging.info(f"Found {len(course_cards)} course cards")

            for card in course_cards[:10]:  # Limit to first 10 for testing
                course_data = self._extract_course_data(card)
                if course_data:
                    courses.append(course_data)

            return courses

        except Exception as e:
            logging.error(f"Error fetching courses: {e}")
            return []

    def _extract_course_data(self, card) -> Dict:
        """
        Extract course information from a course card
        """
        try:
            # Course title
            title_elem = card.find('h3', class_='course-card__title')
            title = title_elem.text.strip() if title_elem else "Unknown Title"

            # Course URL
            link_elem = card.find('a', class_='course-card__link')
            url = "https://www.udemy.com" + link_elem['href'] if link_elem and link_elem.get('href') else ""

            # Instructor
            instructor_elem = card.find('div', class_='course-card__instructor')
            instructor = instructor_elem.text.strip() if instructor_elem else "Unknown Instructor"

            # Rating
            rating_elem = card.find('span', class_='course-card__rating')
            rating = rating_elem.text.strip() if rating_elem else "No rating"

            # Students count
            students_elem = card.find('span', class_='course-card__students')
            students = students_elem.text.strip() if students_elem else "0 students"

            # Course ID (for tracking)
            course_id = url.split('/')[-2] if url else title.lower().replace(' ', '_')

            return {
                'id': course_id,
                'title': title,
                'url': url,
                'instructor': instructor,
                'rating': rating,
                'students': students,
                'discovered_at': time.time()
            }

        except Exception as e:
            logging.error(f"Error extracting course data: {e}")
            return None
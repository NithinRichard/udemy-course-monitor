#!/usr/bin/env python3
"""
Alternative approaches to get Udemy free courses since direct scraping is blocked
"""

import requests
import json
import logging
from typing import List, Dict
import time

class AlternativeUdemyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        })

    def try_udemy_api(self) -> List[Dict]:
        """
        Try to access Udemy's API endpoints
        """
        print("Trying Udemy API endpoints...")

        # Common API endpoints that might work
        api_endpoints = [
            "https://www.udemy.com/api-2.0/courses/?price=free&category=Development",
            "https://www.udemy.com/api-2.0/courses/?price=price-free&category=Development",
            "https://www.udemy.com/api-2.0/courses/?is_paid=false&category=Development",
            "https://www.udemy.com/api-2.0/courses/?price=free",
        ]

        for url in api_endpoints:
            try:
                print(f"Trying API endpoint: {url}")
                time.sleep(3)  # Be respectful
                response = self.session.get(url, timeout=30)

                if response.status_code == 200:
                    print(f"Success! API endpoint works: {url}")
                    data = response.json()
                    return self._parse_api_response(data)
                else:
                    print(f"API endpoint failed with status: {response.status_code}")

            except Exception as e:
                print(f"API endpoint error: {e}")

        return []

    def try_rss_feeds(self) -> List[Dict]:
        """
        Try to find RSS feeds for Udemy courses
        """
        print("Checking for RSS feeds...")

        rss_urls = [
            "https://www.udemy.com/rss/free-courses/",
            "https://www.udemy.com/rss/courses/",
            "https://www.udemy.com/courses/free/rss/",
        ]

        for url in rss_urls:
            try:
                print(f"Trying RSS feed: {url}")
                time.sleep(2)
                response = self.session.get(url, timeout=30)

                if response.status_code == 200:
                    print(f"Success! RSS feed found: {url}")
                    return self._parse_rss_response(response.content)
                else:
                    print(f"RSS feed failed with status: {response.status_code}")

            except Exception as e:
                print(f"RSS feed error: {e}")

        return []

    def try_alternative_sources(self) -> List[Dict]:
        """
        Try alternative websites that aggregate Udemy free courses
        """
        print("Checking alternative data sources...")

        # Websites that often aggregate free Udemy courses
        sources = [
            {
                'name': 'FreeCodeCamp Udemy Courses',
                'url': 'https://www.freecodecamp.org/news/free-udemy-courses/',
                'method': 'html'
            },
            {
                'name': 'Tutorialspoint Free Courses',
                'url': 'https://www.tutorialspoint.com/free_courses.htm',
                'method': 'html'
            }
        ]

        all_courses = []

        for source in sources:
            try:
                print(f"Trying alternative source: {source['name']}")
                time.sleep(3)

                if source['method'] == 'html':
                    courses = self._scrape_alternative_source(source['url'])
                    all_courses.extend(courses)

            except Exception as e:
                print(f"Alternative source error for {source['name']}: {e}")

        return all_courses

    def _parse_api_response(self, data) -> List[Dict]:
        """Parse Udemy API response"""
        courses = []

        if 'results' in data:
            for course in data['results']:
                courses.append({
                    'id': str(course.get('id', '')),
                    'title': course.get('title', 'Unknown Title'),
                    'url': f"https://www.udemy.com{course.get('url', '')}",
                    'instructor': course.get('visible_instructors', [{}])[0].get('display_name', 'Unknown'),
                    'rating': str(course.get('avg_rating_recent', 0)),
                    'students': f"{course.get('num_subscribers', 0)} students",
                    'discovered_at': time.time()
                })

        return courses[:10]  # Limit for testing

    def _parse_rss_response(self, content) -> List[Dict]:
        """Parse RSS feed response"""
        from bs4 import BeautifulSoup

        courses = []
        soup = BeautifulSoup(content, 'xml')

        items = soup.find_all('item')
        for item in items[:10]:  # Limit for testing
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')

            if title and link:
                courses.append({
                    'id': str(hash(link.text)),
                    'title': title.text,
                    'url': link.text,
                    'instructor': 'Unknown',
                    'rating': 'Unknown',
                    'students': 'Unknown',
                    'discovered_at': time.time()
                })

        return courses

    def _scrape_alternative_source(self, url) -> List[Dict]:
        """Scrape an alternative source for Udemy courses"""
        try:
            response = self.session.get(url, timeout=30)

            if 'freecodecamp' in url:
                return self._parse_freecodecamp(response.content)
            elif 'tutorialspoint' in url:
                return self._parse_tutorialspoint(response.content)

        except Exception as e:
            print(f"Error scraping alternative source: {e}")

        return []

    def _parse_freecodecamp(self, content) -> List[Dict]:
        """Parse FreeCodeCamp page for Udemy courses"""
        from bs4 import BeautifulSoup

        courses = []
        soup = BeautifulSoup(content, 'html.parser')

        # Look for Udemy course links
        udemy_links = soup.find_all('a', href=lambda href: href and 'udemy.com' in href)

        for link in udemy_links[:10]:  # Limit for testing
            courses.append({
                'id': str(hash(link['href'])),
                'title': link.get_text().strip(),
                'url': link['href'],
                'instructor': 'Unknown',
                'rating': 'Unknown',
                'students': 'Unknown',
                'discovered_at': time.time()
            })

        return courses

    def _parse_tutorialspoint(self, content) -> List[Dict]:
        """Parse Tutorialspoint page for free courses"""
        from bs4 import BeautifulSoup

        courses = []
        soup = BeautifulSoup(content, 'html.parser')

        # Look for course listings
        course_elements = soup.find_all(['h3', 'h4'], class_='tutorial')

        for element in course_elements[:10]:  # Limit for testing
            link = element.find('a')
            if link and 'udemy' in link.get('href', '').lower():
                courses.append({
                    'id': str(hash(link['href'])),
                    'title': element.get_text().strip(),
                    'url': link['href'],
                    'instructor': 'Unknown',
                    'rating': 'Unknown',
                    'students': 'Unknown',
                    'discovered_at': time.time()
                })

        return courses

    def get_free_programming_courses(self) -> List[Dict]:
        """
        Main method to get free programming courses using various methods
        """
        print("Attempting to find free programming courses...")

        # Try different methods in order of preference
        methods = [
            ("Udemy API", self.try_udemy_api),
            ("RSS Feeds", self.try_rss_feeds),
            ("Alternative Sources", self.try_alternative_sources),
        ]

        for method_name, method_func in methods:
            print(f"\n--- Trying {method_name} ---")
            courses = method_func()
            if courses:
                print(f"Success! Found {len(courses)} courses using {method_name}")
                return courses

        print("All methods failed. Udemy may have strong anti-bot protection.")
        return []

def test_alternative_methods():
    """Test all alternative methods"""
    scraper = AlternativeUdemyScraper()
    courses = scraper.get_free_programming_courses()

    if courses:
        print(f"\n=== Found {len(courses)} Courses ===")
        for i, course in enumerate(courses[:5], 1):
            print(f"{i}. {course['title']}")
            print(f"   URL: {course['url']}")
            print(f"   Instructor: {course['instructor']}")
            print()
    else:
        print("\nNo courses found with any method.")

if __name__ == "__main__":
    print("=== Alternative Udemy Scraper Test ===\n")
    test_alternative_methods()
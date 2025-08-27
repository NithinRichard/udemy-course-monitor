#!/usr/bin/env python3
"""
Test script for Selenium-based Udemy scraper
"""

import logging
from selenium_scraper import SeleniumUdemyScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_selenium_scraper():
    """Test the Selenium scraper"""
    print("=== Testing Selenium Udemy Scraper ===\n")

    # Test with headless=True for automated testing
    scraper = SeleniumUdemyScraper(headless=True)

    print("Starting scraper (browser will open)...")
    courses = scraper.get_free_programming_courses()

    if courses:
        print(f"\n=== SUCCESS! Found {len(courses)} courses ===")
        for i, course in enumerate(courses, 1):
            print(f"\n{i}. {course['title']}")
            print(f"   URL: {course['url']}")
            print(f"   Instructor: {course['instructor']}")
            print(f"   Rating: {course['rating']}")
            print(f"   Students: {course['students']}")
    else:
        print("\n=== No courses found ===")
        print("This could be due to:")
        print("1. Udemy blocking the browser")
        print("2. Page structure changes")
        print("3. Network issues")
        print("4. Chrome driver issues")

if __name__ == "__main__":
    test_selenium_scraper()
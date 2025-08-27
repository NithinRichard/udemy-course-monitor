#!/usr/bin/env python3
"""
Test script to verify Udemy scraper functionality
"""

import requests
from bs4 import BeautifulSoup
import json

def test_udemy_page():
    """Test basic connectivity to Udemy free courses page"""
    urls_to_try = [
        "https://www.udemy.com/courses/free/",
        "https://www.udemy.com/courses/free/?category=Development",
        "https://www.udemy.com/courses/free/?price=free"
    ]

    for url in urls_to_try:
        print(f"\n--- Testing URL: {url} ---")
        success = test_single_url(url)
        if success:
            return True
    return False

def test_single_url(url):
    """Test a single URL"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }

    try:
        print(f"Testing connection to: {url}")
        import time
        time.sleep(2)  # Be respectful with requests
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")

        soup = BeautifulSoup(response.content, 'lxml')

        # Try different selectors that might work
        selectors_to_try = [
            'div.course-card',
            'div[data-purpose="course-card"]',
            'a[href*="/course/"]',
            '.course-card__title',
            'h3'
        ]

        for selector in selectors_to_try:
            elements = soup.select(selector)
            print(f"Selector '{selector}': Found {len(elements)} elements")

            if len(elements) > 0:
                print(f"  Sample element: {elements[0].get_text()[:100] if elements[0].get_text() else 'No text'}")
                if len(elements) <= 3:  # Show details for small results
                    for i, elem in enumerate(elements[:3]):
                        print(f"    Element {i+1}: {elem.get_text()[:200] if elem.get_text() else 'No text'}")

        # Check if page is JavaScript rendered
        if 'course-card' not in response.text and 'course' in response.text.lower():
            print("\nWARNING: Page might be JavaScript rendered. Scraping may not work properly.")
            print("Consider using Selenium or similar for full functionality.")

        return True

    except Exception as e:
        print(f"Error testing Udemy page: {e}")
        return False

def analyze_page_structure():
    """Analyze the page structure for course information"""
    url = "https://www.udemy.com/courses/free/"

    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'lxml')

        # Look for course-related content
        print("\n=== PAGE STRUCTURE ANALYSIS ===")

        # Find all links that might be courses
        course_links = soup.find_all('a', href=lambda href: href and '/course/' in href)
        print(f"Found {len(course_links)} potential course links")

        if course_links:
            print("Sample course links:")
            for i, link in enumerate(course_links[:5]):
                print(f"  {i+1}. {link.get('href')} - {link.get_text()[:50]}")

        # Look for JSON-LD structured data
        json_scripts = soup.find_all('script', type='application/ld+json')
        print(f"\nFound {len(json_scripts)} JSON-LD scripts")

        for i, script in enumerate(json_scripts):
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    print(f"  JSON-LD {i+1}: Array with {len(data)} items")
                elif isinstance(data, dict) and data.get('@type') == 'Course':
                    print(f"  JSON-LD {i+1}: Course data found!")
                    print(f"    Title: {data.get('name', 'N/A')}")
            except:
                pass

    except Exception as e:
        print(f"Error analyzing page: {e}")

if __name__ == "__main__":
    print("=== Udemy Scraper Test ===\n")

    success = test_udemy_page()

    if success:
        analyze_page_structure()
        print("\n=== Test Complete ===")
        print("If you see course cards found above, the scraper should work!")
        print("Otherwise, Udemy may have changed their page structure.")
    else:
        print("Failed to connect to Udemy. Check your internet connection.")
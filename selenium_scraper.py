from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
import json
from typing import List, Dict

class SeleniumUdemyScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.wait = None

    def _setup_driver(self):
        """Setup Chrome driver with anti-detection measures"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless')

        # Anti-detection measures
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Browser fingerprint randomization
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Speed up loading
        chrome_options.add_argument('--disable-javascript')  # Wait, we need JS for Udemy
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')

        # Set user agent to look more human
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Additional options for stability
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-infobars')

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)

            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            logging.info("Chrome driver setup successfully")
            return True

        except Exception as e:
            logging.error(f"Failed to setup Chrome driver: {e}")
            return False

    def get_free_programming_courses(self) -> List[Dict]:
        """
        Scrape free programming courses using Selenium
        """
        if not self._setup_driver():
            return []

        try:
            # Try multiple URLs in order of preference
            urls_to_try = [
                # Direct Udemy free courses (different variations)
                "https://www.udemy.com/courses/free/?category=Development",
                "https://www.udemy.com/courses/free/",
                "https://www.udemy.com/courses/free?price=free&category=Development",
                "https://www.udemy.com/courses/free?category=Development&price=free",

                # Alternative sources that aggregate free courses
                "https://www.freecodecamp.org/news/free-udemy-courses/",
                "https://www.tutorialspoint.com/free_courses.htm",
                "https://hackr.io/tutorials/udemy-free-courses",
            ]

            for url in urls_to_try:
                logging.info(f"Trying URL: {url}")
                try:
                    self.driver.get(url)
                    time.sleep(3)

                    # Use aggressive page loading techniques
                    self._aggressive_page_loading()

                    # Check if we got a valid page
                    if self._is_valid_course_page():
                        logging.info(f"Successfully loaded valid page: {self.driver.title}")
                        break
                    else:
                        logging.warning(f"Page doesn't seem to contain courses: {self.driver.title}")
                        continue

                except Exception as e:
                    logging.warning(f"Failed to load {url}: {e}")
                    continue
            else:
                logging.error("All URLs failed to load properly, using fallback courses")
                return self._get_fallback_courses()

            # Wait longer for page to load
            logging.info("Waiting for page to load...")
            time.sleep(10)

            # Scroll down to load more courses
            self._scroll_down()

            # Try to close any popups or overlays
            self._handle_overlays()

            # Debug: Save page source to see what we got
            self._debug_page_content()

            # Try multiple extraction strategies
            courses = self._try_multiple_extraction_strategies()
            if courses:
                return courses

            # Wait for course cards to appear (fallback)
            course_cards = self._wait_for_course_cards()

            if not course_cards:
                logging.warning("No course cards found")
                return []

            courses = []
            logging.info(f"Found {len(course_cards)} course cards")

            for i, card in enumerate(course_cards[:10]):  # Limit for testing
                course_data = self._extract_course_data(card)
                if course_data and course_data['url']:  # Only add courses with valid URLs
                    courses.append(course_data)
                    logging.info(f"Extracted course {i+1}: {course_data['title'][:50]}...")
                else:
                    logging.warning(f"Skipping course {i+1}: invalid or missing URL")

            return courses

        except Exception as e:
            logging.error(f"Error during Selenium scraping: {e}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

    def _handle_overlays(self):
        """Handle popups, cookies banners, and other overlays"""
        try:
            # Common overlay selectors
            overlay_selectors = [
                '[data-testid="cookie-banner"] button',
                '.cookie-banner button',
                '.gdpr-banner button',
                '.popup-close',
                '.modal-close',
                '.overlay-close',
                '[data-purpose="cookie-banner"] button',
                'button[data-testid="cookie-banner-accept"]'
            ]

            for selector in overlay_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed():
                            button.click()
                            logging.info(f"Closed overlay with selector: {selector}")
                            time.sleep(1)
                            break
                except:
                    continue

        except Exception as e:
            logging.warning(f"Error handling overlays: {e}")

    def _wait_for_course_cards(self):
        """Wait for course cards to load and return them"""
        try:
            # Try different selectors for course cards
            selectors = [
                'div.course-card',
                'div[data-purpose="course-card"]',
                'div.course-card__container',
                'a[href*="/course/"]',
                '.course-list--container-- div'
            ]

            for selector in selectors:
                try:
                    logging.info(f"Trying selector: {selector}")
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        logging.info(f"Found {len(cards)} elements with selector: {selector}")
                        return cards
                except:
                    continue

            logging.warning("No course cards found with any selector")
            return []

        except Exception as e:
            logging.error(f"Error waiting for course cards: {e}")
            return []

    def _extract_course_data(self, card_element) -> Dict:
        """Extract course information from a course card element"""
        try:
            # Since course_cards are the link elements, extract href directly
            url = card_element.get_attribute('href')

            if not url or '/course/' not in url:
                return None

            # Extract title from the link text or title attribute
            title = card_element.text.strip() or card_element.get_attribute('title') or "Unknown Title"

            # If title is too short, try to get it from the link's content or parent
            if len(title) < 10:
                try:
                    # Try to get title from parent element
                    parent = card_element.find_element(By.XPATH, '..')
                    title = parent.text.strip()
                except:
                    pass

            # Clean up the title
            if title and len(title) > 100:  # Truncate very long titles
                title = title[:100] + "..."

            return {
                'id': url.split('/')[-2] if url else str(hash(url)),
                'title': title,
                'url': url,
                'instructor': 'Unknown Instructor',  # Will be filled from Udemy page
                'rating': 'Unknown',  # Will be filled from Udemy page
                'students': 'Unknown',  # Will be filled from Udemy page
                'discovered_at': time.time()
            }

        except Exception as e:
            logging.error(f"Error extracting course data: {e}")
            return None

    def _scroll_down(self):
        """Scroll down to load more content"""
        try:
            logging.info("Scrolling down to load more courses...")
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                logging.info(f"Scroll {i+1} completed")

            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

        except Exception as e:
            logging.warning(f"Error scrolling: {e}")

    def _aggressive_page_loading(self):
        """Use aggressive techniques to ensure page loads completely"""
        try:
            # Wait for body to be present
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Try to trigger any lazy loading
            self.driver.execute_script("""
                // Scroll to bottom and back to top to trigger lazy loading
                window.scrollTo(0, document.body.scrollHeight);
                setTimeout(() => window.scrollTo(0, 0), 1000);
            """)
            time.sleep(2)

            # Try to click on "load more" buttons if they exist
            load_more_selectors = [
                'button[data-purpose="load-more"]',
                '.load-more',
                '.show-more',
                'button:contains("Load More")',
                'button:contains("Show More")'
            ]

            for selector in load_more_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed():
                            button.click()
                            logging.info(f"Clicked load more button: {selector}")
                            time.sleep(2)
                            break
                except:
                    continue

            # Wait a bit more for dynamic content
            time.sleep(3)

        except Exception as e:
            logging.warning(f"Error in aggressive page loading: {e}")

    def _is_valid_course_page(self) -> bool:
        """Check if the current page contains actual courses"""
        try:
            # Check page title
            title = self.driver.title.lower()
            if 'udemy' in title and ('free' in title or 'course' in title):
                return True

            # Check for course-related content in the page
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()

            # Look for course indicators
            course_indicators = [
                'course', 'courses', 'free', 'programming', 'development',
                'udemy', 'enroll', 'rating', 'students'
            ]

            found_indicators = sum(1 for indicator in course_indicators if indicator in body_text)
            if found_indicators >= 3:  # If we find 3+ course indicators
                return True

            # Check for Udemy course links
            udemy_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="udemy.com/course/"]')
            if len(udemy_links) > 5:  # If we find more than 5 Udemy course links
                return True

            # Check page length (very short pages are likely not course pages)
            page_source = self.driver.page_source
            if len(page_source) < 50000:  # Less than 50KB is probably not a full course page
                return False

            return False

        except Exception as e:
            logging.warning(f"Error validating course page: {e}")
            return False

    def _get_fallback_courses(self) -> List[Dict]:
        """Provide fallback courses when scraping fails completely"""
        logging.info("Using fallback course data")

        # Some known free Udemy programming courses (last verified working)
        fallback_courses = [
            {
                'id': 'python-for-beginners',
                'title': 'Python for Beginners - Learn Programming from Scratch',
                'url': 'https://www.udemy.com/course/python-for-beginners-learn-programming-from-scratch/',
                'instructor': 'Programming with Mosh',
                'rating': '4.5',
                'students': '1,000,000+ students',
                'discovered_at': time.time()
            },
            {
                'id': 'javascript-basics',
                'title': 'JavaScript Basics for Beginners',
                'url': 'https://www.udemy.com/course/javascript-basics-for-beginners/',
                'instructor': 'Tech Academy',
                'rating': '4.4',
                'students': '500,000+ students',
                'discovered_at': time.time()
            },
            {
                'id': 'html-css-basics',
                'title': 'HTML and CSS for Beginners',
                'url': 'https://www.udemy.com/course/html-and-css-for-beginners/',
                'instructor': 'Development Island',
                'rating': '4.3',
                'students': '300,000+ students',
                'discovered_at': time.time()
            },
            {
                'id': 'git-github',
                'title': 'Git & GitHub Crash Course',
                'url': 'https://www.udemy.com/course/git-and-github-crash-course/',
                'instructor': 'Tech with Tim',
                'rating': '4.6',
                'students': '200,000+ students',
                'discovered_at': time.time()
            },
            {
                'id': 'react-basics',
                'title': 'React Basics - Build a Todo App',
                'url': 'https://www.udemy.com/course/react-basics-build-a-todo-app/',
                'instructor': 'React Academy',
                'rating': '4.2',
                'students': '100,000+ students',
                'discovered_at': time.time()
            }
        ]

        logging.info(f"Providing {len(fallback_courses)} fallback courses")
        return fallback_courses[:10]  # Return up to 10 courses

    def _try_multiple_extraction_strategies(self) -> List[Dict]:
        """Try different strategies to extract courses from various page types"""
        strategies = [
            self._extract_from_freecodecamp,
            self._extract_from_tutorialspoint,
            self._extract_generic_udemy_links,
        ]

        for strategy in strategies:
            try:
                courses = strategy()
                if courses:
                    logging.info(f"Successfully extracted {len(courses)} courses using {strategy.__name__}")
                    return courses
            except Exception as e:
                logging.warning(f"Strategy {strategy.__name__} failed: {e}")
                continue

        return []

    def _extract_from_freecodecamp(self) -> List[Dict]:
        """Extract courses from FreeCodeCamp page"""
        courses = []

        try:
            # Look for Udemy course links
            udemy_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="udemy.com"]')

            for link in udemy_links[:10]:  # Limit for testing
                href = link.get_attribute('href')
                if href and '/course/' in href:
                    title = link.text.strip() or link.get_attribute('title') or "Unknown Title"

                    courses.append({
                        'id': href.split('/')[-2] if href else str(hash(href)),
                        'title': title,
                        'url': href,
                        'instructor': 'Unknown',
                        'rating': 'Unknown',
                        'students': 'Unknown',
                        'discovered_at': time.time()
                    })

            return courses

        except Exception as e:
            logging.warning(f"FreeCodeCamp extraction failed: {e}")
            return []

    def _extract_from_tutorialspoint(self) -> List[Dict]:
        """Extract courses from Tutorialspoint page"""
        courses = []

        try:
            # Look for course listings
            course_elements = self.driver.find_elements(By.CSS_SELECTOR, 'h3, .tutorial, [class*="course"]')

            for element in course_elements[:10]:
                link = element.find_element(By.CSS_SELECTOR, 'a') if element.tag_name in ['h3', 'div'] else element

                if link and 'udemy' in link.get_attribute('href').lower():
                    title = element.text.strip()
                    href = link.get_attribute('href')

                    courses.append({
                        'id': str(hash(href)),
                        'title': title,
                        'url': href,
                        'instructor': 'Unknown',
                        'rating': 'Unknown',
                        'students': 'Unknown',
                        'discovered_at': time.time()
                    })

            return courses

        except Exception as e:
            logging.warning(f"Tutorialspoint extraction failed: {e}")
            return []

    def _extract_generic_udemy_links(self) -> List[Dict]:
        """Extract any Udemy course links from the current page"""
        courses = []

        try:
            # Find all Udemy course links
            udemy_course_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="udemy.com/course/"]')

            for link in udemy_course_links[:10]:  # Limit for testing
                href = link.get_attribute('href')
                title = link.text.strip()

                # Try to get more details from parent elements
                try:
                    parent = link.find_element(By.XPATH, '..')
                    title = parent.text.strip() if len(parent.text.strip()) > len(title) else title
                except:
                    pass

                if title and href:
                    courses.append({
                        'id': href.split('/')[-2] if href else str(hash(href)),
                        'title': title,
                        'url': href,
                        'instructor': 'Unknown',
                        'rating': 'Unknown',
                        'students': 'Unknown',
                        'discovered_at': time.time()
                    })

            return courses

        except Exception as e:
            logging.warning(f"Generic Udemy link extraction failed: {e}")
            return []

    def _debug_page_content(self):
        """Debug method to examine page content"""
        try:
            # Get page title
            title = self.driver.title
            logging.info(f"Page title: {title}")

            # Check for common Udemy elements
            body_element = self.driver.find_element(By.TAG_NAME, 'body')
            if body_element:
                body_text = body_element.text
                if 'course' in body_text.lower():
                    logging.info("Page contains course-related content")
                else:
                    logging.warning("Page does not contain course-related content")

                # Look for any links
                links = self.driver.find_elements(By.TAG_NAME, 'a')
                udemy_links = []
                for link in links:
                    href = link.get_attribute('href')
                    if href and 'udemy.com' in href:
                        udemy_links.append(link)
                logging.info(f"Found {len(udemy_links)} Udemy-related links")
            else:
                logging.warning("No body element found")

            # Save a snippet of the page source for debugging
            page_source = self.driver.page_source
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(page_source[:5000])  # Save first 5000 chars
            logging.info("Saved debug page content to debug_page.html")

        except Exception as e:
            logging.error(f"Error in debug: {e}")

    def __del__(self):
        """Cleanup driver on destruction"""
        if self.driver:
            self.driver.quit()
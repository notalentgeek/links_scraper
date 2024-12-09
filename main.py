import time  # Import time module

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

URLS_TIMEOUT = 1

# List of URLs to process
urls = ['https://shopee.tw', 'https://www.naver.com/']

# Configure ChromeDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver_path = "/usr/local/bin/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


def process_url(url):
    try:
        # Open the URL
        driver.get(url)

        # Wait for the page to load (or until a specific element is present)
        try:
            WebDriverWait(driver, URLS_TIMEOUT).until(
                lambda driver: driver.execute_script(
                    "return document.readyState") == "complete"
            )
        except TimeoutException:
            raise TimeoutException(f"Timeout: The page at {
                                   url} took longer than {URLS_TIMEOUT} seconds to load.")

        # Wait for a short while to ensure any redirection completes
        time.sleep(5)

        # Capture the current URL after redirection
        current_url = driver.current_url
        if url != current_url:
            print(f"Redirected to: {current_url}")

        # Find all <a> tags
        link_elements = driver.find_elements(By.TAG_NAME, "a")

        # Extract and clean up links
        links = set()
        for idx, element in enumerate(link_elements):
            try:
                # Try getting href before any exception occurs
                href = element.get_attribute("href")
                if href and href.startswith("http"):  # Ensure it's a valid URL
                    links.add(href)
            except StaleElementReferenceException:
                # Log a proper error message
                print(
                    f"Warning: Element at index {
                        idx} became stale and could not be accessed. Skipping this element."
                )
            except Exception as e:
                # Log unexpected errors with details
                print(f"Error: Failed to process element at index {
                    idx} due to: {e}.")

        # Output all unique links
        links = list(links)
        print("Extracted Links:")
        for link in links:
            print(link)
    finally:
        # After processing each URL, idle for 1 minute
        print("Waiting for 1 minute before processing next URL...")
        time.sleep(1)  # Idle for 1 minute


# Iterate over each URL in the list
for url in urls:
    process_url(url)


# finally:
#     # Clean up
#     driver.quit()

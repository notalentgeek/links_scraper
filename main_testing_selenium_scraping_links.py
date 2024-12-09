import time  # Import time module

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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

try:
    # Open Shopee's homepage
    url = "https://shopee.tw"
    driver.get(url)

    # Wait for a short while to ensure any redirection completes
    time.sleep(5)

    # Capture the current URL after redirection
    current_url = driver.current_url
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
    # Clean up
    driver.quit()

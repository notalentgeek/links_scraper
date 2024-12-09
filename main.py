import threading  # Import threading module for timeout
import time  # Import time module

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

URL_TIMEOUT = 10
URL_WAIT_TIMER = 5  # Need to be smaller than URL_TIMEOUT

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

# A flag to indicate if the thread should stop
stop_flag = threading.Event()


def process_url(url):
    # Function to load the URL
    def load_url():
        try:
            if not stop_flag.is_set():
                driver.get(url)
        except Exception as e:
            print(f"Error while loading {url}: {e}")

    # Create a thread to load the URL
    thread = threading.Thread(target=load_url, name=url)
    thread.start()

    # Wait for the thread to complete, with a timeout of 60 seconds
    try:
        thread.join(URL_TIMEOUT)  # Timeout after 60 seconds
        if thread.is_alive():
            # If the thread is still running, set the stop flag
            print(f"Timeout: The page at {url} took longer than {
                  URL_TIMEOUT} seconds to load.")
            stop_flag.set()  # Signal the thread to stop (checked in `load_url`)
            thread.join()  # Wait for the thread to finish cleanly
        else:
            stop_flag.clear()  # Reset the flag for the next URL
            time.sleep(URL_WAIT_TIMER)  # Allow for any redirection to complete

            # Wait for a short while to ensure any redirection completes
            time.sleep(5)

            print(f"Page loaded: {url}")
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
                    # Ensure it's a valid URL
                    if href and href.startswith("http"):
                        links.add(href)
                except StaleElementReferenceException:
                    # Log a proper error message
                    print(f"Warning: Element at index {
                          idx} became stale and could not be accessed. Skipping this element.")
                except Exception as e:
                    # Log unexpected errors with details
                    print(f"Error: Failed to process element at index {
                          idx} due to: {e}.")

            # Output all unique links
            links = list(links)
            print("Extracted Links:")
            for link in links:
                print(link)

    except Exception as e:
        print(f"Error: {e}")

    # After processing each URL, idle for 1 minute
    print("Waiting for 1 minute before processing next URL...")
    time.sleep(1)  # Idle for 1 minute


# Iterate over each URL in the list
for url in urls:
    process_url(url)

# Clean up
driver.quit()

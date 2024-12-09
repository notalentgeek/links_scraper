from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from utils.config import CHROME_DRIVER_PATH


def setup_chrome_driver():
    """Set up and return a configured Chrome WebDriver instance."""
    # Configure ChromeDriver service
    chrome_service = Service(CHROME_DRIVER_PATH)

    # Configure ChromeDriver options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment for headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    )

    # Return the WebDriver instance
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configure ChromeOptions
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# Path to your downloaded ChromeDriver
driver_path = '/usr/local/bin/chromedriver'
service = Service(driver_path)

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
url = 'https://shopee.tw'
driver.get(url)

# Use WebDriverWait to wait for the title to load
try:
    wait = WebDriverWait(driver, 10)
    # Wait for the <title> tag to be present in the DOM
    element = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, 'title')))
    print('=====')
    print(driver.title)
    print('=====')
except Exception as e:
    print(f'Error occurred: {e}')

# Clean up
driver.quit()

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configure ChromeDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

driver_path = '/usr/local/bin/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Shopee's homepage
    url = 'https://shopee.tw'
    driver.get(url)

    # Wait for links to load (Wait for at least one <a> tag to appear)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

    # Use a set to store unique links
    links = set()

    # Just-in-Time Scraping
    print('Extracting links dynamically:')
    for element in driver.find_elements(By.TAG_NAME, 'a'):
        try:
            # Dynamically fetch and process each element
            href = element.get_attribute('href')
            if href and href.startswith('http'):  # Ensure it's a valid URL
                links.add(href)
        except StaleElementReferenceException:
            print('Skipping element due to StaleElementReferenceException')
        except Exception as e:
            print(f'Skipping element due to error: {e}')

    links = list(links)
    print('\nExtracted Links:')
    for link in links:
        print(link)

finally:
    # Clean up
    driver.quit()

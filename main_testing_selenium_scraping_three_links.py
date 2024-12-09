from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configure ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver_path = "/usr/local/bin/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Shopee's homepage
    url = "https://shopee.tw"
    driver.get(url)

    # Wait for links to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    # Find all <a> tags
    link_elements = driver.find_elements(By.TAG_NAME, "a")

    # Extract and clean up links
    links = set()
    for element in link_elements:
        try:
            href = element.get_attribute("href")
            if href and href.startswith("http"):  # Ensure it's a valid URL
                links.add(href)
        except Exception as e:
            # Handle any stale or missing elements gracefully
            print(f"Skipping element due to error: {e}")

    # Output three unique links
    links = list(links)[:3]
    print("Extracted Links:")
    for link in links:
        print(link)

finally:
    # Clean up
    driver.quit()

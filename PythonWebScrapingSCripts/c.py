from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys

# Ensure UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

def extract_main_wrapper_content(driver):
    try:
        # Wait for the main wrapper element to be present
        main_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.main__inner-wrapper.wrap"))
        )

        # Extract and process content as needed
        content = main_wrapper.get_attribute("innerHTML")
        print(content)  # Print the extracted content

    except Exception as e:
        print(f"Error extracting content: {e}")
        # Print the current page source for debugging
        print(driver.page_source)

# Set up Chrome options
chrome_options = Options()
# Comment out the headless mode to see the browser actions
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navigate to the URL
    url = 'https://www.checkers.co.za/c-2413/All-Departments/Food?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page=0'
    driver.get(url)

    # Ensure the page is fully loaded
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    
    # Extract content
    extract_main_wrapper_content(driver)
finally:
    # Close the WebDriver
    driver.quit()

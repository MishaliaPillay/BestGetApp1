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

def extract_product_info(driver):
    try:
        # Wait for the main product container to be present
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid.grid--flex.grid--space-y.layout--1x3"))
        )

        # Fetch all product items
        product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-list__item")  # Selector for product items
        print(product_items)
        if not product_items:
            print("No product items found!")
            return

        for item in product_items:
            # Initialize variables
            image_src = "Not found"
            product_name = "Not found"
            product_price = "Not found"

            # Extract product image
            try:
                img_tag = item.find_element(By.CSS_SELECTOR, "img.product-card__img")
                image_src = img_tag.get_attribute("src")
            except Exception as e:
                print(f"Error finding product image: {e}")

            # Extract product name
            try:
                product_name_element = item.find_element(By.CSS_SELECTOR, "a.range--title")
                product_name = product_name_element.text
            except Exception as e:
                print(f"Error finding product name: {e}")

            # Extract product price
            try:
                product_price_element = item.find_element(By.CSS_SELECTOR, "div.product-card__actions > strong.font-graphic > strong.price")
                product_price = product_price_element.text
            except Exception as e:
                print(f"Error finding product price: {e}")

            # Print extracted information if available
            if image_src != "Not found" and product_name != "Not found" and product_price != "Not found":
                print(f"Product Name: {product_name}")
                print(f"Product Image: {image_src}")
                print(f"Product Price: {product_price}")
                print("-" * 30)

    except Exception as e:
        print(f"Error extracting product info: {e}")
        # Print the entire page source for debugging
       

# Set up Chrome options
chrome_options = Options()
# Uncomment to see browser actions
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navigate to the URL
    url = 'https://www.woolworths.co.za/cat/Food?No=0&Nrpp=24'  # Replace with the actual URL
    driver.get(url)

    # Wait for the page to be fully loaded
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Extract content
    extract_product_info(driver)
finally:
    # Close the WebDriver
    driver.quit()

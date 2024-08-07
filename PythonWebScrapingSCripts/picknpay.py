from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
import traceback

# Ensure UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

def extract_product_info(driver):
    try:
        # Wait for the product container elements to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.x-product-container--grid.ml-0.mr-0.ng-star-inserted"))
        )

        # Fetch all product containers
        product_containers = driver.find_elements(By.CSS_SELECTOR, "div.x-product-container--grid.ml-0.mr-0.ng-star-inserted")

        if not product_containers:
            print("No product containers found!")
            return

        print(f"Found {len(product_containers)} product containers.")

        for container in product_containers:
            # Initialize variables
            image_src = "Not found"
            product_name = "Not found"
            product_price = "Not found"

            # Check if product image exists before extracting attributes
            try:
                product_image = container.find_element(By.CSS_SELECTOR, "img")
                image_src = product_image.get_attribute("src")
            except Exception as e:
                print(f"Error finding product image: {e}")

            # Check if product name exists before extracting attributes
            try:
                product_name_element = container.find_element(By.CSS_SELECTOR, "span.product-name")  # Adjust selector as needed
                product_name = product_name_element.text
            except Exception as e:
                print(f"Error finding product name: {e}")

            # Check if product price exists before extracting attributes
            try:
                product_price_element = container.find_element(By.CSS_SELECTOR, "span.product-price")  # Adjust selector as needed
                product_price = product_price_element.text
            except Exception as e:
                print(f"Error finding product price: {e}")

            # Print extracted information
            print("Product Image:", image_src)
            print("Product Name:", product_name)
            print("Product Price:", product_price)
            print("-" * 30)

    except Exception as e:
        # Print the error message and traceback
        print(f"Error extracting product info: {e}")
        traceback.print_exc()
        # Print the current page source for debugging
        print(driver.page_source)

# Set up Chrome options
chrome_options = Options()
# Uncomment to see browser actions
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navigate to the URL
    url = 'https://www.pnp.co.za/c/pnpbase?currentPage=1'
    driver.get(url)

    # Wait for the page to be fully loaded
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Extract content
    extract_product_info(driver)
finally:
    # Close the WebDriver
    driver.quit()

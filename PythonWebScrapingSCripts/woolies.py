from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
import traceback
import time

# Ensure UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

def extract_product_info(driver):
    try:
        # Wait for the main product container to be present
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.banner-wrapper"))
        )

        # Scroll through the page to load all items
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new items to load

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Wait for product items to be present
        WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-list__item"))
        )

        # Fetch all product items
        product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-list__item")

        if not product_items:
            print("No product items found!")
            return

        for item in product_items:
            # Scroll item into view
            driver.execute_script("arguments[0].scrollIntoView();", item)
            time.sleep(0.5)  # Give time for image to load

            # Initialize variables
            image_src = "Not found"
            product_name = "Not found"
            product_price = "Not found"

            # Extract product image
            try:
                product_image = item.find_element(By.CSS_SELECTOR, "div.product--image > img")
                image_src = product_image.get_attribute("src")
            except Exception as e:
                pass  # Ignore errors finding product image

            # Extract product name
            try:
                # Attempt to find the product name using the first CSS selector
                product_name_element = item.find_element(By.CSS_SELECTOR, "div.range--title.product-card__name > a")
                product_name = product_name_element.text
            except Exception:
                # If the first selector fails, catch the exception and attempt with the second selector
                try:
                    print("First selector failed, trying the second one...")
                    product_name_element = item.find_element(By.CSS_SELECTOR, "div.product--desc > a > h2")
                    product_name = product_name_element.text
                except Exception:
                    # If the second selector also fails, handle the error or set a default value
                    print("Both selectors failed to find the product name.")
                    product_name = "Not found"

            # Extract product price
            try:
                product_price_element = item.find_element(By.CSS_SELECTOR, "span.font-graphic > strong")
                product_price = product_price_element.text
            except Exception as e:
                pass  # Ignore errors finding product price

            # Print extracted information if available
            if image_src != "Not found" or product_name != "Not found" or product_price != "Not found":
                print(f"Product Image: {image_src}")
                print(f"Product Name: {product_name}")
                print(f"Product Price: {product_price}")
                print("-" * 30)
                #print(item.get_attribute('outerHTML'))
                #print("-" * 30)


    except Exception as e:
        print(f"Error extracting product info: {e}")
        traceback.print_exc()
        # Print the current page source for debugging
        print(driver.page_source)

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
    url = 'https://www.woolworths.co.za/cat/Food?No=0&Nrpp=50'
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

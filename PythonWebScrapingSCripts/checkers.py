from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager#type:ignore
import sys

# Ensure UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')

def extract_main_wrapper_content(driver):
    try:
        # Wait for the main wrapper element to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product__listing.product__grid"))
        )

        # Extract and process content as needed
        #content = main_wrapper.get_attribute("innerHTML")
        #print(content)  # Print the extracted content

        product_items=driver.find_elements(By.CSS_SELECTOR,"div.item-product")

        
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
                product_image = item.find_element(By.CSS_SELECTOR, "div.item-product__image.__image > a > img")
                image_src = product_image.get_attribute("src")
            except Exception as e:
                pass  # Ignore errors finding product image

            # Extract product name
            try:
                product_name_element = item.find_element(By.CSS_SELECTOR, "h3.item-product__name > a")
                product_name = product_name_element.text
            except Exception as e:
                pass  # Ignore errors finding product name

            # Extract product price
            try:
                product_price_element = item.find_element(By.CSS_SELECTOR, "div.special-price__price > span")
                product_price = product_price_element.text
            except Exception as e:
                pass  # Ignore errors finding product price

            # Print extracted information if available
            if image_src != "Not found" or product_name != "Not found" or product_price != "Not found":
                print(f"Product Image: {image_src}")
                print(f"Product Name: {product_name}")
                print(f"Product Price: {product_price}")
                print("-" * 30)

    except Exception as e:
        print(f"Error extracting content: {e}")
        # Print the current page source for debugging
        print(driver.page_source)







# Set up Chrome options
chrome_options = Options()
# Comment out the headless mode to see the browser actions
chrome_options.add_argument("--headless")
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

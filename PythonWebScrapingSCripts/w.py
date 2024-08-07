import requests
from bs4 import BeautifulSoup

def find_product_list_items(url, outer_div_classes):
  """Finds divs with class 'product-list__item' within a div with specified classes.

  Args:
    url: The URL of the webpage.
    outer_div_classes: A list of class names for the outer div.

  Returns:
    A list of divs with the class 'product-list__item'.
  """

  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  outer_divs = soup.find_all('div', class_=outer_div_classes)  # Find all matching outer divs

  product_list_items = []
  for outer_div in outer_divs:
    items = outer_div.find_all('div', class_='product-list__item')
    product_list_items.extend(items)

  return product_list_items

# Example usage:
url = "https://www.woolworths.co.za/cat/Food?No=0&Nrpp=24"  # Replace with the actual URL
outer_div_classes = ['grid', 'grid--flex', 'grid--space-y', 'layout--1x4']
product_items = find_product_list_items(url, outer_div_classes)

if product_items:
    for item in product_items:
        # Print with UTF-8 encoding
        print(item.prettify(encoding='utf-8'))  # Prettify for better readability
else:
    print("No product list items found.")
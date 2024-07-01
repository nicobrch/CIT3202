from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import random

# Save product and price_value in a list
product_data = []

def extract_and_insert_products(products):
  print("Extrayendo productos...")
  for product in products:
    name = product.find('h6', itemprop='name').get_text(strip=True)
    price_span = product.find('span', {'data-oe-type': 'monetary', 'data-oe-expression': "combination_info['price']"})
    if price_span:
      price_value = price_span.find('span', class_='oe_currency_value').text
      # Remove non-numeric characters (e.g., spaces, commas) and convert to integer
      price_value = int(price_value.replace('.', '').strip())

    stock_value = random.randint(0, 50)
    rating_value = round(random.uniform(0, 5), 1)

    if name not in [p[0] for p in product_data]:
      product_data.append((name, price_value, stock_value, rating_value))

  print("Productos extraídos:", len(product_data))

def save_to_csv():
  # Define the CSV file path
  csv_file = "./docs/products.csv"
  print("Guardando productos en", csv_file)

  # Write the product data to the CSV file
  with open(csv_file, 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Price', 'Stock', 'Rating'])  # Write the header row
    writer.writerows(product_data)  # Write the product data rows

  print("Productos guardados")

def scrape_products(url):
# Set up the Selenium WebDriver
  driver = webdriver.Chrome() # Make sure you have chromedriver installed and in your PATH
  driver.get(url)

  # Simulate scroll events to load additional content
  for _ in range(75):  # Assuming there are 5 scroll events in total
    # Scroll down using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the dynamically loaded content to appear
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'oe_product')))

    # Extract and print initial data
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, 'html.parser')
    initial_products = initial_soup.find_all('td', class_='oe_product')
    extract_and_insert_products(initial_products)

  save_to_csv()

  # Close the WebDriver
  driver.quit()

scrape_products("https://geekz.cl/shop")
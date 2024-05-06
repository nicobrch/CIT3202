import db
import config
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def extract_and_insert_products(products):
   
  for product in products:
    name = product.find('h6', itemprop='name').get_text(strip=True)
    price = product.find('span', class_='oe_currency_value').get_text(strip=True)
    availability = random.choices([True, False], weights=[0.8, 0.2])[0]

    db.insert_product(name, price, availability)

def scrape_products(url):
# Set up the Selenium WebDriver
  driver = webdriver.Chrome() # Make sure you have chromedriver installed and in your PATH
  driver.get(url)

  # Simulate scroll events to load additional content
  for _ in range(20):  # Assuming there are 5 scroll events in total
    # Scroll down using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the dynamically loaded content to appear
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'oe_product')))

    # Extract and print initial data
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, 'html.parser')
    initial_products = initial_soup.find_all('td', class_='oe_product')
    extract_and_insert_products(initial_products)

  # Close the WebDriver
  driver.quit()

scrape_products(config.web_product_path)
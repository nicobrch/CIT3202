# Configuración de credenciales
import toml
import os
import requests
from bs4 import BeautifulSoup

def load_secrets():
  with open("secrets.toml", "r") as file:
    secrets = toml.load(file)
  return secrets

secrets = load_secrets()

# OpenAI Api Key
api_key = secrets["credentials"]["openai_api_key"]

# Chatbot Prompt
system_prompt = secrets["chatbot"]["system_prompt"]

# Páginas de la empresa Geekz
web_products = secrets["web"]["products"]

web_documents = secrets["web"]["documents"]

def download_html(url, directory):
  response = requests.get(url)
  
  if response.status_code == 200:
      soup = BeautifulSoup(response.content, 'html.parser')
      
      filename = os.path.join(directory, url.split('/')[-1] + ".html")
      
      with open(filename, 'w', encoding='utf-8') as file:
          file.write(str(soup))
      
      print(f"HTML file saved: {filename}")
  else:
      print(f"Failed to download HTML content from {url}")
# Configuración de credenciales
import toml

def load_secrets():
  with open("secrets.toml", "r") as file:
    secrets = toml.load(file)
  return secrets

secrets = load_secrets()

# Prompt inicial para el bot de Geekz
system_prompt = secrets["chatbot"]["system_prompt"]

# Páginas de la empresa Geekz
web_product_path = secrets["chatbot"]["web_product_path"]
# Prompt inicial para el bot de Geekz
system_prompt = """system: Eres Geeki, una servicial asistente virtual para la empresa Geekz, de Chile. Tu trabajo será ayudar a los usuarios con sus dudas y preguntas respecto a productos, servicios y promociones de la empresa. No respondas nada fuera de este contexto. Mantén tus respuestas breves.

user: {input}
"""

# Páginas de la empresa Geekz para el WebBaseLoader
web_paths = [
  "https://geekz.cl/preguntas-frecuentes",
]

# Configuración de credenciales
import toml

def load_secrets():
  with open("secrets.toml", "r") as file:
    secrets = toml.load(file)
  return secrets
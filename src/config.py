# Configuración de credenciales
import toml

production = True # Falso para python, True para streamlit
path = "./"

if production:
    path = "../"

def load_secrets():
    with open(f"{path}secrets.toml", "r") as file:
        secrets = toml.load(file)
    return secrets

secrets = load_secrets()

# OpenAI Api Key
openai_api_key = secrets["credentials"]["openai_api_key"]

# Pinecone Api Key
pinecone_api_key = secrets["credentials"]["pinecone_api_key"]

# Chatbot Prompt
system_prompt = secrets["chatbot"]["system_prompt"]
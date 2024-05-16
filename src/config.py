# Configuración de credenciales
import toml

def load_secrets():
    with open("secrets.toml", "r") as file:
        secrets = toml.load(file)
    return secrets

secrets = load_secrets()

# OpenAI Api Key
openai_api_key = secrets["credentials"]["openai_api_key"]

# Pinecone Api Key
pinecone_api_key = secrets["credentials"]["pinecone_api_key"]

# Pinecone Index Name
pinecone_index = secrets["credentials"]["pinecone_index"]

# Chatbot Prompt
system_prompt = secrets["chatbot"]["system_prompt"]
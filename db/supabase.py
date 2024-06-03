import os
from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.tools import tool

load_dotenv()

@tool
def similarity_search(query: str):
    """Busca información de la empresa, tales como horarios de atención tiendas y servicio al cliente, preguntas frecuentes, políticas de privacidad, despacho, devoluciones, etc. Recibe un texto de entrada para realizar una búsqueda por similitud."""
    try:
        matched_docs = vectorstore.similarity_search(query)
        return matched_docs[0].page_content
    except Exception as e:
        print(f"Error: {e}")
        return None

@tool
def search_products(name: str):
    """Busca productos por su nombre."""
    try:
        data, count = supabase.table("products").select("*").ilike("name", f"%{name}%").execute()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    
@tool
def cheaper_products(quantity: int, name: str = None):
    """Busca los N productos más baratos. Recibe un número entero para la cantidad de productos a buscar. También puede recibir un nombre de producto para buscar productos más baratos que contengan dicho nombre."""
    try:
        if name:
            data, count = supabase.table("products").select("*").ilike("name", f"%{name}%").limit(quantity).order("price").execute()
            return data
        else:
            data, count = supabase.table("products").select("*").limit(quantity).order("price").execute()
            return data
    except Exception as e:
        print(f"Error: {e}")
        return None

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small",
)

vectorstore = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name="documents",
    query_name="document_match",
    chunk_size=500,
)

def document_loader():
    loader = DirectoryLoader(
        path="docs",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
            "autodetect_encoding": True
        }
    )

    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        is_separator_regex=False,
    )

    docs = text_splitter.split_documents(documents)
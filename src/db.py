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
    matched_docs = vectorstore.similarity_search(query)
    return matched_docs[0].page_content

@tool
def search_products(name: str):
    """Busca productos por su nombre."""
    data, count = supabase.table("products").select("*").ilike("name", f"%{name}%").execute()
    return data

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
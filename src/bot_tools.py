import sql_db
import vector_db
from langchain_core.tools import tool

@tool
def informacion_empresa(query: str):
  """Busca dentro de la base de datos la información de la empresa, tales como información sobre horarios de atención tiendas y servicio al cliente, preguntas frecuentes, políticas de privacidad, despacho, devoluciones, etc."""
  return vector_db.search_documents(query)

tools = [
  informacion_empresa,
]
import db
import documents
from langchain_core.tools import tool
from langchain.tools.render import render_text_description_and_args

docs_dir = "../docs/"

@tool
def obtener_productos_por_precio(min_price: int, max_price: int):
  """Obtiene los productos dentro de un rango de precios."""
  products = db.get_products_by_price_range(min_price, max_price)
  return products

@tool
def obtener_productos_por_stock(stock: bool):
  """Obtiene los productos por disponibilidad de stock. Por ejemplo, si stock es True, se obtienen los productos en stock."""
  products = db.get_products_by_stock(stock)
  return products

@tool
def obtener_todos_los_productos():
  """Obtiene todos los productos de la base de datos."""
  products = db.get_all_products()
  return products

@tool
def obtener_informacion_tiendas(message: str):
  """Obtiene la información de las tiendas físicas de la empresa. Debe recibir un mensaje como input para buscar las tiendas."""
  stores = documents.search_document(f"{docs_dir}tiendas.txt", message)
  return stores

@tool
def obtener_preguntas_frecuentes(message: str):
  """Obtiene información sobre preguntas frecuentes. Debe recibir un mensaje como input para buscar una pregunta relacionada."""
  faq = documents.search_document(f"{docs_dir}faq.txt", message)
  return faq

@tool
def obtener_politicas_de_despacho(message: str):
  """Obtiene información sobre las politicas de despacho de la empresa. Debe recibir un mensaje como input para buscar informacion relacionada."""
  despachos = documents.search_document(f"{docs_dir}politicas-despacho.txt", message)
  return despachos

@tool
def obtener_politicas_de_privacidad(message: str):
  """Obtiene información sobre las politicas de privacidad. Debe recibir un mensaje como input para buscar informacion relacionada."""
  privacidad = documents.search_document(f"{docs_dir}politicas-privacidad.txt", message)
  return privacidad

@tool
def obtener_politicas_de_cambios_y_devoluciones(message: str):
  """Obtiene información sobre las politicas de cambios y devoluciones. Debe recibir un mensaje como input para buscar informacion relacionada."""
  cambios = documents.search_document(f"{docs_dir}politicas-cambios-devoluciones.txt", message)
  return cambios

tools = [
  obtener_productos_por_precio,
  obtener_productos_por_stock,
  obtener_todos_los_productos,
  obtener_informacion_tiendas,
  obtener_preguntas_frecuentes,
  obtener_politicas_de_despacho,
  obtener_politicas_de_privacidad,
  obtener_politicas_de_cambios_y_devoluciones,
]

tool_names = render_text_description_and_args(tools)
import db
from langchain_core.tools import tool

@tool
def obtener_productos_por_precio(min_price, max_price):
  """Obtiene los productos dentro de un rango de precios."""
  products = db.get_products_by_price_range(min_price, max_price)
  return products

@tool
def obtener_productos_por_stock(stock):
  """Obtiene los productos por disponibilidad de stock. Por ejemplo, si stock es True, se obtienen los productos en stock."""
  products = db.get_products_by_stock(stock)
  return products

@tool
def obtener_todos_los_productos():
  """Obtiene todos los productos de la base de datos."""
  products = db.get_all_products()
  return products
import sql_db
import vector_db
from langchain_core.tools import tool

@tool
def todos_los_productos():
  """Obtiene todos los productos de la base de datos."""
  products = sql_db.get_all_products()
  return products

@tool
def productos_por_nombre(nombre: str):
  """Obtiene los productos los cuáles contengan un string dentro de su nombre."""
  products = sql_db.get_products_by_name_likeliness(nombre)
  return products

@tool
def n_productos_con_menor_precio(cantidad: int):
  """Obtiene los N productos más baratos en precio."""
  products = sql_db.get_top_n_products_by_lower_price(cantidad)
  return products

@tool
def n_productos_con_mayor_precio(cantidad: int):
  """Obtiene los N productos más caros en precio."""
  products = sql_db.get_top_n_products_by_higher_price(cantidad)
  return products

@tool
def productos_por_rango_de_precios(precio_min: int, precio_max: int):
  """Obtiene todos los productos dado un rango de precio mínimo y máximo."""
  products = sql_db.get_products_by_price_range(precio_min, precio_max)
  return products

@tool
def productos_por_rango_de_stock(stock_min: int, stock_max: int):
  """Obtiene todos los productos dado un rango de stock mínimo y máximo."""
  products = sql_db.get_products_by_stock_range(stock_min, stock_max)
  return products

@tool
def n_productos_con_mayor_rating(cantidad: float):
  """Obtiene los N productos con mayor rating, es decir, lo mejor valorados."""
  products = sql_db.get_top_n_products_by_higher_rating(cantidad)
  return products

@tool
def buscar_informacion_empresa(query: str):
  """Busca dentro de la base de datos vectorial sobre información de la empresa Geekz, tal como preguntas frecuentes, politicas de cambios y devoluciones, politicas de despacho y privacidad y las tiendas. Recibe un string de consulta y devuelve la información más relevante."""
  products = vector_db.search(query)
  return products

tools = [
  todos_los_productos,
  productos_por_nombre,
  n_productos_con_menor_precio,
  n_productos_con_mayor_precio,
  productos_por_rango_de_precios,
  productos_por_rango_de_stock,
  n_productos_con_mayor_rating,
  buscar_informacion_empresa
]
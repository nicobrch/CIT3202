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

@tool
def obtener_informacion_de_la_empresa():
  """Obtiene la información de la empresa, tal como horario de atención servicio al cliente, direcciones de sucursales y horario de atención de sucursal, correo de servicio al cliente"""
  return ("""
  Horario de atención servicio al cliente: Lunes a Viernes de 11:00 a 19:00 hrs
  Correo de servicio al cliente: ayuda@geekz.cl
  Nuestras tiendas:
    * Costanera Center, PB Piso, Local 148 [Abierto de Lunes a Domingo de 10:00 a 20:30].
    * Mall Barrio Independencia Piso 1, Local MT-105 [Abierto de lunes a domingo de 10:00 a 20:00 hrs.].
    * Mall Plaza Oeste, 3er Piso, Local D333 [Abierto de Lunes a Domingo de 10:00 a 20:00].
    * Mall Plaza Los Dominicos, 3er Piso, Local A3049 [Abierto de Lunes a Domingo de 10:00 a 20:00].
    * Mall Marina Oriente, Piso -1, Local 04 [Abierto de Lunes a Viernes de 09:30 a 20:00,  Sabado y Dominingo 10:00 a 20:00].
    * Mall Open Plaza Rancagua, Piso 3. Mall Open Plaza Ovalle, Piso 1  local 1090 [Abierto de Lunes a Domingo de 10:00 a 20:30]
  """)

@tool
def obtener_preguntas_frecuentes():
  """Obtiene la información respecto a preguntas frecuentes de la empresa"""
  return ("""
  ¿Dónde están ubicadas las tiendas Geekz?
  - Contamos con cinco sucursales, ubicadas en Mall Costanera Center, Mall Plaza Oeste, Mall Plaza Los Domínicos, Mall Barrio Independencia, Mall Marina Oriente (Viña del mar), Mall Open Plaza Rancagua y Mall Open Plaza Ovalle . Para conocer las ubicaciones ingresa aquí: https://geekz.cl/tiendas
  ¿El stock que está en la web es el mismo que en las tiendas?
  - No, todos los productos que están en nuestra web corresponden al stock de nuestra bodega. Ten en cuenta que si el producto está en tienda, debes comprarlo directamente en ésta, puesto que TODAS las compras hechas en la web se sacarán de bodega.
  ¿Los valores son los mismos en web y tiendas? 
  - No, los precios pueden variar.
  ¿Hacen envíos a domicilio?
  Sí, puedes revisar los detalles acerca de los despachos aquí: https://www.geekz.cl/Politicas-de-Despacho
  ¿Cuál es el horario de atención al cliente?
  - El horario de Atención al Cliente es de lunes a viernes de 11:00 a 19:00 horas, este horario aplica para la atención por redes sociales (Facebook, Instagram, WhatsApp) y nuestros mails (ayuda@geekz.cl y sos@geekz.cl) Los cuales son nuestros únicos medios de contacto. Todas las consultas realizadas los días sábado, domingos y festivos serán atendidas el día lunes o día hábil siguiente.
  ¿Cuáles son los medios de pago disponibles en el sitio web?
  - Actualmente contamos con Flow (Webpay).
  Acabo de realizar una orden,  ¿Cuándo podré recibir mi pedido?
  - Los pedidos de la web tardan de 5 a 7 días hábiles en llegar a las tiendas ubicadas en Santiago (Costanera, Oeste, Dominicos e Independencia). En el caso de Mall Marina llegan 1 vez por semana por lo que pueden tardar de 7 a 14 días.
  ¿Qué son los eventos especiales?
  - Son eventos que pueden durar un fin de semana o varios días donde ofrecemos descuentos o cupones.
  ¿Cuánto tarda en llegar algo que compré en un evento especial?
  - El plazo de entrega máximo si compraste en un evento especial es de 20 días hábiles.
  ¿Puedo pagar una reserva en tienda?
  - No, las reservas sólo se pueden pagar a través de nuestra web.
  ¿El precio y despacho de una reserva siempre es el mismo?
  - En general, siempre intentamos mantener el precio de lanzamiento de la preventa, pero por motivos de fuerza mayor estos podrían cambiar si la reserva es sin pago anticipado, ya que esta se considera un compromiso de compra. Lo mismo sucede con los despachos, ya que en los meses que pueda tardar el lanzamiento y llegada del producto los valores del Courier pueden cambiar.
  ¿Puedo unir varios pedidos en un solo envío?
  - Sí, es posible siempre y cuando todas las órdenes estén sin pago. En cualquier otro estado no se podrán unir ya que el sistema no lo permite.
  Quiero cambiar la dirección de mi pedido y/o cambiarlo a despacho a domicilio/retiro en tienda,  ¿Cómo lo hago?
  - Si deseas hacer un cambio en el tipo de despacho o de dirección debes enviarnos una solicitud a nuestros canales de atención (redes sociales o mail ayuda@geekz.cl). Es importante que sepas que sólo podremos hacerlo si tu pedido está "sin pago" ni "entregado", si ya está pagado o fue solicitado a nuestra bodega es imposible cambiarlo, el sistema no lo permite.
  Cometí un error y no me di cuenta que mi pedido estaba con Retiro en Tienda, pero soy de región,  ¿Qué puedo hacer?
  - Debes enviarnos una solicitud a nuestros canales de atención (redes sociales o mail ayuda@geekz.cl) para poder enviar el pedido. Una vez hecha la solicitud y realizado el pago del envio, debemos esperar que tu pedido llegue a tienda y que nuestra bodega lo retire nuevamente para hacer el despacho correspondiente.
  """)
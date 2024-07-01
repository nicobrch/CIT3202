import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Función para leer el contenido de un archivo .txt
def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        texto = archivo.read()
    return texto

texto = ""

for archivo in os.listdir("./docs"):
    if archivo.endswith('.txt'):
        ruta_archivo = os.path.join("./docs", archivo)
        texto_archivo = leer_archivo(ruta_archivo)
        texto += texto_archivo

nube_palabras = WordCloud(width=800, height=400, background_color='white').generate(texto)

# Mostrar la nube de palabras
plt.figure(figsize=(10, 5))
plt.imshow(nube_palabras, interpolation='bilinear')
plt.axis('off')
plt.show()

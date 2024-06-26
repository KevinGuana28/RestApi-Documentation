from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# Caché simple en memoria
cache = {}
DURACION_CACHÉ = 300  # Duración del caché en segundos

def obtener_del_cache(clave):
    datos = cache.get(clave)
    if datos and (time.time() - datos['timestamp']) < DURACION_CACHÉ:
        return datos['value']
    else:
        return None

def establecer_en_cache(clave, valor):
    cache[clave] = {'value': valor, 'timestamp': time.time()}

@app.route('/products')
def obtener_productos():
    clave_cache = 'lista_productos'
    
    # Verificar el caché primero
    datos_cache = obtener_del_cache(clave_cache)
    if datos_cache:
        return jsonify(datos_cache)
    
    # Hacer una solicitud a la API si los datos no están en el caché
    response = requests.get('https://api.example.com/products')
    datos = response.json()
    
    # Almacenar la respuesta en el caché
    establecer_en_cache(clave_cache, datos)
    
    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)

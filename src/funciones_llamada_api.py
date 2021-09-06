# Librerias importadas token


import requests
import json



def geocode_coord(direccion):
    """
    Esta función saca las coordenadas de la dirección que le pases
    """
    data = requests.get(f"https://geocode.xyz/{direccion}?json=1").json()
    try:
        return {
            "type": "Point",
            "coordinates": [data["latt"], data["longt"]]
        }
    except:
        return data
    
def generar_json(diccionario, name, token, token2):
    
    url_query = 'https://api.foursquare.com/v2/venues/explore'
    
    parametros = {
        "client_id": token,
        "client_secret": token2,
        "v": "20180323",
        "ll": f"{diccionario['coordinates'][0]}, {diccionario['coordinates'][1]}",
        "query": name,
        "limit": 200
    }
    
    resp = requests.get(url_query, params=parametros).json()
    
    return resp
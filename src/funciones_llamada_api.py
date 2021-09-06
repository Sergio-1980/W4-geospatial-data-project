import requests
import json

from functools import reduce
import operator



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
    """
    Esta función genera un json
    """
    
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

def obtener_datos(resp):
    """
    Esta función filtra los datos del json
    """
    datos_busqueda = resp["response"]["groups"][0]["items"]

    for x in range(len(datos_busqueda)):

        datos_finales = datos_busqueda[x]["venue"]

    return datos_finales


def getFromDict(diccionario, mapa):
    return reduce(operator.getitem,mapa,diccionario)


def type_point(lista):
    return {"type": "Point", 
            "coordinates": lista }


def json_filtrado (datos_finales):
    mapa_nombre = ["venue", "name"]
    mapa_latitud = ["venue", "location", "lat"]
    mapa_longitud = ["venue", "location", "lng"]

    unjsonnuevo = []

    for dic in datos_finales:
        paralista= {}

        paralista["nombre"]= getFromDict(dic,mapa_nombre)
        paralista["latitud"]= getFromDict(dic,mapa_latitud)
        paralista["longitud"]= getFromDict(dic,mapa_longitud)
        paralista["location"]=  type_point([paralista["longitud"],paralista["latitud"]])

        unjsonnuevo.append(paralista)
    
    return unjsonnuevo
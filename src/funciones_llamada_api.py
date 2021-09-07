import requests
import json

from functools import reduce
import operator

import pandas as pd



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


def generar_json(url, diccionario, token, token2, *args ):
    """
    Esta función genera un json
    """
    lst = []
    for i in args:
        parametros = {
            "client_id": token,
            "client_secret": token2,
            "v": "20180323",
            "ll": f"{diccionario['coordinates'][0]}, {diccionario['coordinates'][1]}",
            "query": i,
            "limit": 200
        }
    
        resp = requests.get(url, params=parametros).json()
        lst.append(resp)
    return lst

def obtener_datos(resp):
    """
    Esta función filtra los datos del json
    """
    datos_finales = []
    for i in resp:
        datos_busqueda = i["response"]["groups"][0]["items"]


        for dato in datos_busqueda:
            datos_finales.append(dato["venue"])

    return datos_finales


def getFromDict(diccionario, mapa):
    return reduce(operator.getitem,mapa,diccionario)


def type_point(lista):
    return {"type": "Point", 
            "coordinates": lista }


def json_filtrado (datos_finales):
    mapa_nombre = ["name"]
    mapa_latitud = ["location", "lat"]
    mapa_longitud = ["location", "lng"]
    mapa_ciudad= ["location", "state"]

    unjsonnuevo = []

    for dic in datos_finales:  

        try:
            paralista= {}
            paralista["nombre"]= getFromDict(dic,mapa_nombre)
            paralista["latitud"]= getFromDict(dic,mapa_latitud)
            paralista["longitud"]= getFromDict(dic,mapa_longitud)
            paralista["ciudad"]= getFromDict(dic,mapa_ciudad)
            paralista["location"]=  type_point([paralista["longitud"],paralista["latitud"]])
            unjsonnuevo.append(paralista)
        except:
            pass

    return pd.DataFrame(unjsonnuevo)

def create_cat (datos_finales, full_df):
    lst= []
    for dic in datos_finales: 
        for i in list(range(145)):
            
            lst.append(datos_finales[i]["categories"][0]["name"])
            len(lst)
    
    x = pd.Series(lst)
    full_df["category"] = x
    return full_df 


# Exportamos el json con json.dump

def exportar_json (nombre_fichero, json_new):
    
    with open(f"{nombre_fichero}.json", "w") as f:
        json.dump(json_new, f)
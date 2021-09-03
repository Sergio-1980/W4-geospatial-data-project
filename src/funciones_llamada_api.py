class geocode:

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
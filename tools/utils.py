import random
import requests
import time

def calcular_financiamento(preco):
    if preco is None:
        return 0
    
    parcelas = 360
    entrada_pct = 0.2
    juros_anual = 0.1268   
    
    valor = preco * (1 - entrada_pct) * (1/parcelas + juros_anual/12)
    return round(valor, 2)

def safe_int(valor):
    try:
        return int(valor)
    except:
        return None
    
def generate_viewport(delta):    
    MIN_LAT = -23.80
    MAX_LAT = -23.35
    MIN_LNG = -46.85
    MAX_LNG = -46.35    

    viewports = []

    lat = MIN_LAT 
    while lat < (MAX_LAT):
        lng = MIN_LNG 
        while lng < MAX_LNG :

            viewport = {
                "north": round(lat + delta, 7),
                "south": round(lat, 7),
                "east": round(lng + delta, 7),
                "west": round(lng, 7)
            }

            viewports.append(viewport)
            lng += delta

        lat += delta
    print(len(viewports))
    return viewports  

def request_with_retry(url, headers, payload, retries=3):
    for i in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            return response

        except requests.exceptions.Timeout:
            print(f"Timeout tentativa {i+1}")
            time.sleep(5 * random.range(0.75, 1.25))

    return None
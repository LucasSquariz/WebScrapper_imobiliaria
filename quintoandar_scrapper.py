import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from utils import calcular_financiamento,safe_int
from google_sheets_api import insert_multiple_on_sheet, insert_element_on_sheet

base_url = "https://www.quintoandar.com.br"
#search_url = "https://www.quintoandar.com.br/imovel/893457372/comprar/casa-2-quartos-fazenda-da-juta-sao-paulo"
search_url = "https://apigw.prod.quintoandar.com.br/house-listing-search/v2/search/list"
site_name = "Quinto Andar"

def get_house_json_by_page(url, page = 1):
    headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.quintoandar.com.br",
    "Referer": "https://www.quintoandar.com.br/"
    }

    offset_base = 12 
    offset_final = 0   
    if page and page > 0:
        offset_final = offset_base * page    

    payload = {
        "context": {
            "mapShowing": True,
            "listShowing": True,
            "userId": "Fqy90w_8xYrUTOsyYEdZxwDT_AM8mruMSZrtvgnsNbzADSAMMlpwdw",
            "deviceId": "Fqy90w_8xYrUTOsyYEdZxwDT_AM8mruMSZrtvgnsNbzADSAMMlpwdw",
            "searchId": "d3754573-d95f-4810-a539-e5541d6dda7f",
            "numPhotos": 12,
            "isSSR": False
        },
        "filters": {
            "businessContext": "SALE",
            "blocklist": [],
            "selectedHouses": [],
            "location": {
                "coordinate": {
                    "lat": -23.55052,
                    "lng": -46.633309
                },
                "viewport": {
                    "east": -46.552799814208974,
                    "north": -23.453863413347698,
                    "south": -23.647105568529156,
                    "west": -46.713818185791006
                },
                "neighborhoods": [],
                "countryCode": "BR"
            },
            "priceRange": [],
            "specialConditions": [],
            "excludedSpecialConditions": [],
            "houseSpecs": {
                "area": {
                    "range": {}
                },
                "houseTypes": [],
                "amenities": [],
                "installations": [],
                "bathrooms": {
                    "range": {}
                },
                "bedrooms": {
                    "range": {}
                },
                "parkingSpace": {
                    "range": {}
                },
                "suites": {
                    "range": {}
                }
            },
            "availability": "ANY",
            "occupancy": "ANY",
            "partnerIds": [],
            "categories": [],
            "enableFlexibleSearch": True
        },
        "sorting": {
            "criteria": "RELEVANCE",
            "order": "DESC"
        },
        "pagination": {
            "pageSize": 12,
            "offset": offset_final
        },
        "slug": "sao-paulo-sp-brasil",
        "fields": [
            "id",
            "coverImage",
            "rent",
            "totalCost",
            "salePrice",
            "iptuPlusCondominium",
            "area",
            "imageList",
            "imageCaptionList",
            "address",
            "regionName",
            "city",
            "visitStatus",
            "activeSpecialConditions",
            "type",
            "forRent",
            "forSale",
            "isPrimaryMarket",
            "bedrooms",
            "parkingSpaces",
            "suites",
            "listingTags",
            "yield",
            "yieldStrategy",
            "neighbourhood",
            "categories",
            "bathrooms",
            "isFurnished",
            "installations",
            "amenities",
            "shortRentDescription",
            "shortSaleDescription"
        ],
        "locationDescriptions": [
            {
                "description": "sao-paulo-sp-brasil"
            }
        ],
        "topics": []
    }    

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()
    houses_json = data['hits']['hits'] 
    houses_info = []  

    for house in houses_json:
        print(house['_id'])

    if response.status_code == 200:
        print("deu bom")       
    return

def extract_house_info(json):
    price_value = 0
    cond_value = 0
    iptu_value = 0
    furnished = False
    size = 0
    car = 0
    type = ""
    street = ""
    neighborhood = ""
    city = ""
    financing = 0
    furniture_value = 0
    total_value = 0
    size_price = 0
    url = ""
    update_date = ""

    imovel_info = {
        "Tipo": type,
        "Endereco": street,
        "Bairro": neighborhood,
        "Cidade": city,
        "Metragem": size,
        "Vaga": car,
        "Mobiliado": furnished,
        "Preco": price_value,
        "Condominio": cond_value,
        "IPTU": iptu_value,
        "Valor financiamento": financing,
        "Moveis": furniture_value,
        "Valor total": total_value,
        "Valor metro": size_price,
        "Link": url,
        "Site": site_name,
        "Ultima atualizacao": update_date
    }        

    return

def main():
    extract_house_info(search_url)

main()
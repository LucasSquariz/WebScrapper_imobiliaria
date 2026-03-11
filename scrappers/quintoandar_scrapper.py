import os
from dotenv import load_dotenv
from datetime import datetime
from tools.utils import calcular_financiamento, generate_viewport, request_with_retry
from db.google_sheets_api import insert_multiple_on_sheet
from model.SheetsModel import SheetsModel
from db.database_sql import add_to_db

load_dotenv()
base_url = os.getenv("QUINTO_BASE_URL")
api_url = os.getenv("QUINTO_API_URL")
site_name = "Quinto Andar"

def get_house_json_by_page(url, viewport, page = 1):
    headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.quintoandar.com.br",
    "Referer": "https://www.quintoandar.com.br/",
    "x-ab-test": "ab_beakman_search_services_demand_concentration_v1_map_and_ssr_rent_experiment_v2:1,ab_beakman_search_services_demand_sufficiency_v1_sale_experiment:-1,ab_beakman_search_services_demand_sufficiency_v1_sale_experiment_rollout:false,ab_beakman_search_services_demand_sufficiency_v1_sale_experiment_rollout_v1:false,ab_beakman_search_services_demand_sufficiency_v1_sale_experiment_v1:-1,ab_beakman_search_services_feed_filter_search_profile_experiment:0,ab_beakman_search_services_hue_candidate_generation_experiment_v2:-1,ab_beakman_search_services_location_embedding_on_cg_experiment:1,ab_beakman_search_services_open_search_find:-1,ab_beakman_search_services_open_search_migration:false,ab_beakman_search_services_open_search_migration_rollout:false,ab_beakman_search_services_p_click_experiment_sale_v7:1,ab_beakman_search_services_p_click_experiment_v7:1"
    }

    offset_base = 500
    offset_final = 0   
    if page and page > 0:
        offset_final = offset_base * page    

    payload = {
        "context": {
            "mapShowing": True,
            "listShowing": True,
            "userId": os.getenv("QUINTO_USER_ID"),
            "deviceId": os.getenv("QUINTO_USER_ID"),            
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
                    "east": viewport['east'],
                    "north": viewport['north'],
                    "south": viewport['south'],
                    "west": viewport['west']
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
            "pageSize": offset_base,
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
    
    response = request_with_retry(url, headers=headers, payload=payload)        
    
    if response.status_code == 200:
        data = response.json()
        houses_json = data.get('hits', {}).get('hits', [])        
        houses_info = []  
        houses_id = set()        

        if houses_json:                          
            for house in houses_json:  
                if house and house.get('_source'):                                                    
                    id_imovel, info = extract_house_info(house)
                    if id_imovel not in houses_id:
                        houses_id.add(id_imovel)
                        houses_info.append(info) 
            return houses_info            
        else:
            print("no data in hits!")
    else:
        print(f"--{response.status_code}--")
        return None 

def get_all_data():     
    delta = 0.02
    viewports = generate_viewport(delta)
    
    viewport_count = 0
    all_data = []
    
    for view in viewports:        
        page = 1        

        viewport_count += 1
        if viewport_count < 0:
            continue
        while True:             
            print(f"Quinto andar page: {page}, viewport_count: {viewport_count}, viewport:{view}")       
            data = get_house_json_by_page(api_url, view, page)
            print(data)
            if not data:
                break            
            for info in data:
                all_data.append(info)
            page += 1
            print(f"Quantidade de imóveis: {len(data)}")        
    print(len(all_data))
    return all_data

def extract_house_info(json):
    source = json.get('_source')

    if not source:
        return None, None

    id = 0
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
    interest = False

    id = source.get('id')

    price_value = source.get('salePrice') or 0  
    # a api da quinto andar manda o condominio junto com o iptu, pesquisar pelo valor correto demandaria entrar em cada link, ou seja, aumentaria muito o tempo de execução
    cond_value = source.get('iptuPlusCondominium') or 0   
    size = source.get('area') or 0    
    car = source.get('parkingSpaces') or 0

    type = source.get('type') or ""
    street = source.get('address') or ""
    neighborhood = source.get('neighbourhood') or ""
    city = source.get('city') or ""

    url = f"{base_url}/imovel/{source['id']}/comprar"
    financing = calcular_financiamento(price_value) if  price_value > 0 else 0    
    total_value = round(financing + furniture_value + cond_value + iptu_value, 2)
    size_price = round(price_value / size, 2) if price_value and size and size > 0 else 0 
    update_date = datetime.now().strftime("%d-%m-%Y")

    sheet_model = SheetsModel(type, street, neighborhood, city, size, car, 
                              furnished, price_value, cond_value, iptu_value, financing, 
                              furniture_value, total_value, size_price, url, site_name, update_date, interest)
    imovel_info = sheet_model.to_dict()
          
    return id, imovel_info
    
def scrappy():    
    houses_json = get_all_data()   
    insert_multiple_on_sheet(houses_json) 
    add_to_db(houses_json)

def main():    
    scrappy()    

if __name__ == "__main__":
    main()
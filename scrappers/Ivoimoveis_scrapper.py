import os
import requests
import json
from dotenv import load_dotenv
from db.google_sheets_api import insert_multiple_on_sheet
from db.database_sql import add_to_db
from tools.utils import calcular_financiamento
from model.SheetsModel import SheetsModel

load_dotenv()
base_url = os.getenv("IVO_BASE_URL")
site_name = "Ivo Imóveis"

HEADERS = {
    "Accept" : "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.6",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

def get_houses_data(page_number=1):        
    print(f"Ivo Imóveis page: {page_number}")       
    api_url = f"{os.getenv("IVO_API_URL")}{page_number}"
    response = requests.get(api_url, headers=HEADERS)  

    data = json.loads(response.text)       

    house_datas = data.get("data", [])
    return house_datas


def extract_house_info(data):   
    if data:        
        full_adress = data["full_address"].split(" - ")
        full_heading = data['heading1'].split(",")
        furnished = False
        interest = False

        house_type = full_heading[0] or ""
        street = full_adress[0] or ""
        neighborhood = full_adress[1] or ""
        city = full_adress[2] or ""
        size = data['area'][0] or 0
        car = data['garages'][0] or 0
        price_value = data['sale_price'][0]
        cond_value = data.get('condo_fees') or 0
        iptu_value = data.get('property_tax') or 0
        financing = calcular_financiamento(data['sale_price'][0])
        furniture_value = 500 if furnished else 0
        total_value = financing + furniture_value + cond_value
        size_price = price_value / size if price_value and size > 0 else 0
        url = base_url + data['url']
        full_date = data['updated_at'].split("T")
        update_date = full_date[0]   

    sheet_model = SheetsModel(house_type, street, neighborhood, city, size, car, 
                              furnished, price_value, cond_value, iptu_value, financing, 
                              furniture_value, total_value, size_price, url, site_name, update_date, interest)
    house_info = sheet_model.to_dict()       
    return house_info 

def construct_json():
    page_count = 1
    house_json = []
    curr_data = get_houses_data(page_count)

    while  curr_data:        
        for info in curr_data:
            house_info = extract_house_info(info)
            house_json.append(house_info)            
        page_count += 1
        curr_data = get_houses_data(page_count)    

    print(len(house_json))
    return house_json

def scrappy(json):    
    insert_multiple_on_sheet(json)
    add_to_db(json)

def main():
    data = construct_json()
    scrappy(data) 

if __name__ == "__main__":
    main()
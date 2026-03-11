import requests
import os
from dotenv import load_dotenv
from tools.utils import calcular_financiamento
from datetime import datetime
from db.google_sheets_api import insert_multiple_on_sheet, insert_element_on_sheet
from model.SheetsModel import SheetsModel

load_dotenv()
base_page = os.getenv("LELLO_BASE_URL")
api_url = os.getenv("LELLO_API_URL")
site_name = "Lello Imóveis"

def get_houses():
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json", 
    "Accept-language": "pt-BR,pt;q=0.8",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",        
    }

    houses_json = []   
    
    response = requests.get(api_url, headers=headers)
    data = response.json()
    max_pages = data.get('pages', {})
    print(f"Max pages: {max_pages}")

    for page in range(max_pages):
        print(f"Lello imóveis página {page}")
        final_url = f"https://apigateway.lelloimoveis.com.br/v3/imoveis/search?interesses=1&finalidades=1&pagina=1&page={page}&limit=20"
        response = requests.get(final_url, headers=headers)
        data = response.json()
        houses_arr = data.get('list', [])
        for house in houses_arr:
            house_extracted = extract_house_info(house)
            houses_json.append(house_extracted)    

    print(f"Número de casas: {len(houses_json)}")    
    return houses_json

def extract_house_info(json):
    furniture_value = 0
    furnished = False
    interest = False

    house_type = json.get('tipoImovel') or ""
    street = json.get('endereco') or ""
    neighborhood = json.get('bairro') or ""
    city = json.get('cidade') or ""

    size = json.get('metragemPrincipal') or 0
    car = json.get('quantidadeVagas') or 0
    price_value = json.get('valorVenda') or 0
    cond_value = json.get('previsaoCondominio') or 0
    iptu_value = json.get('previsaoIptu') or 0

    financing = calcular_financiamento(price_value) if  price_value > 0 else 0 
    total_value = round(financing + furniture_value + cond_value + iptu_value, 2)
    size_price = round(price_value / size, 2) if price_value and size and size > 0 else 0
    cadastro = json.get('dataCadastro')
    update_date = datetime.strptime(cadastro, "%Y-%m-%d").strftime("%d-%m-%Y") or datetime.now().strftime("%d-%m-%Y")
    url = f"{base_page}/imovel/{json['idImovel']}"

    sheet_model = SheetsModel(house_type, street, neighborhood, city, size, car, 
                              furnished, price_value, cond_value, iptu_value, financing, 
                              furniture_value, total_value, size_price, url, site_name, update_date, interest)
    imovel_info = sheet_model.to_dict()
      
    print (imovel_info)   
    return imovel_info

def test():
    response = requests.get(api_url)
    data = response.json()
    houses_arr = data.get('list', [])
    data_test = extract_house_info(houses_arr[0])
    insert_element_on_sheet(data_test)
    print(data_test)

def scrappy():    
    all_data = get_houses()
    insert_multiple_on_sheet(all_data)

def main():    
    scrappy()

main()
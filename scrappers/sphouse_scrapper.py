import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from tools.utils import calcular_financiamento,safe_int
from db.google_sheets_api import insert_multiple_on_sheet
from model.SheetsModel import SheetsModel
from db.database_sql import add_to_db

load_dotenv()
base_url = os.getenv("SP_BASE_URL")
site_name = "Sp House"

def get_house_links_by_page(page):
    search_url = f"{os.getenv("SP_SEARCH_URL")}{page}/"    
    response_link = requests.get(search_url)    

    soup_house = BeautifulSoup(response_link.text, "html.parser")
    a_card = soup_house.find_all("a", class_="foto_imovel")

    houses_links = []

    if a_card:
        for card in a_card:
            full_url = base_url + card['href']
            houses_links.append(full_url)        
        return houses_links
    else:
        print("0 links")
        return None

def get_all_links():
    print("entrou no get_all_links")
    all_links = []
    page_number = 1

    data = get_house_links_by_page(page_number)
    
    while data:
        print(f"sp House page: {page_number}")
        for link in data:
            all_links.append(link)        
        page_number += 1
        data = get_house_links_by_page(page_number)
    
    return all_links

def extract_house_info(url):
    try:
        response_house = requests.get(url)
    except:
        return None

    if response_house.status_code != 200:
        return None

    #Selecionando as tags
    soup_house = BeautifulSoup(response_house.text, "html.parser")
    title_tag = soup_house.find("h1", class_="titulo")
    localization_tag = soup_house.find("h2", class_="localizacao")
    info_div = soup_house.find_all("div", class_="icone_unico")
    price_div = soup_house.find_all("div", class_="valor")
    
    #inicializando variáveis
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

    # =========================
    # Tipo
    # =========================
    if title_tag:
        title_text = title_tag.get_text(strip=True)
        title_split = title_text.split(",")
        type_split = title_split[0].split(" ")
        if len(type_split) > 0:
            type = type_split[0]

    # =========================
    # Metragem e vagas
    # =========================
    for div in info_div:

        # Metragem
        expand_icon = div.find("i", class_="expand")
        if expand_icon:
            spans = div.find_all("span")

            if len(spans) > 1:
                size_text = spans[1].get_text(strip=True)                
                size_text = size_text.replace("m²", "")
                size_text = size_text.replace("m2", "")                
                size_text = size_text.strip()               
                size_text = size_text.replace(",", ".")                
                try:
                    size = float(size_text)
                except:
                    size = 0

        # Vagas
        car_icon = div.find("i", class_="car")
        if car_icon:
            spans = div.find_all("span")
            if len(spans) > 1:
                car_text = spans[1].get_text(strip=True)
                car = car_text

    # =========================
    # Endereço
    # =========================
    if localization_tag:
        localization_text = localization_tag.get_text(strip=True)
        localization_split = localization_text.split("-")

        if len(localization_split) > 0:
            street = localization_split[0].strip()
        if len(localization_split) > 1:
            neighborhood = localization_split[1].strip()
        if len(localization_split) > 2:
            city = localization_split[2].strip()

    # =========================
    # Preço
    # =========================
    if len(price_div) > 0:
        h4_tag = price_div[0].find("h4")
        if h4_tag:
            price_text = h4_tag.get_text(strip=True)
            price_text = price_text.replace("R$", "")
            price_text = price_text.replace("$", "")
            price_text = price_text.replace(".", "")
            price_text = price_text.replace(",", ".")
            price_text = price_text.split(".")     
            price_text = price_text[0].strip()       
            price_value = safe_int(price_text)

    # =========================
    # Condomínio
    # =========================
    condo_small = soup_house.find("small", string=lambda t: t and "Condom" in t)

    if condo_small:
        parent_div = condo_small.find_parent("div")
        if parent_div:
            span = parent_div.find("span")
            if span:
                cond_text = span.get_text(strip=True)
                cond_text = cond_text.replace("R$", "")
                cond_text = cond_text.replace(".", "")
                cond_text = cond_text.split(",")[0]
                cond_value = safe_int(cond_text)

    # =========================
    # IPTU
    # =========================
    for div in soup_house.find_all("div", class_="valor"):
        small = div.find("small")

        if small and "IPTU" in small.get_text():
            span = div.find("span")
            if span:
                iptu_text = span.get_text(strip=True)
                iptu_text = iptu_text.replace("R$", "")
                iptu_text = iptu_text.replace(".", "")
                iptu_text = iptu_text.split(",")[0]
                iptu_value = safe_int(iptu_text)

    # =========================
    # Financiamento
    # =========================
    financing = calcular_financiamento(price_value) if price_value else 0

    # =========================
    # Móveis
    # =========================
    furniture_value = 500 if furnished else 0

    # =========================
    # Valor total
    # =========================
    financing = financing or 0
    furniture_value = furniture_value or 0
    cond_value = cond_value or 0
    iptu_value = iptu_value or 0
    total_value = round(financing + furniture_value + cond_value + iptu_value, 2)

    # =========================
    # Valor m²
    # =========================
    if price_value and size and size > 0:
        size_price = round(price_value / size, 2)
    else:
        size_price = 0

    # =========================
    # Data
    # =========================
    update_date = datetime.now().strftime("%d-%m-%Y")

    interest = False

    sheet_model = SheetsModel(type, street, neighborhood, city, size, car, 
                              furnished, price_value, cond_value, iptu_value, financing, 
                              furniture_value, total_value, size_price, url, site_name, update_date, interest)
    imovel_info = sheet_model.to_dict()
           
    return imovel_info

def construct_json():
    print("entrou no construct")
    houses_links = get_all_links()
    houses_data = []
    house_count = 1

    for link in houses_links:
        print(f"Sp House: imóvel {house_count}")
        print(f"Link: {link}")
        curr_data = extract_house_info(link)
        if curr_data:
            houses_data.append(curr_data)
            house_count += 1

    return houses_data

def scrappy():    
    houses_json = construct_json() 
    print(len(houses_json))  
    insert_multiple_on_sheet(houses_json) 
    add_to_db(houses_json)

def main():       
    scrappy()      

if __name__ == "__main__":
    main()
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils import calcular_financiamento,safe_int
from google_sheets_api import insert_multiple_on_sheet, insert_element_on_sheet

base_url = "https://sphouseimoveis.com"
site_name = "Sp House"

def get_house_links_by_page(page):
    search_url = f"https://sphouseimoveis.com/comprar/pagina-{page}/"
    
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

                # Remove m²
                size_text = size_text.replace("m²", "")
                size_text = size_text.replace("m2", "")

                # Remove espaços
                size_text = size_text.strip()

                # Troca vírgula por ponto
                size_text = size_text.replace(",", ".")

                # Converte
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
            price_text = price_text.replace(".", "")
            price_text = price_text.replace(",00", "")
            price_value = price_text

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
        "Site": site_name if 'site_name' in globals() else "",
        "Ultima atualizacao": update_date
    }        
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

def send_to_sheets(house_json):
    print("entrou no send_to_sheets")
    print(len(house_json))
    insert_multiple_on_sheet(house_json)
    return house_json    

def send_to_sheets_test():
    data = extract_house_info("https://sphouseimoveis.com/comprar/sp/sao-paulo/jabaquara/sala/74375551")
    insert_element_on_sheet(data)
    return

def main():
    #extract_house_info("https://sphouseimoveis.com/comprar/sp/sao-paulo/jabaquara/sala/74375551")
    json = construct_json() 
    send_to_sheets(json)  
    

main()
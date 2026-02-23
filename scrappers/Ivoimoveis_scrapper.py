from bs4 import BeautifulSoup
import requests
import json
import sqlite3

base_url = "https://www.ivoimoveis.com"
ivo_url = "https://www.ivoimoveis.com/imovel/apartamento-sao-paulo-4-quartos-208-m/AP5292-IVOA?from=sale"
HEADERS = {
    "Accept" : "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.6",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

#-------------UTILS-----------------
def safe_int(valor):
    try:
        return int(valor)
    except:
        return None

def get_houses_data(page_number=1):        
    print(f"Ivo Imóveis page: {page_number}")       
    page_url = f"https://www.ivoimoveis.com/api/listings/a-venda?pagina={page_number}"
    response = requests.get(page_url, headers=HEADERS)  

    data = json.loads(response.text)       

    house_datas = data.get("data", [])
    return house_datas


def extract_house_info(data):    
    if data:        
        full_adress = data["full_address"].split(" - ")
        endereco = full_adress[0]

        full_heading = data['heading1'].split(",")
        tipo = full_heading[0]

        bairro = full_adress[1]

        cidade = full_adress[2]

        metragem = data['area'][0]

        vagas_valor = data['garages'][0]

        preco = data['sale_price'][0]

        condominio_valor = data.get('condo_fees') or 0

        iptu_valor = data.get('property_tax') or 0

        link = base_url + data['url']

        full_date = data['updated_at'].split("T")
        atualizacao = full_date[0]    

    imovel_info = {
        "Endereço": endereco,
        "Tipo": tipo,
        "Bairro": bairro,
        "Cidade": cidade,
        "Metragem": metragem,
        "Vaga": vagas_valor,
        "Mobiliado": False,
        "Preço": preco,
        "Condominio": condominio_valor,
        "IPTU": iptu_valor,
        "Link": link,
        "Ultima atualizacao": atualizacao,
        "Site": "Ivo Imóveis"
    }

    return imovel_info   

def construct_json():
    page_count = 1
    house_json = []
    curr_data = get_houses_data(page_count)

    while  curr_data:        
        for info in curr_data:
            house_json.append(extract_house_info(info))
        page_count = page_count + 1
        curr_data = get_houses_data(page_count)
    print(len(house_json))
    return house_json

def main():
    construct_json()

if __name__ == "__main__":
    main()
from .google_sheets_api import insert_multiple_on_sheet
import requests
import json
from .utils import calcular_financiamento

base_url = "https://www.ivoimoveis.com"

HEADERS = {
    "Accept" : "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.6",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

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
        full_heading = data['heading1'].split(",")
        mobiliado = False

        tipo = full_heading[0]
        endereco = full_adress[0]
        bairro = full_adress[1]
        cidade = full_adress[2]
        metragem = data['area'][0]
        vagas_valor = data['garages'][0]
        preco = data['sale_price'][0]
        condominio_valor = data.get('condo_fees') or 0
        iptu_valor = data.get('property_tax') or 0
        financiamento = calcular_financiamento(data['sale_price'][0])
        furniture_value = 500 if mobiliado else 0
        total_value = financiamento + furniture_value + condominio_valor
        size_price = preco / metragem if preco and metragem > 0 else 0
        link = base_url + data['url']
        full_date = data['updated_at'].split("T")
        update = full_date[0]   

    imovel_info = {
        "Tipo": tipo,
        "Endereco": endereco,
        "Bairro": bairro,
        "Cidade": cidade,
        "Metragem": metragem,
        "Vaga": vagas_valor,
        "Mobiliado": mobiliado,
        "Preco": preco,
        "Condominio": condominio_valor,
        "IPTU": iptu_valor,
        "Valor financiamento": financiamento,
        "Moveis": furniture_value,
        "Valor total": total_value,
        "Valor metro": size_price,
        "Link": link,
        "Site": "Ivo Imóveis",
        "Ultima atualizacao": update
    }

    '''------- DEBUG ------------'''
    '''
    print(full_adress)
    print(imovel_info) 
    '''
    '''--------------------------'''
    return imovel_info 

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
    
    insert_multiple_on_sheet(house_json)

    print(len(house_json))
    return house_json

def test():
    data_test = get_houses_data(12)
    extract_house_info(data_test[5])    

def test_financiamento():
    print(calcular_financiamento(400000))
    return

def main():
    construct_json()

    #test_financiamento()
    #test()

if __name__ == "__main__":
    main()
from bs4 import BeautifulSoup
import requests
import json

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

def get_imoveis_links(page_number=1):
    base_url = "https://www.ivoimoveis.com"
    search_url = "https://www.ivoimoveis.com/imoveis/a-venda"
    page_url = f"https://www.ivoimoveis.com/api/listings/a-venda?pagina={page_number}"

    response = requests.get(page_url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")

    data = json.loads(response.text)    

    links = soup.find_all("a", href=True)    
    house_links = []       

    for link in links:
        link_ref = link['href']
        if "/imovel" in link_ref:
            full_url = base_url + link_ref
            house_links.append(full_url)
    #print(house_links)
    return house_links


def extract_imovel_info(imovel_url):
    response = requests.get(imovel_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    #Estrutura do título: [Tipo do imóvel], [metragem] m², à venda por R$ [Preço] - [Endereço] - [Bairro] - [Cidade/estado]
    titulo_div = soup.find("div", class_="title-and-breadcrumbs")
    detalhes_div = soup.find("div", class_="listing-details")
    if not titulo_div or not detalhes_div:
        print("Erro: estrutura principal não encontrada")
        return

    #Link
    link_tag = soup.find("link", rel="canonical")
    link = link_tag.get("href") if link_tag else None

    #Endereço
    endereco_span_tag = titulo_div.find("span")

    if endereco_span_tag:
        endereco_span = endereco_span_tag.get_text(strip=True)
    else:
        endereco_span = ""

    endereco_traco = endereco_span.split(" - ")
    tipo = endereco = bairro = cidade = None
    metragem = preco = None

    if len(endereco_traco) >= 4:
        info_inicial = endereco_traco[0]
        endereco = endereco_traco[1]
        bairro = endereco_traco[2]
        cidade = endereco_traco[3]

        endereco_virgula = info_inicial.split(",")

        if len(endereco_virgula) >= 3:
            tipo = endereco_virgula[0].strip()
            metragem = safe_int(endereco_virgula[1].replace("m²", "").strip())
            preco = endereco_virgula[2].replace("à venda por R$", "").strip()

    #IPTU/Condomínio
    iptu_div = soup.find("div", class_="taxs_sale")
    iptu_valor = 0
    condominio_valor = 0

    if iptu_div:
        iptu_ps = iptu_div.find_all("p")    

        for p in iptu_ps: 
            span = p.get_text().split("R$")
            if span[0] == "Condomínio":
                condominio_valor = safe_int(span[1].replace(".", "").replace("/mês", "").strip())            
            elif span[0] == "IPTU":
                iptu_valor = safe_int(span[1].replace(".", "").replace("/mês", "").strip())         
            else:
                print("erro")

    #Vaga
    vaga_div = detalhes_div.find("div", class_="garages")
    if vaga_div:
        vaga_span = vaga_div.find("span")
        vaga_split = vaga_span.get_text().strip().split(" ")
        vagas_valor = safe_int(vaga_split[0])
    else:
        vagas_valor = 0


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
        "Ultima atualizacao": "a",
        "Site": "Ivo Imóveis"
    }

    print(imovel_info)

def main():
    get_imoveis_links()

if __name__ == "__main__":
    main()
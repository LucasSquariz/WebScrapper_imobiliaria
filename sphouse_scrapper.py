from bs4 import BeautifulSoup
import requests

base_url = "https://sphouseimoveis.com"

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
    all_links = []
    page_number = 1

    data = get_house_links_by_page(page_number)
    
    while data:
        print(f"sp House page: {page_number}")
        for link in data:
            all_links.append(link)        
        page_number += 1
        data = get_house_links_by_page(page_number)

    print(all_links)
    print(len(all_links))
    return

def extract_house_info(url):
    response_house = requests.get(url)

    soup_house = BeautifulSoup(response_house.text, "html.parser")
    title = soup_house.find("h1", class_="titulo")
    localization = soup_house.find("h2", class_="localizacao")

    print(f"Titulo: {title.text}")
    print(f"localização: {localization.text}")
    return

def main():
    #get_all_links()
    extract_house_info("https://sphouseimoveis.com/comprar/sp/sao-paulo/jabaquara/apartamento/77167247")
    
main()
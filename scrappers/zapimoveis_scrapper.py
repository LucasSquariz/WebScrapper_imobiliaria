import cloudscraper
from bs4 import BeautifulSoup
import requests
import json

base_url = "https://www.zapimoveis.com.br/venda/imoveis/sp+sao-paulo/?transacao=venda&onde=%2CS%C3%A3o+Paulo%2CS%C3%A3o+Paulo%2C%2C%2C%2C%2Ccity%2CBR%3ESao+Paulo%3ENULL%3ESao+Paulo%2C-23.555771%2C-46.639557%2C&areaMinima=40"

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
data = scraper.get(base_url, headers={'x-domain': '.zapimoveis.com.br'}).text

soup = BeautifulSoup(data, "html.parser")

data_tag = soup.find_all("script", type="application/ld+json")
for tag in data_tag:
    if tag.string:  # garante que tem conteúdo
        data_obj = json.loads(tag.string)
        print(data_obj)

'''

with open("zapimoveis.json", "w", encoding="utf-8") as arquivo:
    json.dump(data_obj, arquivo, indent=4, ensure_ascii=False)
'''
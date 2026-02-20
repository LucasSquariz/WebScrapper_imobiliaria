from bs4 import BeautifulSoup
import requests

ivo_url = "https://www.ivoimoveis.com/imoveis/a-venda"

HEADERS = {
    "Accept" : "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.6",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

response = requests.get(ivo_url, headers=HEADERS)


soup = BeautifulSoup(response.text, "html.parser")

script_tag = soup.find("div", class_="digital-result digital-result__list")
html = script_tag

print(html.prettify())
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticação
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "config/credentials.json", scope
)

client = gspread.authorize(creds)

# Abrir planilha
sheet = client.open("Scrapper_imoveis").sheet1

#print(sheet.get_all_values())

def insert_element_on_sheet(obj):
    headers = sheet.row_values(1)

    data = {
        "Tipo": obj.get("Tipo", ""),
        "Endereço": obj.get("Endereco", ""),        
        "Bairro": obj.get("Bairro", ""),
        "Cidade": obj.get("Cidade", ""),
        "Metragem": obj.get("Metragem", 0),
        "Vaga": obj.get("Vaga", 0),
        "Mobiliado": obj.get("Mobiliado", False),
        "Preço": obj.get("Preco", ""),
        "Condominio": obj.get("Condominio", 0),
        "IPTU": obj.get("IPTU", 0),
        "Link": obj.get("Link", ""),
        "Ultima atualizacao": obj.get("Ultima atualizacao", ""),
        "Site": obj.get("Site", "")
    }

    row = [data.get(col, "") for col in headers]
    sheet.append_row(row)      

def insert_multiple_on_sheet(obj_list):    
    headers = sheet.row_values(1)
    
    rows = []

    for obj in obj_list:
        data = {
            "Tipo": obj.get("Tipo", ""),
            "Endereço": obj.get("Endereco", ""),        
            "Bairro": obj.get("Bairro", ""),
            "Cidade": obj.get("Cidade", ""),
            "Metragem": obj.get("Metragem", 0),
            "Vaga": obj.get("Vaga", 0),
            "Mobiliado": obj.get("Mobiliado", False),
            "Preço": obj.get("Preco", ""),
            "Condominio": obj.get("Condominio", 0),
            "IPTU (parcela 12x)": obj.get("IPTU", 0),
            "Valor do financiamento": obj.get("Valor financiamento", 0),
            "Móveis": obj.get("Moveis", 0),
            "Valor total 1ª parcela": obj.get("Valor total", 0),
            "Valor m²": obj.get("Valor metro", 0),
            "Link": obj.get("Link", ""),
            "Site": obj.get("Site", ""),
            "Ultima atualização": obj.get("Ultima atualizacao", "")
        }

        row = [data.get(col, "") for col in headers]
        rows.append(row)

    sheet.append_rows(rows, table_range="A:M")
    
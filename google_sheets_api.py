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

# Inserir uma linha
sheet.append_row([
    "Casa",
    "São Paulo",
    120,
    500000
])

print(sheet.get_all_values())
def calcular_financiamento(preco):
    if preco is None:
        return 0
    
    parcelas = 360
    entrada_pct = 0.2
    juros_anual = 0.1268   
    
    valor = preco * (1 - entrada_pct) * (1/parcelas + juros_anual/12)
    return round(valor, 2)

def safe_int(valor):
    try:
        return int(valor)
    except:
        return None
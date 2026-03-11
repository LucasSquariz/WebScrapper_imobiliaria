from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.SqlModel import Base, House

DATABASE_URL = "sqlite:///scraper_data.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

def add_to_db(obj_list):    
    print("entrou no add to db")
    session = SessionLocal()

    for obj in obj_list:
        house = House(        
        Tipo = obj.get("Tipo", ""),
        endereco = obj.get("Endereco", ""), 
        bairro = obj.get("Bairro", ""),
        cidade = obj.get("Cidade", ""),
        metragem = obj.get("Metragem", 0),
        vaga = obj.get("Vaga", 0),
        mobiliado = obj.get("Mobiliado", False),
        preco = obj.get("Preco", ""),
        condominio = obj.get("Condominio", 0),
        iptu = obj.get("IPTU", 0),
        valor_financiamento = obj.get("Valor financiamento", 0),           
        valor_moveis = obj.get("Moveis", 0),
        valor_total = obj.get("Valor total", 0),
        valor_metro = obj.get("Valor metro", 0),
        link = obj.get("Link", ""),
        site = obj.get("Site", ""),
        interesse = obj.get("Interesse", False),
        ultima_atualizacao = obj.get("Ultima atualizacao", "")
        )   
        session.add(house)

    session.commit()
    session.close()
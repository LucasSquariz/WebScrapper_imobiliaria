from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

class House(Base):
    __tablename__ = "casas"

    id = Column(Integer, primary_key=True, index=True)    
    Tipo = Column(String)
    endereco = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    metragem = Column(Integer)
    vaga = Column(Integer)
    mobiliado = Column(Boolean)
    preco = Column(Integer)
    condominio = Column(Integer)
    iptu = Column(Integer)
    valor_financiamento = Column(Float)            
    valor_moveis = Column(Integer)
    valor_total = Column(Float) 
    valor_metro = Column(Float)
    link = Column(String)
    site = Column(String)
    ultima_atualizacao = Column(String)
    interesse = Column(Boolean)
     
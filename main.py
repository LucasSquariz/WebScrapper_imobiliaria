import scrappers.quintoandar_scrapper as quintoScrapper
import scrappers.lello_scrapper as lello
import scrappers.sphouse_scrapper as sphouse
import scrappers.Ivoimoveis_scrapper as ivo
from db.database_sql import engine, SessionLocal
from model.SqlModel import Base , Product

Base.metadata.create_all(bind=engine)

def main():    
    quintoScrapper.main()
    lello.main()
    sphouse.main(
        ivo.main()
    )   
    
if __name__ == "__main__":
    main()
import scrappers.quintoandar_scrapper as quintoScrapper
import scrappers.lello_scrapper as lello
import scrappers.sphouse_scrapper as sphouse
import scrappers.Ivoimoveis_scrapper as ivo


def main():
    quintoScrapper.main()
    lello.main()
    sphouse.main(
        ivo.main()
    )
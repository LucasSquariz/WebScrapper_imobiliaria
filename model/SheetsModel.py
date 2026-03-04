class SheetsModel:
    def __init__(self, 
                 type="",
                 street="",
                 neighborhood="",
                 city="",
                 size=0,
                 car=0,
                 furnished=False,
                 price_value=0,
                 cond_value=0,
                 iptu_value=0,
                 financing=0,
                 furniture_value=0,
                 total_value=0,
                 size_price=0,
                 url="",
                 site_name="",
                 update_date="",
                 interest=False):

        self.type = type
        self.street = street
        self.neighborhood = neighborhood
        self.city = city
        self.size = size
        self.car = car
        self.furnished = furnished
        self.price_value = price_value
        self.cond_value = cond_value
        self.iptu_value = iptu_value
        self.financing = financing
        self.furniture_value = furniture_value
        self.total_value = total_value
        self.size_price = size_price
        self.url = url
        self.site_name = site_name
        self.update_date = update_date
        self.interest = interest

    def to_dict(self):
        return {
            "Tipo": self.type,
            "Endereco": self.street,
            "Bairro": self.neighborhood,
            "Cidade": self.city,
            "Metragem": self.size,
            "Vaga": self.car,
            "Mobiliado": self.furnished,
            "Preco": self.price_value,
            "Condominio": self.cond_value,
            "IPTU": self.iptu_value,
            "Valor financiamento": self.financing,
            "Moveis": self.furniture_value,
            "Valor total": self.total_value,
            "Valor metro": self.size_price,
            "Link": self.url,
            "Site": self.site_name,
            "Ultima atualizacao": self.update_date,
            "Interesse": self.interest
        }
import bs4
import requests
import lxml

from database_operations import Database


class Product:
    def __init__(self, name):
        self.name = name
        self.info = []
        self.prices = []
        self.cities = []


    def set_name(self):
        self.name = input("Product name: ")

    def set_name(self, name):
        self.name = name

    def set_product_list(self):
        pass
        # TODO

    def get_url(self):
        words = self.name.split()
        return 'https://www.olx.pl/oferty/q-' + '-'.join(words) + '/?page={}'

    def set_prices_and_cities(self):
        distinct_records = self.info[0]
        city_info = self.info[4]
        for product in distinct_records:
            title, price, city, link = product
            self.prices.append(price)
            self.cities.append((city))



class Page:

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    def __init__(self, url):
        self.url = url
        self.number_of_pages = self.get_number_of_pages()
        self.products = []

    def get_number_of_pages(self):
        return len(self.get_analyzed_page(1).select('.item.fleft'))

    def get_analyzed_page(self, number):
        req = requests.get(self.url.format(number), headers=self.header)
        return bs4.BeautifulSoup(req.text, "lxml")

    def parse_price(self, price):
        return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))

    def get_products_data(self):
        none_type_counter = 0
        for page_number in range(self.number_of_pages+1):
            page = self.get_analyzed_page(page_number)
            products = page.select('.offer-wrapper')
            for product in products:
                try:
                    title = product.find('strong').get_text().strip()
                    price = product.find('p', class_='price').get_text().strip()
                    footer = product.find('td', class_='bottom-cell')
                    location = footer.find('small', class_='breadcrumb').get_text().strip().split(',')[0]
                    link = product.find('a')['href']

                    if price.lower() not in ('za darmo', 'zamienię'):
                        self.products.append((title, self.parse_price(price), location, link))
                except:
                    none_type_counter += 1
        print(f'Number of products lacking in at least one argument: {none_type_counter}\n')

from web_scraping import Product, Page
from database_operations import Database
from csv_handler import CsvHandler
from pathlib import Path


def run():
    path = Path('Products/')
    path.mkdir(parents=True, exist_ok=True)
    while True:
        product_name = input('Product name: ')
        product = Product(product_name)
        main_page = Page(product.get_url())
        main_page.get_products_data()
        database = Database(product.name, main_page.products)
        database.run(product)
        csv_handler = CsvHandler(product)
        csv_handler.create_csv_distinct_records()
        csv_handler.create_csv_basic_price_info_by_city()

        new_product = input("Would you like to search for another product? Enter 'y' to run or any input to exit: ")
        if new_product.lower() == 'y':
            continue
        else:
            break


if __name__ == "__main__":
    run()

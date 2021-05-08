from web_scraping import Product, Page
from database_operations import Database
from csv_handler import CsvHandler

if __name__ == "__main__":
    phone = Product('Samsung S21 Ultra')
    main_page = Page(phone.get_url())
    main_page.get_products_data()

    database = Database(phone.name, main_page.products)
    database.run(phone)
    csv_handler = CsvHandler(phone)
    csv_handler.create_csv_distinct_records()
    csv_handler.create_csv_basic_price_info_by_city()
from web_scraping import Product, Page
from database_operations import Database

if __name__ == "__main__":
    phone = Product('Samsung S21 Ultra')
    main_page = Page(phone.get_url())
    main_page.get_products_data()

    database = Database(phone.name, main_page.products)
    database.run()

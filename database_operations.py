import sqlite3
from sqlite3 import Error
import os



class Database:

    def __init__(self, product_name, products):
        self.product_name = self.clean_table_name(product_name)
        self.products = products
        self.connection = self.establish_connection()
        self.cursor = self.connection.cursor()
        self.view_name = 'view_' + self.product_name

    def run(self):
        if self.connection is not None:
            self.create_table()
            self.insert_values()
            self.create_view()
            self.commit_changes()

            cheapest_offer = self.get_cheapest_offer()
            most_expensive_offer = self.get_most_expensive_offer()
            most_common_price = self.get_most_common_price()

            while True:
                try:
                    delete_decision = int(input('[0] delete database\n[1] delete data connected with this product\n[2] finish'))
                    break
                    # TODO
                except:
                    print('Invalid input')

            self.delete_view()
            self.delete_table()
            self.delete_database()

            self.commit_changes_and_close()

    def establish_connection(self):
        try:
            return sqlite3.connect(f'{self.product_name}.db')
        except Error as error:
            print(error)
            return None

    def clean_table_name(self, table_name):
        return ''.join(chr for chr in table_name if chr.isalnum())

    # not cleaning input would make program vulnerable to an SQL injection attack
    # clean_table_name('); drop tables --')  # returns 'droptables'

    def create_table(self):
        try:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.product_name} (title TEXT, price REAL, city TEXT, link TEXT)')
        except Error as error:
            print(error)

    def insert_values(self):
        try:
            self.cursor.executemany(f'INSERT INTO {self.product_name} VALUES (?, ?, ?, ?)', self.products)
        except Error as error:
            print(error)

    def create_view(self):
        try:
            self.cursor.execute(f'create view {self.view_name}(title, price, city, link) AS select distinct * from {self.product_name};')
        except Error as error:
            print(error)

    def get_distinct_records(self):
        try:
            self.cursor.execute(f'select * from {self.view_name};')
            return self.cursor.fetchall()
        except Error as error:
            print(error)

    def get_price_info(self):
        try:
            self.cursor.execute(f'select count(price), avg(price), min(price), max(price), city from {self.view_name} group by city order by max(price) desc;')
            return self.cursor.fetchall()
        except Error as error:
            print(error)

    def get_cheapest_offer(self):
        try:
            self.cursor.execute(f'select * from {self.view_name} order by  price asc limit 1;')
            return self.cursor.fetchall()
        except Error as error:
            print(error)

    def get_most_expensive_offer(self):
        try:
            self.cursor.execute(f'select * from {self.view_name} order by  price desc limit 1;')
            return self.cursor.fetchall()
        except Error as error:
            print(error)

    def get_most_common_price(self):
        try:
            self.cursor.execute(f'select price from {self.view_name} group by price order by count(price) desc limit 1;')
            return self.cursor.fetchall()
        except Error as error:
            print(error)

    def delete_view(self):
        try:
            self.cursor.execute(f'drop view {self.view_name};')
        except Error as error:
            print(error)

    def delete_table(self):
        try:
            self.cursor.execute(f'delete from {self.product_name};')
        except Error as error:
            print(error)

    def delete_database(self):
        try:
            self.delete_view()
            self.delete_table()
        except Error as error:
            print(error)
        finally:
            if os.path.exists(f'{self.product_name}.db'):
                os.remove(f'{self.product_name}.db')
            else:
                print("The file does not exist")

    def commit_changes(self):
        self.connection.commit()

    def commit_changes_and_close(self):
        self.commit_changes()
        self.connection.close()

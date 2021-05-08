import csv

class CsvHandler:
    def __init__(self, product):
        self.product = product
        self.product.name = self.clean_name(self.product.name)

    def clean_name(self, name):
        return ''.join(chr for chr in name if chr.isalnum())

    def create_csv_distinct_records(self):
        with open(f'{self.product.name}/{self.product.name}_distinct_records.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Title', 'Price', 'City', 'Link'])
            writer.writerows(self.product.info[0])

    def create_csv_basic_price_info_by_city(self):
        with open(f'{self.product.name}/{self.product.name}_basic_price_info_by_city.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['City', 'Count', 'Average', 'Min', 'Max'])
            writer.writerows(self.product.info[4])
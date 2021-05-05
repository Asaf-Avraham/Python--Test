import csv
import os


def read_dict_from_csv_file(filename):
    file = open(filename, 'r')
    reader = csv.reader(file)
    header = next(reader)
    Dict = dict()
    for Line in reader:
        line_dict = dict(zip(header, Line))
        key = line_dict['book_id']
        if Dict.get(key, None) is None:
            Dict[key] = line_dict  # new book
        else:
            Dict[key]['quantity'] = Dict[key].get('quantity', 1) + 1
    return Dict


class BookStore:

    def __init__(self, store_inventory: str):

        self.store_inventory = store_inventory
        self.book_dict = read_dict_from_csv_file(store_inventory)
        self.quantity_discount_dict = {1: 1, 2: 0.9, 3: 0.85, }

    def __str__(self):

        s = f'Load from {self.store_inventory}'
        for Element in self.book_dict.items():
            s += f'{Element}\n'
        return s

    def calculate_price(self, buy_file_name):

        purchase = read_dict_from_csv_file(buy_file_name)
        price = index = 0
        for Id, Dict in purchase.items():
            if self.book_dict.get(Id, None) is None:
                print(f'{buy_file_name} books purchase price is{price-price*10/100:10.2f} NIS')
                print(f'Error in {buy_file_name}: Book not in store inventory' + f' book ID={Id}')
            book_info = self.book_dict[Id]
            quantity = Dict.get('quantity', 1)
            if quantity > 1:
                price += int(book_info['price']) * (1 + (quantity - 1) * 0.95)
                index += quantity
            else:
                price += int(book_info['price'])
                index += 1
        discount = self.quantity_discount_dict.get(index, 0.8)
        return price * discount


def main():
    customer_list = ['user1.csv', 'user2.csv', 'user3.csv', 'user4.csv', 'user5.csv',
                     'user6.csv']
    best_book_shop = BookStore('./BooksData.csv')
    # print(best_book_shop)

    for customer_file_name in customer_list:
        if os.path.exists(customer_file_name):
            price = best_book_shop.calculate_price(customer_file_name)
            print(f'{customer_file_name} books purchase price is{price:10.2f} NIS')
        else:
            print(f'{customer_file_name} books purchase not found, check file name or path')


if __name__ == '__main__':
    main()

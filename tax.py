from math import ceil
from decimal import Decimal as D
from file import InputFile


class Tax:
    def __init__(self, file_name):
        self._exempts = ["pill", "book", "chocolate"]
        self._basicTax = D(10)
        self._importTax = D(5)
        self._precision = D(0.05)
        self._sales_taxes = D(0)
        self._total_price_with_taxes = D(0)
        self._file_name = file_name
        ifile = InputFile(file_name)
        self._list_of_items = []
        self._list_of_items = ifile.load_order_from_file()

    def basic_tax_exempt(self, product_name):

        for exempt in self._exempts:

            if exempt.upper() in product_name.upper():
                return True
        return False

    @staticmethod
    def import_tax_required(product_name):

        if "IMPORTED" in product_name.upper():
            return True
        return False

    def calculate_unitary_price_with_tax(self, product_name, sale_price):

        if not self.basic_tax_exempt(product_name):
            temp_tax = self._basicTax
            # temp_price = temp_price * (1 + self._basicTax/100)
        else:
            temp_tax = 0

        if self.import_tax_required(product_name):
            temp_tax += self._importTax

        only_tax = sale_price * (temp_tax / D(100))
        only_tax = ceil(only_tax*D(20))/D(20)
        price_with_tax = sale_price + only_tax
        return price_with_tax

    def calculate_total_price_with_tax(self, product_name, sale_price, quantity):
        price_with_tax = self.calculate_unitary_price_with_tax(product_name, sale_price) * quantity
        self._sales_taxes += price_with_tax - sale_price * quantity
        self._total_price_with_taxes += price_with_tax
        return price_with_tax

    @staticmethod
    def format_decimal(value):
        return '{0:.2f}'.format(value)

    def calculate(self):
        for dic in self._list_of_items:
            print(str(dic["quantity"]) + " " + dic["product_name"] + ": " +
                  str(self.calculate_total_price_with_tax(dic["product_name"],
                                                          D(dic["price"]),
                                                          D(dic["quantity"]))))
        print("Sales Taxes: " + self.format_decimal(self._sales_taxes))
        print("Total: " + self.format_decimal(self._total_price_with_taxes))

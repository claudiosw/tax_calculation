from math import ceil


class Tax:
    def __init__(self, file_name):
        self._exempts = ["pill", "book", "chocolate"]
        self._basicTax = 10
        self._importTax = 5
        self._precision = 0.05
        self._sales_taxes = 0
        self._total_price_with_taxes = 0
        self._file_name = file_name
        self._input_file = open(file_name, "r")
        self._list_of_items = []
        self.load_from_file()

    def load_from_file(self):
        with open(self._file_name) as f:

            for line in f:

                if line.find(" at ") > 0:
                    temp, price = line.rsplit(" at ", 1)
                    quantity, product_name = temp.split(" ", 1)
                    # print("quantity=" + str(quantity) + "product_name=" + product_name + "price=" + str(price))
                    self._list_of_items.append({"quantity": quantity, "product_name": product_name,
                                                "price": price})

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

    def calculate_price_with_tax(self, product_name, sale_price):

        if not self.basic_tax_exempt(product_name):
            temp_tax = self._basicTax
            # temp_price = temp_price * (1 + self._basicTax/100)
        else:
            temp_tax = 0

        if self.import_tax_required(product_name):
            temp_tax += self._importTax

        only_tax = sale_price * (temp_tax / 100)
        only_tax = ceil(only_tax*20)/20
        price_with_tax = sale_price + only_tax
        self._sales_taxes += price_with_tax - sale_price
        self._total_price_with_taxes += price_with_tax
        return price_with_tax

    @staticmethod
    def format_decimal(value):
        return '{0:.2f}'.format(value)

    def calculate(self):
        for dic in self._list_of_items:
            print(str(dic["quantity"]) + " " + dic["product_name"] + ": " +
                  self.format_decimal(self.calculate_price_with_tax(dic["product_name"], float(dic["price"]))))
        print("Sales Taxes: " + self.format_decimal(self._sales_taxes))
        print("Total: " + self.format_decimal(self._total_price_with_taxes))

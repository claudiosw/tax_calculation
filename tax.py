from math import ceil
from decimal import Decimal
from file import InputFile


def import_tax_required(product_name: str) -> str:
    """
    Return True if it is an imported product.

    :param str product_name: name of the product
    :return: if it is imported
    """
    return 'IMPORTED' in product_name.upper()


class Tax(object):
    """
    Class that does tax calculation

    Test case example:

    >>> from tax import Tax
    >>> t1 = Tax('inputs/Input1.txt')
    >>> t1.calculate()
    1 book: 12.49
    1 music CD: 16.49
    1 chocolate bar: 0.85
    Sales Taxes: 1.50
    Total: 29.83

    """

    def __init__(self, file_name: str):
        """

        :param file_name: path of the input file
        """
        self._exempts = ['pill', 'book', 'chocolate']
        self._basicTax = 10
        self._importTax = Decimal(5)
        self._sales_taxes = Decimal(0)
        self._total_price_with_taxes = Decimal(0)
        self._file_name = file_name
        ifile = InputFile(file_name)
        self._list_of_items = []
        self._list_of_items = ifile.load_order_from_file()

    def basic_tax_exempt(self, product_name: str) -> bool:
        """
        Check if the product is in the tax exempt list

        :param product_name: Description of the product
        :return: Return True if it is in the tax exempt list
        """

        for exempt in self._exempts:

            if exempt.upper() in product_name.upper():
                return True
        return False

    def calculate_unitary_price_with_tax(self, product_name: str, sale_price: Decimal) -> Decimal:
        """
        Calculate the unitary price with tax

        :param product_name: Description of the product
        :param sale_price: Sale price without tax
        :return: Sale price with tax
        """

        if self.basic_tax_exempt(product_name):
            temp_tax = 0
        else:
            temp_tax = Decimal(self._basicTax)

        if import_tax_required(product_name):
            temp_tax += self._importTax

        only_tax = sale_price * (temp_tax / Decimal(100))
        round_close_to = 0.05
        round_close_to = Decimal(round_close_to)
        only_tax = ceil(only_tax / round_close_to) * round_close_to
        return sale_price + only_tax

    def calculate_total_price_with_tax(
        self,
        product_name: str,
        sale_price: Decimal,
        quantity: Decimal,
    ) -> Decimal:
        """
        Calculate the total price with tax

        :param product_name: Description of the product
        :param sale_price: Unitary sale price without tax
        :param quantity: Quantity of products sold
        :return: Total sale price with tax
        """
        price_with_tax = self.calculate_unitary_price_with_tax(
            product_name,
            sale_price,
        ) * quantity
        self._sales_taxes += price_with_tax - sale_price * quantity
        self._total_price_with_taxes += price_with_tax
        return price_with_tax

    def calculate(self):
        """
        Get input data, calculate tax and output it

        """
        for dic in self._list_of_items:
            total_price_with_tax = self.calculate_total_price_with_tax(
                dic['product_name'],
                Decimal(dic['price']),
                Decimal(dic['quantity']),
            )
            print(
                '{quantity} {product_name}: {total_price_with_tax:.2f}'.format(
                    quantity=dic['quantity'],
                    product_name=dic['product_name'],
                    total_price_with_tax=total_price_with_tax,
                ),
            )
        print('Sales Taxes: {taxes:.2f}'.format(taxes=self._sales_taxes))
        print('Total: {total:.2f}'.format(total=self._total_price_with_taxes))

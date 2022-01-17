import pytest
from tax import *
from decimal import Decimal as D
import math


@pytest.mark.parametrize(
   'file_path, product_name, expected_result, desc', [
       ("inputs/Input1.txt", "chocolate bar", True, "Tax Exempt chocolate"),
       ("inputs/Input1.txt", "Book", True, "Tax Exempt book + different case"),
       ("inputs/Input1.txt", "packet of headache pills", True, "Tax Exempt pill"),
       ("inputs/Input1.txt", "imported bottle of perfume", False, "Not a Tax Exempt")
   ]
)
def test_tax_exempt(file_path, product_name, expected_result, desc):
    t1 = Tax(file_path)
    value = t1.basic_tax_exempt(product_name)
    assert value is expected_result


@pytest.mark.parametrize(
  'file_path, product_name, expected_result, desc', [
      ("inputs/Input1.txt", "imported box of chocolates", True, "Imported product"),
      ("inputs/Input1.txt", "box of chocolates", False, "Not a Imported product")
  ]
)
def test_import_tax_required(file_path, product_name, expected_result, desc):
   t1 = Tax(file_path)
   value = t1.import_tax_required(product_name)
   assert value is expected_result


@pytest.mark.parametrize(
  'file_path, product_name, sale_price, quantity, expected_result, desc', [
      ("inputs/Input1.txt", "book", 12.49, 1, 12.49, "Tax Exempt"),
      ("inputs/Input1.txt", "music CD", 14.99, 1, 16.49, "Basic Tax Required"),
      ("inputs/Input1.txt", "imported bottle of perfume", 47.50, 1, 54.65, "Basic and Importation Tax Required"),
      ("inputs/Input1.txt", "imported box of chocolates", 10.00, 1, 10.50, "Importation Tax Required")
  ]
)
def test_calculate_price_with_tax(file_path, product_name, sale_price, quantity, expected_result, desc):
   t1 = Tax(file_path)
   value = t1.calculate_total_price_with_tax(product_name, D(sale_price), D(quantity))
   assert math.isclose(value, expected_result, rel_tol=0.01)


@pytest.mark.parametrize(
  'desc, file_path, expected_result', [
      ("Test file with only 1 quantity", "inputs/Input3.txt",
       "1 imported bottle of perfume: 32.19\n1 bottle of perfume: 20.89\n1 packet of headache" + \
       " pills: 9.75\n1 box of imported chocolates: 11.85\nSales Taxes: 6.70\nTotal: 74.68\n"
       ),
      ("Test file with more than 1 quantity", "inputs/Input4.txt",
       "2 imported bottle of perfume: 64.38\n1 bottle of perfume: 20.89\n2 packet of headache" + \
       " pills: 19.50\n1 box of imported chocolates: 11.85\nSales Taxes: 10.90\nTotal: 116.62\n"
       ),
  ]
)
def test_calculate(desc, file_path, expected_result, capsys):
   t1 = Tax(file_path)
   t1.calculate()
   captured = capsys.readouterr()
   assert captured.out == expected_result


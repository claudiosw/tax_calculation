import pytest
from tax import *
from decimal import Decimal as D
import math


@pytest.mark.parametrize(
   'file_path, product_name, expected_result', [
       ("inputs/Input1.txt", "chocolate bar", True),
       ("inputs/Input1.txt", "Book", True),
       ("inputs/Input1.txt", "packet of headache pills", True),
       ("inputs/Input1.txt", "imported bottle of perfume", False)
   ]
)
def test_tax_exempt(file_path, product_name, expected_result):
    t1 = Tax(file_path)
    value = t1.basic_tax_exempt(product_name)
    assert value is expected_result


def test_import_tax_required():
    t1 = Tax("inputs/Input1.txt")
    value = t1.import_tax_required("imported box of chocolates")
    assert value is True

    t1 = Tax("inputs/Input1.txt")
    value = t1.import_tax_required("box of chocolates")
    assert value is False


def test_calculate_price_with_tax():
    t1 = Tax("inputs/Input1.txt")
    value = t1.calculate_total_price_with_tax("book", D(12.49), D(1))
    assert math.isclose(value, 12.49, rel_tol=0.01)

    t1 = Tax("inputs/Input1.txt")
    value = t1.calculate_total_price_with_tax("music CD", D(14.99), D(1))
    assert math.isclose(value, 16.49, rel_tol=0.01)

    t1 = Tax("inputs/Input1.txt")
    value = t1.calculate_total_price_with_tax("imported bottle of perfume", D(47.50), D(1))
    assert math.isclose(value, 54.65, rel_tol=0.01)

    t1 = Tax("inputs/Input1.txt")
    value = t1.calculate_total_price_with_tax("imported box of chocolates", D(10.00), D(1))
    assert math.isclose(value, 10.50, rel_tol=0.01)


def test_calculate(capsys):
    t1 = Tax("inputs/Input3.txt")
    t1.calculate()
    captured = capsys.readouterr()
    assert captured.out == "1 imported bottle of perfume: 32.19\n1 bottle of perfume: 20.89\n1 packet of headache" + \
                           " pills: 9.75\n1 box of imported chocolates: 11.85\nSales Taxes: 6.70\nTotal: 74.68\n"

    t1 = Tax("inputs/Input4.txt")
    t1.calculate()
    captured = capsys.readouterr()
    assert captured.out == "2 imported bottle of perfume: 64.38\n1 bottle of perfume: 20.89\n2 packet of headache" + \
                           " pills: 19.50\n1 box of imported chocolates: 11.85\nSales Taxes: 10.90\nTotal: 116.62\n"

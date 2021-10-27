import pytest
from tax import *
from decimal import Decimal as D
import math


def test_tax_exempt():
    t1 = Tax("inputs/Input1.txt")
    value = t1.basic_tax_exempt("chocolate bar")
    assert value is True

    t1 = Tax("inputs/Input1.txt")
    value = t1.basic_tax_exempt("Chocolate bar")
    assert value is True

    t1 = Tax("inputs/Input1.txt")
    value = t1.basic_tax_exempt("Book")
    assert value is True

    t1 = Tax("inputs/Input1.txt")
    value = t1.basic_tax_exempt("packet of headache pills")
    assert value is True

    t1 = Tax("inputs/Input1.txt")
    value = t1.basic_tax_exempt("imported bottle of perfume")
    assert value is False


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

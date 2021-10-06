import pytest
from tax import *


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
    value = t1.calculate_price_with_tax("book", 12.49)
    assert value == 12.49

    t1 = Tax("inputs/Input1.txt")
    value = t1.calculate_price_with_tax("music CD", 14.99)
    assert round(value, 2) == 16.49

    t1 = Tax("inputs/Input1.txt")
    value = t1.calculate_price_with_tax("imported bottle of perfume", 47.50)
    assert value == 54.65

    t1 = Tax("inputs/Input1.txt")
    value = t1.calculate_price_with_tax("imported box of chocolates", 10.00)
    assert value == 10.50


def test_format_decimal():
    t1 = Tax("inputs/Input1.txt")
    value = t1.format_decimal(12.5)
    assert value == "12.50"


def test_calculate(capsys):
    t1 = Tax("inputs/Input3.txt")
    t1.calculate()
    captured = capsys.readouterr()
    assert captured.out == "1 imported bottle of perfume: 32.19\n1 bottle of perfume: 20.89\n1 packet of headache" + \
                           " pills: 9.75\n1 box of imported chocolates: 11.85\nSales Taxes: 6.70\nTotal: 74.68\n"

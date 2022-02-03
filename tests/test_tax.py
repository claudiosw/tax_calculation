import pytest
from tax import Tax, import_tax_required
from decimal import Decimal
import math


file1 = 'inputs/Input1.txt'


@pytest.mark.parametrize(
    'file_path, product_name, expected_result, desc',
    [
        (file1, 'chocolate bar', True, 'Tax Exempt chocolate'),
        (file1, 'Book', True, 'Tax Exempt book + different case'),
        (file1, 'packet of headache pills', True, 'Tax Exempt pill'),
        (file1, 'imported bottle of perfume', False, 'Not a Tax Exempt'),
    ],
)
def test_tax_exempt(file_path, product_name, expected_result, desc):
    t1 = Tax(file_path)
    assert t1.basic_tax_exempt(product_name) is expected_result


@pytest.mark.parametrize(
    'product_name, expected_result, desc',
    [
        ('imported box of chocolates', True, 'Imported product'),
        ('box of chocolates', False, 'Not a Imported product'),
    ],
)
def test_import_tax_required(product_name, expected_result, desc):
    assert import_tax_required(product_name) is expected_result


@pytest.mark.parametrize(
    'file_path, product_name, sale_price, quantity, expected_result, desc',
    [
        (file1, 'book', 12.49, 1, 12.49, 'Tax Exempt'),
        (file1, 'music CD', 14.99, 1, 16.49, 'Basic Tax Required'),
        (
            file1,
            'imported bottle of perfume',
            47.50,
            1,
            54.65,
            'Basic and Importation Tax Required',
        ),
        (
            file1,
            'imported box of chocolates',
            10.00,
            1,
            10.50,
            'Importation Tax Required',
        ),
    ],
)
def test_calculate_price_with_tax(
    file_path,
    product_name,
    sale_price,
    quantity,
    expected_result,
    desc,
):
    t1 = Tax(file_path)
    error_precision = 0.01
    total = t1.calculate_total_price_with_tax(
        product_name,
        Decimal(sale_price),
        Decimal(quantity),
    )
    assert math.isclose(total, expected_result, rel_tol=error_precision)


@pytest.mark.parametrize(
    'file_path, expected_result, desc',
    [
        (
            'inputs/Input3.txt',
            '1 imported bottle of perfume: 32.19\n1 bottle of perfume: 20.89' +
            '\n1 packet of headache pills: 9.75\n1 box of imported chocolate' +
            's: 11.85\nSales Taxes: 6.70\nTotal: 74.68\n',
            'Test file with only 1 quantity',
        ),
        (
            'inputs/Input4.txt',
            '2 imported bottle of perfume: 64.38\n1 bottle of perfume: 20.89' +
            '\n2 packet of headache pills: 19.50\n1 box of imported chocolat' +
            'es: 11.85\nSales Taxes: 10.90\nTotal: 116.62\n',
            'Test file with more than 1 quantity',
        ),
    ],
)
def test_calculate(file_path, expected_result, desc, capsys):
    t1 = Tax(file_path)
    t1.calculate()
    captured = capsys.readouterr()
    assert captured.out == expected_result

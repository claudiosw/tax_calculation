class InputFile(object):
    """
    Class that deals with files

    Test case example:

    >>> from file import InputFile
    >>> ifile = InputFile('inputs/Input1.txt')
    >>> ifile.load_order_from_file()
    [{'quantity': '1', 'product_name': 'book', 'price': '12.49\n'}, {'quantity': '1', 'product_name': 'music CD',
    'price': '14.99\n'}, {'quantity': '1', 'product_name': 'chocolate bar', 'price': '0.85'}]

    """
    def __init__(self, file_name: str):
        """

        :param file_name: path of the input file
        """
        self._list_of_items = []
        self._file_name = file_name

    def load_order_from_file(self) -> list[str]:
        """
        Load file from self._file_name and return list with orders

        :return: Return list of orders
        """

        with open(self._file_name) as file_order:

            for line in file_order:

                if line.find(' at ') > 0:
                    temp, price = line.rsplit(' at ', 1)
                    quantity, product_name = temp.split(' ', 1)
                    self._list_of_items.append(
                        {
                            'quantity': quantity,
                            'product_name': product_name,
                            'price': price,
                        },
                    )
        return self._list_of_items

class InputFile:
    def __init__(self, file_name):
        self._input_file = open(file_name, "r")
        self._list_of_items = []
        self._file_name = file_name

    def load_order_from_file(self):
        with open(self._file_name) as f:

            for line in f:

                if line.find(" at ") > 0:
                    temp, price = line.rsplit(" at ", 1)
                    quantity, product_name = temp.split(" ", 1)
                    self._list_of_items.append({"quantity": quantity, "product_name": product_name,
                                                "price": price})
        return self._list_of_items
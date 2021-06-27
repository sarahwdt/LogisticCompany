class Order:
    def __init__(self, string):
        string = string.replace('\n', '')
        attr = string.split(':')
        self.id = attr[1] if len(attr) > 1 else ''
        self.status = attr[2] if len(attr) > 2 else ''
        self.products = list(attr[3].split(',')) if len(attr) > 3 else ''

    def save(self):
        if isinstance(self.products, list):
            return "order:" + str(self.id) + ":" + self.status + ":" + ",".join(self.products)
        else:
            return "order:" + str(self.id) + ":" + self.status + ":" + str(self.products)

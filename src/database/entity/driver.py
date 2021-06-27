class Driver:
    def __init__(self, string):
        string = string.replace('\n', '')
        attr = string.split(':')
        self.id = attr[1] if len(attr) > 1 else ''
        self.name = attr[2] if len(attr) > 2 else ''
        self.car = attr[3] if len(attr) > 3 else ''
        self.orders = list(attr[4].split(',')) if len(attr) > 4 else ''

    def save(self):
        if isinstance(self.orders, list):
            return "driver:" + str(self.id) + ":" + self.name + ":" + self.car + ":" + ",".join(self.orders)
        else:
            return "driver:" + str(self.id) + ":" + self.name + ":" + self.car + ":" + str(self.orders)

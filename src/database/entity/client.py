class Client:
    def __init__(self, string):
        string = string.replace('\n', '')
        attr = string.split(':')
        self.id = attr[1] if len(attr) > 1 else ''
        self.login = attr[2] if len(attr) > 2 else ''
        self.orders = list(attr[3].split(',')) if len(attr) > 3 else ''

    def save(self):
        if isinstance(self.orders, list):
            return "client:" + self.id + ":" + self.login + ":" + ",".join(self.orders)
        else:
            return "client:" + self.id + ":" + self.login + ":" + str(self.orders)

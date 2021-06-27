class Product:
    def __init__(self, string):
        string = string.replace('\n', '')
        attr = string.split(':')
        self.id = attr[1] if len(attr) > 1 else ''
        self.name = attr[2] if len(attr) > 2 else ''

    def save(self):
        return "product:" + self.id + ":" + self.name

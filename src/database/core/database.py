from src.database.entity.client import Client
from src.database.entity.driver import Driver
from src.database.entity.manager import Manager
from src.database.entity.order import Order
from src.database.entity.product import Product


class Database:
    def __init__(self, txt):
        self.txt = txt
        self.clients = []
        self.drivers = []
        self.orders = []
        self.products = []
        self.managers = []
        self.load()
        self.statuses = {"canceled": "Отменен",
                         "created": "Создан",
                         "on the way": "В пути",
                         "delivered": "Доставлен"}

    def load(self):
        db_file = open(self.txt, "rt")
        lines = db_file.readlines()
        for line in lines:
            name = line.split(':')[0]
            if name == 'client':
                self.clients.append(Client(line))
            if name == 'driver':
                self.drivers.append(Driver(line))
            if name == 'manager':
                self.managers.append(Manager(line))
            if name == 'order':
                self.orders.append(Order(line))
            if name == 'product':
                self.products.append(Product(line))
        db_file.close()
        error = self.validate()
        while error is not None:
            print(error)
            error = self.validate()
        self.save()

    def save(self):
        db_file = open(self.txt, "wt")
        for item in self.clients:
            db_file.write(item.save())
            db_file.write("\n")
        for item in self.drivers:
            db_file.write(item.save())
            db_file.write("\n")
        for item in self.managers:
            db_file.write(item.save())
            db_file.write("\n")
        for item in self.orders:
            db_file.write(item.save())
            db_file.write("\n")
        for item in self.products:
            db_file.write(item.save())
            db_file.write("\n")
        db_file.close()

    def validate(self):
        for i in range(len(self.products)):
            if self.try_parse_int(self.products[i].id) is None:
                deleted_id = self.products[i].id
                self.products.pop(i)
                return "Продукт с неверным id " + str(deleted_id) + "!"

            for temp in self.products:
                if self.products[i].id == temp.id and self.products[i] != temp:
                    deleted_id = self.products[i].id
                    self.products.pop(i)
                    return "Продукт с id " + str(deleted_id) + " существует!"

        for i in range(len(self.orders)):
            if self.try_parse_int(self.orders[i].id) is None:
                deleted_id = self.orders[i].id
                self.orders.pop(i)
                return "Продукт с неверным id " + str(deleted_id) + "!"

            for temp in self.orders:
                if self.orders[i].id == temp.id and self.orders[i] != temp:
                    deleted_id = self.orders[i].id
                    self.orders.pop(i)
                    return "Заказ с id " + str(deleted_id) + " существует!"

            if len(self.orders[i].products) == 0 or self.orders[i].products[0] == '':
                self.orders.pop(i)
                return "Пустой заказ"

            product_ids = self.to_list_ids(self.products)
            for product_i in range(len(self.orders[i].products)):
                if self.orders[i].products[product_i] not in product_ids:
                    self.orders[i].products.pop(product_i)
                    product_i -= 1

        for i in range(len(self.drivers)):
            if self.try_parse_int(self.drivers[i].id) is None:
                deleted_id = self.drivers[i].id
                self.drivers.pop(i)
                return "Водитель с неверным id " + str(deleted_id) + "!"

            for temp in self.drivers:
                if self.drivers[i].id == temp.id and self.drivers[i] != temp:
                    deleted_id = self.drivers[i].id
                    self.drivers.pop(i)
                    return "Водитель с id " + str(deleted_id) + " существует!"

            orders_ids = self.to_list_ids(self.orders)
            for order_i in range(len(self.drivers[i].orders)):
                if self.drivers[i].orders[order_i] not in orders_ids:
                    self.drivers[i].orders.pop(order_i)
                    order_i -= 1

        for i in range(len(self.clients)):
            if self.try_parse_int(self.clients[i].id) is None:
                deleted_id = self.clients[i].id
                self.clients.pop(i)
                return "Клиент с неверным id " + str(deleted_id) + "!"

            for temp in self.clients:
                if self.clients[i].id == temp.id and self.clients[i] != temp:
                    deleted_id = self.clients[i].id
                    self.clients.pop(i)
                    return "Клиент с id " + str(deleted_id) + " существует!"
                if self.clients[i].login != temp.login and self.clients[i] != temp:
                    deleted_id = self.clients[i].login
                    self.clients.pop(i)
                    return "Клиент с логином " + str(deleted_id) + " существует!"

            orders_ids = self.to_list_ids(self.orders)
            for order_i in range(len(self.clients[i].orders)):
                if self.clients[i].orders[order_i] not in orders_ids:
                    self.clients[i].orders.pop(order_i)
                    order_i -= 1

        for i in range(len(self.managers)):
            if self.try_parse_int(self.managers[i].id) is None:
                deleted_id = self.managers[i].id
                self.managers.pop(i)
                return "Менеджер с неверным id " + str(deleted_id) + "!"

            for temp in self.managers:
                if self.managers[i].id == temp.id and self.managers[i] != temp:
                    deleted_id = self.managers[i].id
                    self.managers.pop(i)
                    return "Менеджер с id " + str(deleted_id) + " существует!"
                if self.managers[i].login != temp.login and self.managers[i] != temp:
                    deleted_id = self.managers[i].name
                    self.managers.pop(i)
                    return "Менеджер с логином " + str(deleted_id) + " существует!"

        return None

    @staticmethod
    def try_parse_int(target):
        try:
            return int(target)
        except:
            return None

    @staticmethod
    def to_list_ids(arr):
        ids = []
        for i in arr:
            ids.append(i.id)
        return ids

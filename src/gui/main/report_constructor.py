from datetime import datetime


class ReportConstructor:
    def __init__(self, database) -> None:
        self.database = database

    def buildMainReport(self):
        report = "Отчет по состоянию системы\n" \
                 "==========================\n" \
                 "Количество заказов по статусам:\n"
        statuses = set()
        for order in self.database.orders:
            statuses.add(order.status)
        for status in statuses:
            report += "\t" + status
            count = 0
            for order in self.database.orders:
                if order.status == status:
                    count += 1
            report += ":" + str(count) + "\n"

        report += "==========================\n" \
                  + "Количество товаров доступных к заказу:" + str(len(self.database.products)) + "\n"

        active = 0
        sleep = 0
        for driver in self.database.drivers:
            if len(driver.orders) == 0:
                sleep += 1
            else:
                active += 1
        report += "==========================\n" \
                  "Количество водителей в работе:" + str(active) + "\n" \
                  + "Количество свободных водителей:" + str(sleep) + "\n"

        report += "==========================\n" \
                  + "Количество активных клиентов:" + str(len(self.database.clients)) + "\n"
        report += "==========================\n" \
                  + "Количество активных менеджеров:" + str(len(self.database.managers)) + "\n"
        report += "==========================\n" \
                  + "Отчет актуален на " + datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "\n"
        return report

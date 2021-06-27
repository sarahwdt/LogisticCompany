from tkinter import Button
from tkinter import filedialog

from src.gui.main.drivers_mainframe import DriversMainFrame
from src.gui.main.mainframe import MainFrame
from src.gui.main.orders_mainframe import OrdersMainFrame
from src.gui.main.products_mainframe import ProductsMainFrame
from src.gui.main.report_constructor import ReportConstructor
from src.gui.main.users_mainframe import UsersMainFrame


class ManagerMainFrame(MainFrame):
    def __init__(self, frame, database, user, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, screenName, baseName, className, useTk, sync, use)
        self.frame = frame
        Button(master=self, text='Заказы', command=self.openOrders).pack()
        Button(master=self, text='Продукты', command=self.openProducts).pack()
        Button(master=self, text='Водители', command=self.openDrivers).pack()
        Button(master=self, text='Пользователи', command=self.openUsers).pack()
        Button(master=self, text='Отчет', command=self.makeReport).pack()
        self.geometry('200x200+600+400')
        self.protocol("WM_DELETE_WINDOW", self.back)
        self.report_constructor = ReportConstructor(database)

    def back(self):
        self.frame.deiconify()
        self.destroy()

    def openOrders(self):
        self.withdraw()
        OrdersMainFrame(frame=self, database=self.database, user=self.user).mainloop()

    def openProducts(self):
        self.withdraw()
        ProductsMainFrame(frame=self, database=self.database, user=self.user).mainloop()

    def openDrivers(self):
        self.withdraw()
        DriversMainFrame(frame=self, database=self.database, user=self.user).mainloop()

    def openUsers(self):
        self.withdraw()
        UsersMainFrame(frame=self, database=self.database, user=self.user).mainloop()

    def makeReport(self):
        self.withdraw()
        dlg = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Простой txt файл", '*.txt')], )

        if dlg != '':
            f = open(dlg, "w")
            f.write(self.report_constructor.buildMainReport())
            f.close()
        self.deiconify()

from tkinter import Label, Button, Listbox, Toplevel, END, Entry, LabelFrame, messagebox, E, EW, W, NSEW, SW, NS

from src.database.entity.driver import Driver
from src.gui.main.mainframe import MainFrame


class DriversMainFrame(MainFrame):
    def __init__(self, frame, database, user, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, screenName, baseName, className, useTk, sync, use)
        self.frame = frame
        Button(self, text="Добавить", command=self.add).grid(row=0, column=1, sticky=NS)
        label_frame = LabelFrame(self, text="Водители")
        Label(master=label_frame, text="id", borderwidth=2, relief="solid").grid(row=0, column=0, sticky=E)
        Label(master=label_frame, text="Имя", borderwidth=2, relief="solid").grid(row=0, column=1, sticky=EW)
        Label(master=label_frame, text="Машина", borderwidth=2, relief="solid").grid(row=0, column=2, sticky=EW)
        Label(master=label_frame, text="Опции", borderwidth=2, relief="solid").grid(row=0, column=3, columnspan=3,
                                                                                    sticky=EW)

        for i in range(len(database.drivers)):
            Label(master=label_frame, text=database.drivers[i].id).grid(row=i + 1, column=0, sticky=E)
            Label(master=label_frame, text=database.drivers[i].name).grid(row=i + 1, column=1, sticky=EW)
            Label(master=label_frame, text=database.drivers[i].car).grid(row=i + 1, column=2, sticky=EW)
            Button(master=label_frame, text="Открыть", command=lambda ci=i: self.open(ci)).grid(row=i + 1, column=3,
                                                                                                sticky=W)
            Button(master=label_frame, text="Изменить", command=lambda ci=i: self.upd(ci)).grid(row=i + 1, column=4,
                                                                                                sticky=W)
            Button(master=label_frame, text="Удалить", command=lambda ci=i: self._delete(ci)).grid(row=i + 1, column=5,
                                                                                                   sticky=W)
        label_frame.grid(row=0, column=0, sticky=NSEW)
        Button(master=self, text='Назад', command=self.back).grid(row=1, column=0, sticky=SW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label_frame.grid_columnconfigure(1, weight=1)
        label_frame.grid_columnconfigure(2, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.back)

    def back(self):
        self.frame.deiconify()
        self.destroy()

    def add(self):
        top = Toplevel(self)

        Label(top, text="Идентификатор").pack()
        id_entry = Entry(top)
        id_entry.pack()

        Label(top, text="Имя").pack()
        name_entry = Entry(top)
        name_entry.pack()

        Label(top, text="Машина").pack()
        car_entry = Entry(top)
        car_entry.pack()

        orders_list = Listbox(top, selectmode="multiple")
        for item in self.database.orders:
            related = False
            for driver in self.database.drivers:
                if item.id in driver.orders:
                    related = True
            if not related:
                orders_list.insert(END, item.id)
        orders_list.pack()

        Button(top, text="Добавить",
               command=lambda: self._create(id_entry.get(), name_entry.get(), car_entry.get(), orders_list)).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def upd(self, i):
        top = Toplevel(self)

        Label(top, text='Идентификатор:' + self.database.drivers[i].id).pack()

        Label(top, text="Имя").pack()
        name_entry = Entry(top)
        name_entry.insert(END, self.database.drivers[i].name)
        name_entry.pack()

        Label(top, text="Машина").pack()
        car_entry = Entry(top)
        car_entry.insert(END, self.database.drivers[i].car)
        car_entry.pack()

        j = 0
        orders_list = Listbox(top, selectmode="multiple")
        for item in self.database.orders:
            related = False
            for driver in self.database.drivers:
                if item.id in driver.orders and self.database.drivers[i].id != driver.id:
                    related = True
            if not related:
                orders_list.insert(END, item.id)
                if item.id in self.database.drivers[i].orders:
                    orders_list.select_set(j)
                j += 1

        orders_list.pack()

        Button(top, text="Обновить",
               command=lambda: self._upd(i, name_entry.get(), car_entry.get(), orders_list)).pack()
        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def open(self, i):
        top = Toplevel(self)
        Label(top, text='Идентификатор:' + self.database.drivers[i].id).pack()
        Label(top, text='Имя:' + self.database.drivers[i].name).pack()
        Label(top, text='Машина:' + self.database.drivers[i].car).pack()
        label_frame = LabelFrame(top, text="Заказы")
        for order in self.database.orders:
            if order.id in self.database.drivers[i].orders:
                Label(label_frame, text=order.id).pack()
        label_frame.pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def _create(self, i, name, car, orders):
        orders_ids = []
        for i in orders.curselection():
            orders_ids.append(str(orders.get(i)))

        self.database.drivers.append(Driver('driver:' + str(i) + ':' + name + ':' + car + ':' + ','.join(orders_ids)))
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _upd(self, i, name, car, orders):
        self.database.drivers[i].name = name
        self.database.drivers[i].car = car
        temp_orders = []
        if isinstance(orders.curselection(), tuple):
            for o in orders.curselection():
                temp_orders.append(orders.get(o))
            self.database.drivers[i].orders = temp_orders
        else:
            self.database.drivers[i].orders = orders.get(orders.curselection()) if orders.curselection() != '' else ''

        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _delete(self, i):

        self.database.drivers.pop(i)
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

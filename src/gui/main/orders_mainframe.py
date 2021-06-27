from tkinter import Label, Button, Listbox, Toplevel, END, Entry, LabelFrame, messagebox, W, EW, E, NSEW, SW, NS

from src.database.entity.order import Order
from src.gui.main.mainframe import MainFrame


class OrdersMainFrame(MainFrame):
    def __init__(self, frame, database, user, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, screenName, baseName, className, useTk, sync, use)
        self.frame = frame
        Button(self, text="Добавить", command=self.add).grid(row=0, column=1, sticky=NS)
        label_frame = LabelFrame(self, text="Все заказы")
        Label(master=label_frame, text="id", borderwidth=2, relief="solid").grid(row=0, column=0, sticky=E)
        Label(master=label_frame, text="Статус", borderwidth=2, relief="solid").grid(row=0, column=1, sticky=EW)
        Label(master=label_frame, text="Клиент", borderwidth=2, relief="solid").grid(row=0, column=2, sticky=EW)
        Label(master=label_frame, text="Машина", borderwidth=2, relief="solid").grid(row=0, column=3, sticky=EW)
        Label(master=label_frame, text="Опции", borderwidth=2, relief="solid").grid(row=0, column=4, columnspan=3,
                                                                                    sticky=EW)

        for i in range(len(database.orders)):
            Label(master=label_frame, text=database.orders[i].id).grid(row=i + 1, column=0, sticky=W)
            Label(master=label_frame, text=database.orders[i].status).grid(row=i + 1, column=1, sticky=EW)
            for c in range(len(database.clients)):
                if database.orders[i].id in database.clients[c].orders:
                    Label(master=label_frame, text=database.clients[c].login).grid(row=i + 1, column=2, sticky=EW)
            for d in range(len(database.drivers)):
                if database.orders[i].id in database.drivers[d].orders:
                    Label(master=label_frame, text=database.drivers[d].name).grid(row=i + 1, column=3, sticky=EW)
            Button(master=label_frame, text="Открыть", command=lambda ci=i: self.open(ci)).grid(row=i + 1, column=4,
                                                                                                sticky=E)
            Button(master=label_frame, text="Изменить", command=lambda ci=i: self.upd(ci)).grid(row=i + 1, column=5,
                                                                                                sticky=E)
            Button(master=label_frame, text="Удалить", command=lambda ci=i: self._delete(ci)).grid(row=i + 1, column=6,
                                                                                                   sticky=E)
        label_frame.grid(row=0, column=0, sticky=NSEW)
        Button(master=self, text='Назад', command=self.back).grid(row=1, column=0, sticky=SW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label_frame.grid_columnconfigure(1, weight=1)
        label_frame.grid_columnconfigure(2, weight=1)
        label_frame.grid_columnconfigure(3, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.back)

    def back(self):
        self.frame.deiconify()
        self.destroy()

    def upd(self, i):
        top = Toplevel(self)
        Label(top, text="Статус").pack()
        status_list = Listbox(top)
        for item in self.database.statuses:
            status_list.insert(END, self.database.statuses[item])
        status_list.pack()

        Button(top, text="Обновить статус",
               command=lambda: self._update_status(i, status_list.get(status_list.curselection()))).pack()
        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def open(self, i):
        top = Toplevel(self)
        Label(top, text='Идентификатор:' + self.database.orders[i].id).pack()
        Label(top, text='Статус:' + self.database.orders[i].status).pack()
        label_frame = LabelFrame(top, text="Товары")
        for item in self.database.products:
            if item.id in self.database.orders[i].products:
                Label(label_frame, text=item.name).pack()
        label_frame.pack()
        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def add(self):
        top = Toplevel(self)

        Label(top, text="Идентификатор").pack()
        id_entry = Entry(top)
        id_entry.pack()

        products_list = Listbox(top, selectmode="multiple")
        for item in self.database.products:
            products_list.insert(END, item.name)
        products_list.pack()
        products = []
        for selected in products_list.curselection():
            products.append(products_list.get(selected))

        Button(top, text="Добавить заказ",
               command=lambda: self._create(id_entry.get(), products_list.curselection())).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def _create(self, i, indexes):
        product_ids = []
        for i in indexes:
            product_ids.append(str(self.database.products[i].id))

        self.database.orders.append(Order('product:' + str(i) + ':' + 'created:' + ','.join(product_ids)))
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _update_status(self, i, status):
        self.database.orders[i].status = status
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _delete(self, i):
        self.database.orders.pop(i)
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

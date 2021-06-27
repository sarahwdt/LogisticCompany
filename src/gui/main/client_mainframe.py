from tkinter import Label, Button, Listbox, Toplevel, END, Entry, LabelFrame, messagebox, E, EW, W, NSEW, NS

from src.database.entity.order import Order
from src.gui.main.mainframe import MainFrame


class ClientMainFrame(MainFrame):
    def __init__(self, frame, database, user, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, screenName, baseName, className, useTk, sync, use)
        self.frame = frame
        Button(self, text="Добавить", command=self.add).grid(row=0, column=1, sticky=NS)
        label_frame = LabelFrame(self, text="Заказы")
        Label(master=label_frame, text="id", borderwidth=2, relief="solid").grid(row=0, column=0, sticky=E)
        Label(master=label_frame, text="Статус", borderwidth=2, relief="solid").grid(row=0, column=1, sticky=EW)
        Label(master=label_frame, text="Опции", borderwidth=2, relief="solid").grid(row=0, column=2, columnspan=2,
                                                                                    sticky=EW)

        for i in range(len(database.orders)):
            if database.orders[i].id in user.orders:
                Label(master=label_frame, text=database.orders[i].id).grid(row=i + 1, column=0, sticky=E)
                Label(master=label_frame, text=database.orders[i].status).grid(row=i + 1, column=1, sticky=EW)
                Button(master=label_frame, text="Открыть", command=lambda ci=i: self.open(ci)).grid(row=i + 1, column=2,
                                                                                                    sticky=W)
                Button(master=label_frame, text="Отменить", command=lambda ci=i: self.cancel(ci)).grid(row=i + 1,
                                                                                                       column=3,
                                                                                                       sticky=W)
        label_frame.grid(row=0, column=0, sticky=NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label_frame.grid_columnconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.back)

    def back(self):
        self.frame.deiconify()
        self.destroy()

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
               command=lambda: self.create(id_entry.get(), products_list.curselection())).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def create(self, i, indexes):
        product_ids = []
        for pi in indexes:
            product_ids.append(str(self.database.products[pi].id))

        self.database.orders.append(
            Order('product:' + str(i) + ':' + self.database.statuses['created'] + ':' + ','.join(product_ids)))
        for ci in range(len(self.database.clients)):
            if self.database.clients[ci].id == self.user.id:
                self.database.clients[ci].orders.append(str(i))
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user)

    def cancel(self, i):
        self.database.orders[i].status = self.database.statuses["canceled"]
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user)

    def delete(self, i):
        self.database.orders.pop(i)
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.database, self.user)

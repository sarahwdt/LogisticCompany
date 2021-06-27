from tkinter import Label, Button, Toplevel, END, Entry, messagebox, LabelFrame, EW, W, E, NSEW, SW, NS

from src.database.entity.product import Product
from src.gui.main.mainframe import MainFrame


class ProductsMainFrame(MainFrame):
    def __init__(self, frame, database, user, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, screenName, baseName, className, useTk, sync, use)
        self.frame = frame
        Button(self, text="Добавить", command=self.add).grid(row=0, column=1, sticky=NS)
        label_frame = LabelFrame(self, text="Продукты")
        Label(master=label_frame, text="id", borderwidth=2, relief="solid").grid(row=0, column=0, sticky=E)
        Label(master=label_frame, text="Название", borderwidth=2, relief="solid").grid(row=0, column=1, sticky=EW)
        Label(master=label_frame, text="Опции", borderwidth=2, relief="solid").grid(row=0, column=2, columnspan=3,
                                                                                    sticky=EW)
        for i in range(len(database.products)):
            Label(master=label_frame, text=database.products[i].id).grid(row=i + 1, column=0, sticky=W)
            Label(master=label_frame, text=database.products[i].name).grid(row=i + 1, column=1, sticky=EW)
            Button(master=label_frame, text="Открыть", command=lambda ci=i: self.open(ci)).grid(row=i + 1, column=2,
                                                                                                sticky=E)
            Button(master=label_frame, text="Изменить", command=lambda ci=i: self.upd(ci)).grid(row=i + 1, column=3,
                                                                                                sticky=E)
            Button(master=label_frame, text="Удалить", command=lambda ci=i: self._delete(ci)).grid(row=i + 1, column=4,
                                                                                                   sticky=E)
        label_frame.grid(row=0, column=0, sticky=NSEW)
        Button(master=self, text='Назад', command=self.back).grid(row=1, column=0, sticky=SW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label_frame.grid_columnconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.back)

    def back(self):
        self.frame.deiconify()
        self.destroy()

    def open(self, i):
        top = Toplevel(self)
        Label(top, text='Идентификатор:' + self.database.products[i].id).pack()
        Label(top, text='Название:' + self.database.products[i].name).pack()
        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def upd(self, i):
        top = Toplevel(self)
        Label(top, text="Идентификатор:" + self.database.products[i].id).pack()
        Label(top, text="Название").pack()
        name_entry = Entry(top)
        name_entry.insert(END, self.database.products[i].name)
        name_entry.pack()

        Button(top, text="Обновить", command=lambda: self._upd(i, name_entry.get())).pack()
        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def add(self):
        top = Toplevel(self)
        Label(top, text="Идентификатор").pack()
        id_entry = Entry(top)
        id_entry.pack()
        Label(top, text="Название").pack()
        name_entry = Entry(top)
        name_entry.pack()

        Button(top, text="Добавить", command=lambda: self._create(id_entry.get(), name_entry.get())).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def _create(self, new_id, name):
        self.database.products.append(Product('product:' + new_id + ':' + name))
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _upd(self, i, name):
        self.database.products[i].name = name
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _delete(self, i):
        self.database.products.pop(i)
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

from tkinter import Label, Button, Toplevel, END, Entry, LabelFrame, messagebox, E, EW, W, NSEW, SW, NS

from src.database.entity.client import Client
from src.database.entity.manager import Manager
from src.gui.main.mainframe import MainFrame


class UsersMainFrame(MainFrame):
    def __init__(self, frame, database, user, screenName=None, baseName=None, className='Tk', useTk=1, sync=0,
                 use=None):
        super().__init__(database, user, screenName, baseName, className, useTk, sync, use)
        self.frame = frame
        Button(self, text="Добавить", command=self.add).grid(row=0, column=1, sticky=NS)
        label_frame = LabelFrame(self, text="Клиенты")
        Label(master=label_frame, text="id", borderwidth=2, relief="solid").grid(row=0, column=0, sticky=E)
        Label(master=label_frame, text="Логин", borderwidth=2, relief="solid").grid(row=0, column=1, sticky=EW)
        Label(master=label_frame, text="Опции", borderwidth=2, relief="solid").grid(row=0, column=2, columnspan=3,
                                                                                    sticky=EW)
        for i in range(len(database.clients)):
            Label(master=label_frame, text=database.clients[i].id).grid(row=i + 1, column=0, sticky=W)
            Label(master=label_frame, text=database.clients[i].login).grid(row=i + 1, column=1, sticky=EW)
            Button(master=label_frame, text="Открыть", command=lambda ci=i: self.open(ci)).grid(row=i + 1, column=2,
                                                                                                sticky=E)
            Button(master=label_frame, text="Изменить", command=lambda ci=i: self.upd(ci)).grid(row=i + 1, column=3,
                                                                                                sticky=E)
            Button(master=label_frame, text="Удалить", command=lambda ci=i: self._delete(ci)).grid(row=i + 1, column=4,
                                                                                                   sticky=E)
        label_frame.grid(row=0, column=0, sticky=NSEW)
        Button(self, text="Добавить", command=self.add_m).grid(row=1, column=1, sticky=NS)
        label_frame2 = LabelFrame(self, text="Менеджеры")
        Label(master=label_frame2, text="id", borderwidth=2, relief="solid").grid(row=0, column=0, sticky=E)
        Label(master=label_frame2, text="Логин", borderwidth=2, relief="solid").grid(row=0, column=1, sticky=EW)
        Label(master=label_frame2, text="Опции", borderwidth=2, relief="solid").grid(row=0, column=2, columnspan=3,
                                                                                     sticky=EW)
        for i in range(len(database.managers)):
            Label(master=label_frame2, text=database.managers[i].id).grid(row=i + 1, column=0, sticky=W)
            Label(master=label_frame2, text=database.managers[i].login).grid(row=i + 1, column=1, sticky=EW)
            Button(master=label_frame2, text="Открыть", command=lambda ci=i: self.open_m(ci)).grid(row=i + 1, column=2,
                                                                                                   sticky=E)
            Button(master=label_frame2, text="Изменить", command=lambda ci=i: self.upd_m(ci)).grid(row=i + 1, column=3,
                                                                                                   sticky=E)
            if user.id != database.managers[i].id:
                Button(master=label_frame2, text="Удалить", command=lambda ci=i: self._delete_m(ci)).grid(row=i + 1,
                                                                                                          column=4,
                                                                                                          sticky=E)
        label_frame2.grid(row=1, column=0, sticky=NSEW)
        Button(master=self, text='Назад', command=self.back).grid(row=2, column=0, sticky=SW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        label_frame.grid_columnconfigure(1, weight=1)
        label_frame2.grid_columnconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.back)

    def back(self):
        self.frame.deiconify()
        self.destroy()

    def add(self):
        top = Toplevel(self)

        Label(top, text="Идентификатор").pack()
        id_entry = Entry(top)
        id_entry.pack()

        Label(top, text="Логин").pack()
        login_entry = Entry(top)
        login_entry.pack()

        Button(top, text="Добавить",
               command=lambda: self._create(id_entry.get(), login_entry.get())).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def add_m(self):
        top = Toplevel(self)

        Label(top, text="Идентификатор").pack()
        id_entry = Entry(top)
        id_entry.pack()

        Label(top, text="Логин").pack()
        login_entry = Entry(top)
        login_entry.pack()

        Button(top, text="Добавить",
               command=lambda: self._create_m(id_entry.get(), login_entry.get())).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def upd(self, i):
        top = Toplevel(self)
        Label(top, text="Логин").pack()
        login_entry = Entry(top)
        login_entry.insert(END, self.database.clients[i].login)
        login_entry.pack()

        Button(top, text="Обновить", command=lambda: self._upd(i, login_entry.get())).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def upd_m(self, i):
        top = Toplevel(self)
        Label(top, text="Логин").pack()
        login_entry = Entry(top)
        login_entry.insert(END, self.database.managers[i].login)
        login_entry.pack()

        Button(top, text="Обновить", command=lambda: self._upd_m(i, login_entry.get())).pack()

        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def open(self, i):
        top = Toplevel(self)
        Label(top, text='Идентификатор:' + self.database.clients[i].id).pack()
        Label(top, text='Логин:' + self.database.clients[i].login).pack()
        label_frame = LabelFrame(top, text="Заказы")
        for item in self.database.orders:
            if item.id in self.database.clients[i].orders:
                Label(label_frame, text=item.id).pack()
        label_frame.pack()
        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def open_m(self, i):
        top = Toplevel(self)
        Label(top, text='Идентификатор:' + self.database.managers[i].id).pack()
        Label(top, text='Логин:' + self.database.managers[i].login).pack()
        top.transient(self)
        top.grab_set()
        top.focus_set()
        top.wait_window()

    def _create(self, i, login):
        self.database.clients.append(Client('client:' + str(i) + ':' + login + ':'))
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _create_m(self, i, login):
        self.database.managers.append(Manager('manager:' + str(i) + ':' + login + ':'))
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _upd(self, i, login):
        self.database.clients[i].login = login
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _upd_m(self, i, login):
        self.database.managers[i].login = login
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _delete(self, i):
        self.database.clients.pop(i)
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

    def _delete_m(self, i):
        self.database.managers.pop(i)
        error = self.database.validate()
        if error is not None:
            messagebox.showerror("Ошибка", error)
        else:
            self.database.save()
            self.destroy()
            self.__init__(self.frame, self.database, self.user)

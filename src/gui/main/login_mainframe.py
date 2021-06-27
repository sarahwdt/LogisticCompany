from tkinter import Tk, Label, Button, Entry, messagebox

from src.gui.main.client_mainframe import ClientMainFrame
from src.gui.main.manager_mainframe import ManagerMainFrame


class LoginMainFrame(Tk):
    def __init__(self, database, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry('400x100+600+400')
        self.title("Автомобильные перевозки")
        self.database = database
        self.loginLabel = Label(master=self, text='Логин').pack()
        self.loginEntry = Entry(master=self)
        self.loginEntry.pack()
        self.loginButton = Button(master=self, text='Войти', command=self.login).pack()
        self.user = ''

    def login(self):
        for client in self.database.clients:
            if client.login == self.loginEntry.get():
                self.user = client
                self.showClientWindow()
        for manager in self.database.managers:
            if manager.login == self.loginEntry.get():
                self.user = manager
                self.showManagerWindow()
        messagebox.showinfo(title="Пользователь не найден",
                            message="Пользователь c логином \"" + self.loginEntry.get() + "\" не найден")

    def showManagerWindow(self):
        self.withdraw()
        ManagerMainFrame(frame=self, database=self.database, user=self.user).mainloop()

    def showClientWindow(self):
        self.withdraw()
        ClientMainFrame(frame=self, database=self.database, user=self.user).mainloop()

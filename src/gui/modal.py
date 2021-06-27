from tkinter import Toplevel


class Modal(Toplevel):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.transient(master)
        self.grab_set()
        self.focus_set()
        self.wait_window()

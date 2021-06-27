from tkinter import Tk


class MainFrame(Tk):
    def __init__(self, database, user, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.database = database
        self.user = user

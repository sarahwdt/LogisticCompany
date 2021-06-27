from src.database.core.database import Database
from src.gui.main.login_mainframe import LoginMainFrame

database = Database("C:/Users/nastya/Desktop/db.txt")

if __name__ == '__main__':
    LoginMainFrame(database).mainloop()

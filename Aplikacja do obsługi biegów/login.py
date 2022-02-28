import sys
from time import daylight
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog

import mysql.connector

from utils.mysql_data import HOST, DATABASE, ADMIN_NAME, ADMIN_PASSWORD
from utils.message_boxes import CriticalMessageBox
from utils.error_messages import DATABASE_ERROR_MSG

from admin import AdminWindow
from register import RegisterWindow
from runner import RunnerWindow

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('./qt_layouts/login.ui', self)

        self.setWindowTitle('Logowanie')

        self.database_error_box = CriticalMessageBox(text=DATABASE_ERROR_MSG)
        self.database = None

        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_button.clicked.connect(self.login_slot)
        self.register_button.clicked.connect(self.register_slot)

        self.register_window = RegisterWindow()
        self.admin_window = AdminWindow()
        self.runner_window = RunnerWindow()

    def login_slot(self):
        # Check if line edits are empty
        login_text = self.login_line_edit.text()
        password_text = self.password_line_edit.text()
        login_error_box = QtWidgets.QMessageBox()
        login_error_box.setWindowTitle("Błąd logowania")
        login_error_box.setIcon(QtWidgets.QMessageBox.Critical)

        if login_text == '' or password_text == '':
            # Error while logging in
            login_error_box.setText("Podano nieprawidłowy login lub hasło")
            login_error_box.exec_()
        
        try:
            self.database = mysql.connector.connect(
                host=HOST, 
                user=login_text, 
                password=password_text, 
                database=DATABASE)

            print('Connection was successful')
        except Exception as e:
            print(e)
            login_error_box.setText("Uzytkownik o podanych danych nie istnieje")
            login_error_box.exec_()
            return 

        if login_text == ADMIN_NAME:
            self.admin_window.set_database(self.database)
            self.admin_window.show()
        else:
            self.runner_window.set_pesel(login_text)
            self.runner_window.set_database(self.database)
            self.runner_window.set_user_data()
            self.runner_window.show()

        self.close()

    def register_slot(self):
        try:
            creator_database = mysql.connector.connect(
                host=HOST, 
                user=ADMIN_NAME, 
                password=ADMIN_PASSWORD)

            print('Connection was successful')
        except Exception as e:
            print(e)
            self.database_error_box.exec_()
            return 

        print('register')
        self.register_window.set_database(creator_database)
        self.register_window.show()
    
if __name__ == "__main__":
    app = QApplication([])
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
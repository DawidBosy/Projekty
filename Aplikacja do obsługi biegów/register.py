import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget
from utils.message_boxes import CriticalMessageBox, SuccessMessageBox

class RegisterWindow(QWidget):
    def __init__(self, modifying=False, parent=None):
        super().__init__(parent)
        uic.loadUi('./qt_layouts/register.ui', self)

        self.setWindowTitle('Rejestracja')

        self.database = None
        self.modifying = modifying

        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
            
        if modifying:
            self.register_button.setText('Zmodyfikuj')
            self.pesel_line_edit.setEnabled(False)
            self.password_line_edit.setEnabled(False)
            self.confirm_password_line_edit.setEnabled(False)

        self.register_button.clicked.connect(self.register_slot)

    def set_database(self, database):
        self.database = database

    def closeEvent(self, event):
        print('Closing database...')
        self.database.close()
        event.accept()

    def setup_initial_values(self, init_data):
        self.name_line_edit.setText(init_data['firstname'])
        self.lastname_line_edit.setText(init_data['lastname'])
        self.date_edit.setDate(QtCore.QDate.fromString(init_data['birth_date'], 'dd-mm-yyyy'))
        self.pesel_line_edit.setText(init_data['pesel'])
        self.gender_combo_box.setCurrentText(init_data['gender'])
        self.height_line_edit.setText(init_data['height'])
        self.weight_line_edit.setText(init_data['weight'])
        self.phone_line_edit.setText(init_data['phone'])
        self.city_line_edit.setText(init_data['city'])
        self.address_line_edit.setText(init_data['address'])

    def register_slot(self):
        register_error_box = QtWidgets.QMessageBox()
        register_error_box.setIcon(QtWidgets.QMessageBox.Critical)

        name = self.name_line_edit.text()
        lastname = self.lastname_line_edit.text()
        date = self.date_edit.date().toPyDate()
        pesel = self.pesel_line_edit.text()
        gender = self.gender_combo_box.currentText()
        height = self.height_line_edit.text()
        weight = self.weight_line_edit.text()
        phone = self.phone_line_edit.text()
        city = self.city_line_edit.text()
        address = self.address_line_edit.text()
        password = self.password_line_edit.text()
        confirm_password = self.confirm_password_line_edit.text()

        # Check if none of attributes are empty
        for line_edit in self.findChildren(QtWidgets.QLineEdit):
            if line_edit.text() == '':
                if self.modifying and line_edit.objectName() in ['password_line_edit', 'confirm_password_line_edit']:
                    continue
                register_error_box.setText("Zadne z pól nie moze zostac puste")
                register_error_box.exec_()
                return
        
        # Check if password was entered correctly
        if password != confirm_password:
            register_error_box.setText("Podano dwa rózne hasła")
            register_error_box.exec_()
            return

        # Check length of pesel
        if len(pesel) != 11 or not pesel.isdigit():
            register_error_box.setText("PESEL musi być ciągiem 11 cyfr")
            register_error_box.exec_()
            return

        # Check if height of weight are integers
        if not (height.isdigit() and weight.isdigit()):
            error_box = CriticalMessageBox(text='Wzrost i waga muszą być liczbami naturalnymi')
            error_box.exec_()
            return

        # Register user
        if not self.modifying:
            create_query = (
                "CREATE USER '{}'@'%' "
                "IDENTIFIED BY '{}';"
            ).format(pesel, password)

            insert_person_query = (
                "INSERT INTO runeventapp.Osoba VALUES ('{}', '{}', '{}', '{}', STR_TO_DATE('{}', '%Y-%m-%d'), '{}', '{}', '{}')"
            ).format(pesel, name, lastname, gender, date, phone, address, city)

            insert_runner_query = (
                "INSERT INTO runeventapp.Zawodnik VALUES ('{}', '{}', '{}', NULL, NULL)"
            ).format(pesel, height, weight)

            grant_queries = [
                "GRANT ALL PRIVILEGES ON runeventapp.osoba  TO '{}'@'%';".format(pesel),
                "GRANT ALL PRIVILEGES ON runeventapp.zawodnik  TO '{}'@'%';".format(pesel),
                "GRANT ALL PRIVILEGES ON runeventapp.klub  TO '{}'@'%';".format(pesel),
                "GRANT ALL PRIVILEGES ON runeventapp.uczestnictwo  TO '{}'@'%';".format(pesel),
                "GRANT SELECT ON runeventapp.* TO '{}'@'%';".format(pesel)
            ]

            cursor = self.database.cursor()

            try:
                print(create_query)
                cursor.execute(create_query)
                print(insert_person_query)
                cursor.execute(insert_person_query)
                print(insert_runner_query)
                cursor.execute(insert_runner_query)
                
                for grant_query in grant_queries:
                    print(grant_query)
                    cursor.execute(grant_query)

                self.database.commit()
            except Exception as e:
                if str(e).startswith('1396'):
                    error_box = CriticalMessageBox(text='Uzytkownik o podanym peselu juz istnieje')
                    error_box.exec_()
                else:
                    print(e)

                return

            # Notify user about successful registration
            register_error_box.setIcon(QtWidgets.QMessageBox.Information)
            register_error_box.setText("Rejestracja powiodła się!")
            register_error_box.exec_()
        # Modify user
        else:
            update_personal_info_query = (
                "UPDATE runeventapp.Osoba "
                "SET imie = '{}', nazwisko = '{}', plec = '{}', data_urodzenia = STR_TO_DATE('{}', '%Y-%m-%d'), "
                "nr_telefonu = '{}', adres = '{}', miejscowosc = '{}' "
                "WHERE pesel = '{}'"
            ).format(name, lastname, gender, date, phone, address, city, pesel)

            update_runner_info_query = (
                "UPDATE runeventapp.Zawodnik "
                "SET wzrost = {}, waga = {} "
                "WHERE pesel = '{}'"
            ).format(height, weight, pesel)

            print(update_personal_info_query)
            print(update_runner_info_query)

            cursor = self.database.cursor()

            try:
                cursor.execute(update_personal_info_query)
                print(update_personal_info_query)
                cursor.execute(update_runner_info_query)
                print(update_runner_info_query)

                self.database.commit()
            except Exception as e:
                print(e)
                return

            # Notify user about successful registration
            register_error_box.setIcon(QtWidgets.QMessageBox.Information)
            register_error_box.setText("Modyfikacja powiodła się!")
            register_error_box.exec_()

        self.database.close()
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    win = RegisterWindow()
    win.show()
    sys.exit(app.exec())
from dataclasses import dataclass
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QTabWidget, QTableWidget, QTableWidgetItem
from utils.message_boxes import CriticalMessageBox, SuccessMessageBox, WarningMessageBox
from utils.error_messages import EMPTY_FIELDS_MSG

from utils.mysql_data import HOST, DATABASE, ADMIN_NAME, ADMIN_PASSWORD
import mysql.connector
from mysql.connector import errorcode

from register import RegisterWindow

class RunnerWindow(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('./qt_layouts/runner.ui', self)

        self.setWindowTitle('Biegacz')

        self.user_data = {
            'firstname': '',
            'lastname': '',
            'pesel': '',
            'gender': '',
            'birth_date': '',
            'phone': '',
            'address': '',
            'city': '',
            'height': '',
            'weight': '',
            'club': '',
            'category': ''
        }

        self.database = None

        self.modify_user_data_button.clicked.connect(self.modify_user_data_slot)
        self.modify_window = RegisterWindow(modifying=True)

        self.currentChanged.connect(self.on_tab_change)

        self.join_club_button.clicked.connect(self.join_club_slot)
        self.club_combo_box.activated.connect(self.load_club_slot)

        self.start_run_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_run_date.setDateTime(QtCore.QDateTime.currentDateTime())

        self.search_run_button.clicked.connect(self.search_for_runs)
        self.sign_up_button.clicked.connect(self.sign_up_for_run)

        self.search_run_table.horizontalHeader().setVisible(True)

        self.user_runs_table.horizontalHeader().setVisible(True)

        self.run_refresh_button.clicked.connect(self.load_user_runs)

        self.start_run_date.dateChanged.connect(self.check_date)
        self.end_run_date.dateChanged.connect(self.check_date)
        self.min_distance_spin_box.valueChanged.connect(self.check_distance)
        self.max_distance_spin_box.valueChanged.connect(self.check_distance)

    def check_date(self):
        start_date = self.start_run_date.date()
        end_date = self.end_run_date.date()

        if start_date > end_date:
            date_warning_box = WarningMessageBox(text='Startowa data nie moze być wcześniejsza od końcowej daty')
            date_warning_box.exec_()
            self.start_run_date.setDate(min(start_date, end_date))
            self.end_run_date.setDate(min(start_date, end_date))

    def check_distance(self):
        min_dis = self.min_distance_spin_box.value()
        max_dis = self.max_distance_spin_box.value()

        if min_dis > max_dis:
            distance_warning_box = WarningMessageBox(text='Minimalny dystans nie moze być większy od maksymalnego dystansu')
            distance_warning_box.exec_()
            self.min_distance_spin_box.setValue(min(min_dis, max_dis))
            self.max_distance_spin_box.setValue(min(min_dis, max_dis))

    def load_club_names(self):
        club_select_query = (
            "SELECT nazwa FROM Klub"
        )

        cursor = self.database.cursor()
        cursor.execute(club_select_query)
        club_names = [club_name for club_name, in cursor.fetchall()]
        print(club_names)
        self.club_combo_box.clear()
        self.club_combo_box.addItems(club_names)

    def on_tab_change(self, i):
        if i == 3:
            self.load_club_names()

    def load_club_slot(self):
        club_name = self.club_combo_box.currentText()

        club_data_query = (
            "SELECT zalozyciel, data_powstania, miejscowosc "
            "FROM Klub "
            "WHERE nazwa = '{}'"
        ).format(club_name)

        cursor = self.database.cursor()

        try:
            cursor.execute(club_data_query)
            founder, date, city = cursor.fetchone()
            year, month, day = [int(x) for x in str(date).split('-')]
            date = '{:02d}/{:02d}/{}'.format(day, month, year)

            self.club_founder_label.setText(founder)
            self.club_date_label.setText(date)
            self.club_city_label.setText(city)

        except Exception as e:
            print(e)

        cursor.close()

    def set_database(self, database):
        self.database = database
        self.load_club_names()
        self.load_club_slot()
        self.load_user_runs()

    def set_pesel(self, pesel):
        self.user_data['pesel'] = pesel

    def set_user_data(self):
        pesel = self.user_data['pesel']
    
        personal_data_query = (
            "SELECT imie, nazwisko, plec, data_urodzenia, nr_telefonu, adres, miejscowosc "
            "FROM Osoba "
            "WHERE pesel = '{}'"
        ).format(pesel)

        runner_data_query = (
            "SELECT wzrost, waga, kl.nazwa, ka.wiek_min, ka.wiek_max "
            "FROM zawodnik z "
            "LEFT JOIN klub kl on z.klub_id_klubu = kl.id_klubu "
            "LEFT JOIN kategoria ka on z.kategoria_id_kategoria = ka.id_kategoria "
            "WHERE z.pesel = '{}'"
        ).format(pesel) 

        cursor = self.database.cursor()

        try:
            cursor.execute(personal_data_query)
            firstname, lastname, gender, birth_date, phone, address, city = cursor.fetchone()

            cursor.execute(runner_data_query)
            height, weight, club, category_min_age, category_max_age = cursor.fetchone()

            club = '' if club == None else club
            category = '' if category_min_age == category_max_age == None else '{}-{}'.format(category_min_age, category_max_age)

            year, month, day = [int(x) for x in str(birth_date).split('-')]
            birth_date = '{}-{}-{}'.format(day, month, year)

            self.user_data = {
                'pesel': pesel,
                'firstname': firstname,
                'lastname': lastname,
                'gender': gender,
                'birth_date': birth_date,
                'phone': phone,
                'address': address,
                'city': city,
                'height': str(height),
                'weight': str(weight),
                'club': club,
                'category': category
            }

            print(self.user_data)

            self.set_user_labels()

        except Exception as e:
            print(e)

        cursor.close()

    def get_user_data(self):
        return self.user_data

    def set_user_labels(self):
        print(self.user_data)

        self.user_name_label.setText(self.user_data['firstname'] + ' ' + self.user_data['lastname'])
        self.pesel_label.setText(self.user_data['pesel'])
        self.gender_label.setText(self.user_data['gender'])
        self.birth_date_label.setText(self.user_data['birth_date'])
        self.phone_label.setText(self.user_data['phone'])
        self.address_label.setText(self.user_data['address'])
        self.city_label.setText(self.user_data['city'])
        self.height_label.setText(self.user_data['height'])
        self.weight_label.setText(self.user_data['weight'])
        self.club_label.setText(self.user_data['club'])
        self.category_label.setText(self.user_data['category'])

    def modify_user_data_slot(self):
        try:
            creator_database = mysql.connector.connect(
                host=HOST, 
                user=ADMIN_NAME, 
                password=ADMIN_PASSWORD)

            print('Connection was successful')
        except Exception as e:
            print(e)
            return 

        self.modify_window.set_database(creator_database)
        self.modify_window.setup_initial_values(init_data=self.get_user_data())
        self.modify_window.show()

    def join_club_slot(self):
        club_name = self.club_combo_box.currentText()

        id_club_subquery = (
            "SELECT id_klubu FROM Klub "
            "WHERE nazwa = '{}'"
        ).format(club_name)

        join_club_query = (
            "UPDATE Zawodnik "
            "SET klub_id_klubu = ({}) "
            "WHERE pesel = '{}'"
        ).format(id_club_subquery, self.user_data['pesel'])

        cursor = self.database.cursor()

        try:
            cursor.execute(join_club_query)
            self.database.commit()
            self.set_user_data()
        except Exception as e:
            print(e)
            cursor.close()
            return

        if cursor.rowcount == 0:
            join_club_warning_box = WarningMessageBox(text='Juz jesteś członkiem tego klubu')
            join_club_warning_box.exec_()
        else:
            join_club_success_box = SuccessMessageBox(text='Dołaczono do klubu!')
            join_club_success_box.exec_()

        cursor.close()

    def search_for_runs(self):
        start_date = self.start_run_date.date().toPyDate()
        end_date = self.end_run_date.date().toPyDate()
        min_distance = self.min_distance_spin_box.value()
        max_distance = self.max_distance_spin_box.value()

        select_run_query = (
            "SELECT b.nazwa_biegu, w.data_wydarzenia, b.data_biegu, b.dystans, b.rodzaj " 
            "FROM Bieg b JOIN Wydarzenie w ON b.wydarzenie_id_wydarzenia = w.id_wydarzenia "
            "WHERE dystans BETWEEN {} AND {} "
            "AND data_biegu BETWEEN CAST('{}' AS DATE) AND CAST('{}' AS DATE)"
        ).format(min_distance, max_distance, start_date, end_date)

        cursor = self.database.cursor()

        try:
            cursor.execute(select_run_query)
            runs_data = [row for row in cursor.fetchall()]

            if runs_data == []:
                none_found_box = WarningMessageBox(text='Nie znaleziono żadnego biegu')
                none_found_box.exec_()
            else:
                self.insert_into_table(runs_data)
        except Exception as e:
            print(e)

        cursor.close()

    def insert_into_table(self, runs_data):
        table = self.search_run_table

        for row in range(table.rowCount() - 1, -1, -1):
            table.removeRow(row)

        for i, row in enumerate(runs_data):
            name, date, time, distance, type = row
            year, month, day = [int(x) for x in str(date).split('-')]
            date = '{:02d}/{:02d}/{}'.format(day, month, year)

            hour, minutes, _ = [int(x) for x in str(time).split(':')]
            time = '{:02d}:{:02d}'.format(hour, minutes)

            print(name, date, distance, type)

            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(name))
            table.setItem(i, 1, QTableWidgetItem(date))
            table.setItem(i, 2, QTableWidgetItem(time))
            table.setItem(i, 3, QTableWidgetItem(str(distance)))
            table.setItem(i, 4, QTableWidgetItem(type))

    def sign_up_for_run(self):
        table = self.search_run_table

        if table.selectionModel().selectedRows() == []:
            none_selected_box = WarningMessageBox(text='Nie wybrano żadnego biegu')
            none_selected_box.exec_()
            return

        run_name = table.selectionModel().selectedRows()[0].data()
        
        run_id_subquery = (
            "SELECT id_biegu "
            "FROM Bieg "
            "WHERE nazwa_biegu = '{}'"
        ).format(run_name)

        event_id_subquery = (
            "SELECT wydarzenie_id_wydarzenia "
            "FROM Bieg "
            "WHERE nazwa_biegu = '{}'"
        ).format(run_name)

        insert_run_query = (
            "INSERT INTO Uczestnictwo (zawodnik_pesel, bieg_id_biegu, bieg_id_wydarzenia) "
            "VALUES ('{}', ({}), ({}))"
        ).format(self.user_data['pesel'], run_id_subquery, event_id_subquery)
        
        cursor = self.database.cursor()

        try:
            cursor.execute(insert_run_query)
            self.database.commit()
            join_run_success_box = SuccessMessageBox(text='Dołączono do biegu!')
            join_run_success_box.exec_()
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                error_run_join_box = CriticalMessageBox(text='Juz dołączyłeś do tego biegu')
                error_run_join_box.exec_()
            else:
                print(e)

        cursor.close()

    def insert_into_user_table(self, user_runs_data):
        table = self.user_runs_table

        for row in range(table.rowCount() - 1, -1, -1):
            table.removeRow(row)

        for i, row in enumerate(user_runs_data):
            name, event_date, run_time, distance, type, time, place = row

            year, month, day = [int(x) for x in str(event_date).split('-')]
            event_date = '{:02d}/{:02d}/{}'.format(day, month, year)
  
            hour, minutes, _ = [int(x) for x in str(run_time).split(':')]

            run_time = '{:02d}:{:02d}'.format(hour, minutes)

            place = '-' if place is None else str(place)
            time = '-' if time is None else str(time)

            print(name, event_date, distance, type, time, place)

            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(name))
            table.setItem(i, 1, QTableWidgetItem(event_date))
            table.setItem(i, 2, QTableWidgetItem(run_time))
            table.setItem(i, 3, QTableWidgetItem(str(distance)))
            table.setItem(i, 4, QTableWidgetItem(type))
            table.setItem(i, 5, QTableWidgetItem(time))
            table.setItem(i, 6, QTableWidgetItem(place))

    def load_user_runs(self):
        user_runs_query = (
            "SELECT b.nazwa_biegu, w.data_wydarzenia, b.data_biegu, b.dystans, b.rodzaj, u.czas, u.zajete_miejsce "
            "FROM uczestnictwo u "
	        "JOIN bieg b on u.bieg_id_biegu = b.id_biegu "
	        "JOIN wydarzenie w on u.bieg_id_wydarzenia = w.id_wydarzenia "
            "WHERE u.zawodnik_pesel = '{}'"
        ).format(self.user_data['pesel'])

        cursor = self.database.cursor()

        try:
            cursor.execute(user_runs_query)
            user_runs_data = [row for row in cursor.fetchall()]
            self.insert_into_user_table(user_runs_data)
        except Exception as e:
            print(e)

        cursor.close()

if __name__ == "__main__":
    app = QApplication([])
    win = RunnerWindow()
    win.show()
    sys.exit(app.exec())
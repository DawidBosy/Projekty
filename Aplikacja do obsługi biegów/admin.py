import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QTabWidget, QTableWidget, QTableWidgetItem
from utils.message_boxes import CriticalMessageBox, WarningMessageBox, SuccessMessageBox
from utils.error_messages import EMPTY_FIELDS_MSG, INSERT_ERROR_MSG, MODIFY_ERROR_MSG, MODIFY_WARNING_MSG, DELETE_ERROR_MSG

import mysql.connector
from utils.mysql_data import HOST, ADMIN_NAME, ADMIN_PASSWORD, DATABASE

class AdminWindow(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('./qt_layouts/admin.ui', self)

        self.setWindowTitle('Admin')

        self.empty_field_error_box = CriticalMessageBox(text=EMPTY_FIELDS_MSG)
        self.insert_error_box = CriticalMessageBox(text=INSERT_ERROR_MSG)
        self.modify_error_box = CriticalMessageBox(text=MODIFY_ERROR_MSG)
        self.modify_warning_box = WarningMessageBox(text=MODIFY_WARNING_MSG)
        self.delete_error_box = CriticalMessageBox(text=DELETE_ERROR_MSG)
        self.success_box = SuccessMessageBox(text='Operacja powiodła się!')

        self.database = None

        self.AddTabWidget.currentChanged.connect(self.on_sub_tab_change)
        self.ModifyTabWidget.currentChanged.connect(self.on_modify_tab_change)
        self.currentChanged.connect(self.on_main_tab_change)

        self.run_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.date_time_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.event_date_modify_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.run_modify_date_edit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.event_add_button.clicked.connect(self.event_add_slot)
        self.run_add_button.clicked.connect(self.run_add_slot)
        self.sponsor_add_button.clicked.connect(self.sponsor_add_slot)
        self.time_add_button.clicked.connect(self.time_add_slot)
        self.time_delete_button.clicked.connect(self.time_delete_slot)
        self.club_add_button.clicked.connect(self.club_add_slot)

        self.event_modify_button.clicked.connect(self.event_modify_slot)
        self.event_delete_button.clicked.connect(self.event_delete_slot)
        self.run_modify_button.clicked.connect(self.run_modify_slot)
        self.run_delete_button.clicked.connect(self.run_delete_slot)
        self.sponsor_modify_button.clicked.connect(self.sponsor_modify_slot)
        self.sponsor_delete_button.clicked.connect(self.sponsor_delete_slot)
        self.view_combo_box.activated.connect(self.load_view_data)

        self.run_modify_event_combo_box.activated.connect(self.load_run_names_for_run_modify)
        self.run_name_combo_box.activated.connect(self.load_run_data_for_run_modify)
        self.event_modify_combo_box.activated.connect(self.load_event_data_for_event_modify)
        self.sponsor_modify_company_combo_box.activated.connect(self.load_event_names_for_sponsor_modify)
        self.sponsor_modify_event_combo_box.activated.connect(self.load_event_data_for_sponsor_modify)

        self.company_add_button.clicked.connect(self.company_add_slot)
        self.company_modify_button.clicked.connect(self.company_modify_slot)
        self.company_delete_button.clicked.connect(self.company_delete_slot)

        self.company_name_combo_box.activated.connect(self.load_company_data_for_company_modify)

        def dragEnterEvent(event):
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()

        def dragMoveEvent(event):
            if event.mimeData().hasUrls:
                event.setDropAction(QtCore.Qt.CopyAction)
                event.accept()
            else:
                event.ignore()

        def dropEvent(event):
            files = [u.toLocalFile() for u in event.mimeData().urls()]

            try:
                for file in files:
                    with open(file, 'r') as f:
                        for i, row in enumerate(f.readlines()):
                            if row == '' or row == '\n': 
                                continue
                            pesel, time, place = row[:-1].split()
                            print(pesel, time, place)
                            self.run_time_table.insertRow(i)
                            self.run_time_table.setItem(i, 0, QTableWidgetItem(pesel))
                            self.run_time_table.setItem(i, 1, QTableWidgetItem(time))
                            self.run_time_table.setItem(i, 2, QTableWidgetItem(place))
            except Exception as e:
                print(e)
                file_format_warning = WarningMessageBox(text='Błędny format pliku')
                file_format_warning.exec_()
                for row in range(self.run_time_table.rowCount() - 1, -1, -1):
                    self.run_time_table.removeRow(row)

        self.run_time_table.dragEnterEvent = dragEnterEvent
        self.run_time_table.dragMoveEvent = dragMoveEvent
        self.run_time_table.dropEvent = dropEvent

    def load_event_data_for_event_modify(self):
        event_name = self.event_modify_combo_box.currentText()
        
        select_event_data_query = (
            "SELECT organizator, data_wydarzenia "
            "FROM Wydarzenie "
            "WHERE nazwa = '{}'"
        ).format(event_name)

        cursor = self.database.cursor()
        cursor.execute(select_event_data_query)
        organizer, event_date = cursor.fetchone()

        self.organizer_modify_line_edit.setText(organizer)

        year, month, day = [int(x) for x in str(event_date).split('-')]
        self.event_date_modify_edit.setDate(QtCore.QDate(year, month, day))

    def load_run_names_for_view(self):
        cursor = self.database.cursor()

        select_table_names_query = (
            "SHOW TABLES"
        )

        cursor = self.database.cursor()

        cursor.execute(select_table_names_query)

        table_names = [table_name for table_name, in cursor.fetchall()]

        self.view_combo_box.clear()
        self.view_combo_box.addItems(table_names)

        cursor.close()

    def on_main_tab_change(self, i):
        if i == 2:
            self.load_run_names_for_view()
            self.load_view_data()

    def load_event_names_for_run_add(self):
        cursor = self.database.cursor()
        select_event_query = (
                "SELECT nazwa FROM Wydarzenie;"
        )

        cursor.execute(select_event_query)

        event_names = [event_name for event_name, in cursor.fetchall()]

        self.event_combo_box.clear()
        self.event_combo_box.addItems(event_names)

        cursor.close()

    def load_run_names_for_time_add(self):
        cursor = self.database.cursor()

        select_run_query = (
            "SELECT nazwa_biegu FROM Bieg;"
        )

        cursor.execute(select_run_query)

        run_names = [run_name for run_name, in cursor.fetchall()]

        self.run_combo_box.clear()
        self.run_combo_box.addItems(run_names)

        cursor.close()

    def load_company_name_for_sponsor_add(self):
        cursor = self.database.cursor()

        select_company_query = (
            "SELECT nazwa FROM Firma;"
        )

        cursor.execute(select_company_query)

        company_names = [company_name for company_name, in cursor.fetchall()]

        self.company_combo_box.clear()
        self.company_combo_box.addItems(company_names)

        select_event_query = (
            "SELECT nazwa FROM Wydarzenie;"
        )

        cursor.execute(select_event_query)

        event_names = [event_name for event_name, in cursor.fetchall()]

        self.event_combo_box_2.clear()
        self.event_combo_box_2.addItems(event_names)

        cursor.close()

    def load_event_names_for_sponsor_add(self):
        cursor = self.database.cursor()

        select_event_query = (
            "SELECT nazwa FROM Wydarzenie;"
        )

        cursor.execute(select_event_query)

        event_names = [event_name for event_name, in cursor.fetchall()]

        self.event_combo_box_2.clear()
        self.event_combo_box_2.addItems(event_names)

        cursor.close()

    def on_sub_tab_change(self, i):
        cursor = self.database.cursor()

        # Bieg
        if i == 0:
            self.load_event_names_for_run_add()
        # Czas
        elif i == 1:
            self.load_run_names_for_time_add()
        # Sponsor
        elif i == 4:
            self.load_company_name_for_sponsor_add()
            self.load_event_names_for_sponsor_add()
        
        cursor.close()

    def load_event_names_for_event_modify(self):
        cursor = self.database.cursor()

        select_event_name_query = (
            "SELECT nazwa FROM Wydarzenie;"
        )

        cursor.execute(select_event_name_query)

        event_names = [event_name for event_name, in cursor.fetchall()]

        self.event_modify_combo_box.clear()
        self.event_modify_combo_box.addItems(event_names)

        cursor.close()

    def load_event_names_for_run_modify(self):
        cursor = self.database.cursor()

        select_event_name_query = (
            "SELECT nazwa FROM Wydarzenie;"
        )

        cursor.execute(select_event_name_query)

        event_names = [event_name for event_name, in cursor.fetchall()]

        self.run_modify_event_combo_box.clear()
        self.run_modify_event_combo_box.addItems(event_names)

        cursor.close()

    def load_company_names_for_sponsor_modify(self):
        cursor = self.database.cursor()

        select_company_name_query = (
            "SELECT nazwa FROM Firma;"
        )

        cursor.execute(select_company_name_query)

        company_names = [company_name for company_name, in cursor.fetchall()]

        self.sponsor_modify_company_combo_box.clear()
        self.sponsor_modify_company_combo_box.addItems(company_names)

        cursor.close()

    def load_company_names_for_company_modify(self):
        cursor = self.database.cursor()

        select_company_name_query = (
            "SELECT nazwa FROM Firma;"
        )

        cursor.execute(select_company_name_query)

        company_names = [company_name for company_name, in cursor.fetchall()]

        self.company_name_combo_box.clear()
        self.company_name_combo_box.addItems(company_names)

    def on_modify_tab_change(self, i):
        cursor = self.database.cursor()

        if i == 0:
            self.load_event_names_for_run_modify()
            self.load_run_data_for_run_modify()
        elif i == 1:
            self.load_company_names_for_company_modify()
            self.load_company_data_for_company_modify()
        elif i == 2:
            self.load_company_names_for_sponsor_modify()
            self.load_event_names_for_sponsor_modify()
            self.load_event_data_for_sponsor_modify()
        elif i == 3:
            self.load_event_names_for_event_modify()
            self.load_event_data_for_event_modify()

        cursor.close()

    def set_database(self, database):
        self.database = database

        # Init all combo boxes with values
        self.load_event_names_for_run_add()
        self.load_run_names_for_time_add()
        self.load_company_name_for_sponsor_add()
        self.load_event_names_for_sponsor_add()

        self.load_event_names_for_run_modify()
        self.load_run_names_for_run_modify()
        self.load_run_data_for_run_modify()

        self.load_company_names_for_company_modify()
        self.load_company_data_for_company_modify()

        self.load_company_names_for_sponsor_modify()
        self.load_event_names_for_sponsor_modify()
        self.load_event_data_for_sponsor_modify()

        self.load_event_names_for_event_modify()
        self.load_event_data_for_event_modify()

        self.load_run_names_for_view()
        self.load_view_data()

    def closeEvent(self, event):
        print('Closing database...')
        self.database.close()
        event.accept()

    def event_add_slot(self):
        event_name = self.event_line_edit.text()
        organizer_name =  self.organizer_line_edit.text()
        event_date = self.date_time_edit.date().toPyDate()

        if event_name == '' or organizer_name == '':
            self.empty_field_error_box.exec_()
            return

        cursor = self.database.cursor()

        event_select_query = "SELECT * FROM Wydarzenie WHERE nazwa = '{}'".format(event_name)

        print(event_select_query)

        cursor.execute(event_select_query)
        event_rows = cursor.fetchall()

        if event_rows != []:
            event_error_box = CriticalMessageBox(text='Wydarzenie o takiej nazwie juz istnieje!')
            event_error_box.exec_()
            return

        event_add_query = (
        "INSERT INTO Wydarzenie (nazwa, organizator, data_wydarzenia) VALUES ('{}', '{}', STR_TO_DATE('{}', '%Y-%m-%d'))"
        ).format(event_name, organizer_name, event_date)

        try:
            cursor.execute(event_add_query)
            self.database.commit()
        except Exception as e:
            print(e)
            self.insert_error_box.exec_()
            cursor.close()
            return

        self.success_box.exec_()
        cursor.close()

        print(event_add_query)

    def run_add_slot(self):
        event_name = self.event_combo_box.currentText()
        run_name = self.run_name_line_edit.text()
        run_datetime = str(self.run_time_edit.time().toPyTime())
        distance_value = self.distance_spin_box.value()
        run_type = self.type_line_edit.text()

        run_datetime = run_datetime[:run_datetime.rfind(':')]

        print(run_datetime)

        if event_name == '' or run_name == '' or run_type == '':
            self.empty_field_error_box.exec_()
            return

        # TODO: Check if run already exists
        cursor = self.database.cursor()

        run_select_query = (
            "SELECT * FROM Bieg b, Wydarzenie w "
            "WHERE b.wydarzenie_id_wydarzenia = w.id_wydarzenia "
            "AND b.nazwa_biegu = '{}' AND w.nazwa = '{}'"
        ).format(run_name, event_name)
        
        print(run_select_query)

        cursor.execute(run_select_query)
        run_rows = cursor.fetchall()

        if run_rows != []:
            run_error_box = CriticalMessageBox(text='Bieg o takiej nazwie w wybranym wydarzeniu juz istnieje!')
            run_error_box.exec_()
            return

        event_id_subquery = (
            "SELECT id_wydarzenia FROM Wydarzenie "
            "WHERE nazwa = '{}'").format(event_name)

        run_add_query= (
            "INSERT INTO Bieg (dystans, rodzaj, data_biegu, wydarzenie_id_wydarzenia, nazwa_biegu) "
            "VALUES ({}, '{}', '{}', ({}), '{}')"
        ).format(distance_value, run_type, run_datetime, event_id_subquery, run_name)

        try:
            print(run_add_query)
            cursor.execute(run_add_query)
            self.database.commit()
        except Exception as e:
            print(e)
            self.insert_error_box.exec_()
            cursor.close()
            return

        self.success_box.exec_()
        cursor.close()

        print(run_add_query)

    def sponsor_add_slot(self):
        company_name = self.company_combo_box.currentText()
        event_name = self.event_combo_box_2.currentText()
        amount_value = self.amount_spin_box.value()

        if company_name == '' or event_name == '':
            self.empty_field_error_box.exec_()
            return

        company_subquery = (
        "SELECT id_firmy from Firma "
        "WHERE nazwa = '{}'").format(company_name)

        event_subquery = (
        "SELECT id_wydarzenia from Wydarzenie "
        "WHERE nazwa = '{}'").format(event_name)

        sponsoring_query = (
            "INSERT INTO Sponsoring VALUES ({}, ({}), ({}))"
        ).format(amount_value, event_subquery, company_subquery)

        cursor = self.database.cursor()

        try:
            cursor.execute(sponsoring_query)
            self.database.commit()
        except Exception as e:
            print(e)
            error_box = CriticalMessageBox(text='Wybrane wydarzenie jest juz sponosorowane przez tę firmę')
            error_box.exec_()
            cursor.close()
            return

        self.success_box.exec_()
        cursor.close()

        print(sponsoring_query)

    def time_add_slot(self):
        table = self.run_time_table
        run_name = self.run_combo_box.currentText()
        
        if table.rowCount() == 0:
            error_box = CriticalMessageBox(window_title='Błąd', text='Nie dodano danych')
            error_box.exec_()
            return

        cursor = self.database.cursor()

        invalid_pesels = set()
        updated_pesels = set()

        run_subquery = (
            "SELECT id_biegu, wydarzenie_id_wydarzenia "
            "FROM Bieg "
            "WHERE nazwa_biegu = '{}'"
        ).format(run_name)

        try:
            cursor.execute(run_subquery)
            id_run, id_event = cursor.fetchall()[0]

            count_rows = 0

            for row in range(table.rowCount()):
                pesel = table.item(row, 0).text()
                time = table.item(row, 1).text()
                place = table.item(row, 2).text()

                # time_query = (
                #     "INSERT INTO Uczestnictwo VALUES (STR_TO_DATE('{}', '%h:%i:%s'), {}, '{}', {}, {})"
                # ).format(time, place, pesel, id_run, id_event)

                time_update_query = (
                    "UPDATE Uczestnictwo "
                    "SET czas = STR_TO_DATE('{}', '%h:%i:%s'), zajete_miejsce = {} "
                    "WHERE zawodnik_pesel = '{}' AND bieg_id_biegu = {} AND bieg_id_wydarzenia = {}"
                ).format(time, place, pesel, id_run, id_event)

                
                cursor.execute(time_update_query)

                if cursor.rowcount == 1:
                    updated_pesels.add(pesel)
                elif cursor.rowcount == 0:
                    invalid_pesels.add(pesel)
                else:
                    print('dodano: {}'.format(cursor.rowcount))

                print(time_update_query)
                count_rows += 1

            self.database.commit()
            cursor.close()
        except Exception as e:
            print(e)
            self.insert_error_box.exec_()
            cursor.close()
            return

        if invalid_pesels == set():
            self.success_box.exec_()
        elif updated_pesels == set() and invalid_pesels != set():
            error_box = CriticalMessageBox(text='Rekordy nie zostały zmodyfikowane')
            error_box.exec_()
        elif updated_pesels != set() and invalid_pesels != set():
            warning_box = WarningMessageBox(text='Dodano dane dla: {}\nBłąd dla danych: {}'.format(updated_pesels, invalid_pesels))
            warning_box.exec_()

        for row in range(table.rowCount() - 1, -1, -1):
            table.removeRow(row)

    def time_delete_slot(self):
        table = self.run_time_table

        for row in range(table.rowCount() - 1, -1, -1):
            table.removeRow(row)

    def club_add_slot(self):
        name = self.club_name_line_edit.text()
        founder = self.founder_line_edit.text()
        city = self.city_line_edit.text()

        if name == '' or founder == '' or city == '':
            self.empty_field_error_box.exec_()
            return

        cursor = self.database.cursor()

        club_select_query = (
            "SELECT * FROM Klub "
            "WHERE nazwa = '{}' "
        ).format(name)
        
        print(club_select_query)

        cursor.execute(club_select_query)
        club_rows = cursor.fetchall()

        if club_rows != []:
            club_error_box = CriticalMessageBox(text='Klub o takiej nazwie juz istnieje!')
            club_error_box.exec_()
            cursor.close()
            return

        club_query = (
            "INSERT INTO Klub (nazwa, zalozyciel, data_powstania, miejscowosc) VALUES ('{}', '{}', curdate(),'{}')"
        ).format(name, founder, city)

        try:
            cursor = self.database.cursor()
            cursor.execute(club_query)
            self.database.commit()
            cursor.close()
        except Exception as e:
            print(e)
            self.insert_error_box.exec_()
            cursor.close()
            return

        print(club_query)

        self.success_box.exec_()

    def event_modify_slot(self):
        event_name = self.event_modify_combo_box.currentText()
        organizer_name = self.organizer_modify_line_edit.text()
        event_date = self.event_date_modify_edit.text()

        if event_name == '' or organizer_name == '' or event_date == '':
            self.empty_field_error_box.exec_()
            return

        day, month, year = event_date.split('/')
        event_date = '{}-{}-{}'.format(year, month, day)

        event_modify_query = (
            "UPDATE Wydarzenie "
            "SET organizator = '{}', data_wydarzenia = '{}' "
            "WHERE nazwa = '{}'"
        ).format(organizer_name, event_date, event_name)

        cursor = self.database.cursor()

        try:
            cursor.execute(event_modify_query)
            self.database.commit()
            print(event_modify_query)
        except Exception as e:
            self.modify_error_box.exec_()
            print(e)

        if cursor.rowcount == 0:
            self.modify_warning_box.exec_()
        else:
            self.success_box.exec_()

        cursor.close()

    def event_delete_slot(self):
        event_name = self.event_modify_combo_box.currentText()
  
        if event_name == '':
            self.empty_field_error_box.exec_()
            return

        event_delete_query = (
            "DELETE FROM Wydarzenie "
            "WHERE nazwa = '{}'"
        ).format(event_name)

        cursor = self.database.cursor()

        try:
            cursor.execute(event_delete_query)
            self.database.commit()
            print(event_delete_query)
            self.success_box.exec_()
            
            select_event_name_query = (
                "SELECT nazwa FROM Wydarzenie;"
            )

            cursor.execute(select_event_name_query)

            event_names = [event_name for event_name, in cursor.fetchall()]

            self.load_event_names_for_event_modify()
            self.load_event_data_for_event_modify()
        except Exception as e:
            self.delete_error_box.exec_()
            print(e)

        cursor.close()

    def load_run_names_for_run_modify(self):
        event_name = self.run_modify_event_combo_box.currentText()

        event_id_subquery = (
            "SELECT id_wydarzenia "
            "FROM Wydarzenie "
            "WHERE nazwa = '{}'"
        ).format(event_name)
        
        print(event_id_subquery)

        select_run_query = (
            "SELECT nazwa_biegu "
            "FROM Bieg "
            "WHERE wydarzenie_id_wydarzenia = ({})"
        ).format(event_id_subquery)

        print(select_run_query)

        cursor = self.database.cursor()

        try:
            cursor.execute(select_run_query)
            run_names = [run_name for run_name, in cursor.fetchall()]
            self.run_name_combo_box.clear()
            self.run_name_combo_box.addItems(run_names)
            cursor.close()

            self.load_run_data_for_run_modify()
        except Exception as e:
            print(e)

        cursor.close()

    def load_run_data_for_run_modify(self):
        run_name = self.run_name_combo_box.currentText()

        select_run_data_query = (
            "SELECT dystans, rodzaj, data_biegu "
            "FROM Bieg "
            "WHERE nazwa_biegu = '{}'"
        ).format(run_name)

        print(select_run_data_query)

        cursor = self.database.cursor()

        try:
            cursor.execute(select_run_data_query)
            distance, type, date = cursor.fetchone()
            
            self.distance_spin_box_2.setValue(distance)
            self.run_type_line_edit.setText(type)

            hour, minutes, _ = [int(x) for x in str(date).split(':')]
            self.run_modify_date_edit.setTime(QtCore.QTime(hour, minutes))

        except Exception as e:
            print(e)

        cursor.close()

    def run_modify_slot(self):
        event_name = self.run_modify_event_combo_box.currentText()
        run_name = self.run_name_combo_box.currentText()
        run_date = self.run_modify_date_edit.text()
        run_distance = self.distance_spin_box_2.value()
        run_type = self.run_type_line_edit.text()

        if event_name == '' or run_name == '' or run_date == '' or run_distance == '' or run_type == '':
            self.empty_field_error_box.exec_()
            return

        hour, minutes = run_date.split(':')
        run_date = '{}:{}'.format(hour, minutes)

        run_modify_query = (
            "UPDATE Bieg "
            "SET dystans = {}, rodzaj = '{}', data_biegu = '{}' "
            "WHERE nazwa_biegu = '{}'"
        ).format(run_distance, run_type, run_date, run_name)

        print(run_modify_query)

        cursor = self.database.cursor()

        try:
            cursor.execute(run_modify_query)
            self.database.commit()
            print(run_modify_query)
        except Exception as e:
            self.modify_error_box.exec_()
            print(e)

        if cursor.rowcount == 0:
            self.modify_warning_box.exec_()
        else:
            self.success_box.exec_()

        cursor.close()
            
    def run_delete_slot(self):
        run_name = self.run_name_combo_box.currentText()

        if run_name == '':
            self.empty_field_error_box.exec_()
            return

        run_delete_query = (
            "DELETE FROM Bieg "
            "WHERE nazwa_biegu = '{}'"
        ).format(run_name)

        cursor = self.database.cursor()

        try:
            cursor.execute(run_delete_query)
            self.database.commit()
            print(run_delete_query)
            self.success_box.exec_()
            
            self.load_run_names_for_run_modify()
            self.load_run_data_for_run_modify()
        except Exception as e:
            self.delete_error_box.exec_()
            print(e)

        cursor.close()

    def load_event_names_for_sponsor_modify(self):
        company_name = self.sponsor_modify_company_combo_box.currentText()
        
        giga_query = (
            "select w.nazwa from wydarzenie w, sponsoring s, firma f "
            "where w.id_wydarzenia = s.wydarzenie_id_wydarzenia and s.firma_id_firmy = f.id_firmy and f.nazwa = '{}'"
        ).format(company_name)

        cursor = self.database.cursor()

        try:
            cursor.execute(giga_query)
            event_names = [event_name for event_name, in cursor.fetchall()]

            self.sponsor_modify_event_combo_box.clear()
            self.sponsor_modify_event_combo_box.addItems(event_names)

            self.load_event_data_for_sponsor_modify()
        except Exception as e:
            print(e)

        cursor.close()

    def load_event_data_for_sponsor_modify(self):
        company_name = self.sponsor_modify_company_combo_box.currentText()
        event_name = self.sponsor_modify_event_combo_box.currentText()

        company_id_subquery = (
            "SELECT id_firmy "
            "FROM Firma "
            "WHERE nazwa = '{}'"
        ).format(company_name)

        event_id_subquery = (
            "SELECT id_wydarzenia "
            "FROM Wydarzenie "
            "WHERE nazwa = '{}'"
        ).format(event_name)

        amount_query = (
            "SELECT kwota "
            "FROM Sponsoring "
            "WHERE wydarzenie_id_wydarzenia = ({}) AND firma_id_firmy = ({})"
        ).format(event_id_subquery, company_id_subquery)

        cursor = self.database.cursor()

        try:
            cursor.execute(amount_query)
            amount, = cursor.fetchone()
            amount = int(amount)
            self.sponsor_modify_amount_spin_box.setValue(amount)
        except Exception as e:
            print(e)

        cursor.close()

    def sponsor_modify_slot(self):
        sponsor_name = self.sponsor_modify_company_combo_box.currentText()
        event_name = self.sponsor_modify_event_combo_box.currentText()
        amount = self.sponsor_modify_amount_spin_box.value()

        id_event_query = (
            "SELECT id_wydarzenia "
            "FROM Wydarzenie "
            "WHERE nazwa = '{}'"
        ).format(event_name)

        id_sponsor_query = (
            "SELECT id_firmy "
            "FROM Firma "
            "WHERE nazwa = '{}'"
        ).format(sponsor_name)

        sponsor_modify_query = (
            "UPDATE Sponsoring "
            "SET kwota = {} "
            "WHERE wydarzenie_id_wydarzenia = ({}) AND firma_id_firmy = ({})"
        ).format(amount, id_event_query, id_sponsor_query)

        cursor = self.database.cursor()

        try:
            cursor.execute(sponsor_modify_query)
            self.database.commit()
            print(sponsor_modify_query)
        except Exception as e:
            self.modify_error_box.exec_()
            print(e)

        if cursor.rowcount == 0:
            self.modify_warning_box.exec_()
        else:
            self.success_box.exec_()

        cursor.close()

    def sponsor_delete_slot(self):
        sponsor_name = self.sponsor_modify_company_combo_box.currentText()
        event_name = self.sponsor_modify_event_combo_box.currentText()

        id_event_query = (
            "SELECT id_wydarzenia "
            "FROM Wydarzenie "
            "WHERE nazwa = '{}'"
        ).format(event_name)

        id_sponsor_query = (
            "SELECT id_firmy "
            "FROM Firma "
            "WHERE nazwa = '{}'"
        ).format(sponsor_name)

        sponsor_delete_query = (
            "DELETE FROM Sponsoring "
            "WHERE wydarzenie_id_wydarzenia = ({}) AND firma_id_firmy = ({})"
        ).format(id_event_query, id_sponsor_query)

        cursor = self.database.cursor()

        try:
            cursor.execute(sponsor_delete_query)
            self.database.commit()
            print(sponsor_delete_query)
            self.success_box.exec_()
            
            self.load_company_names_for_sponsor_modify()
            self.load_event_names_for_sponsor_modify()
            self.load_event_data_for_sponsor_modify()
        except Exception as e:
            self.delete_error_box.exec_()
            print(e)

        cursor.close()

    def company_add_slot(self):
        name = self.company_name_line_edit.text()
        address = self.company_address_line_edit.text()
        email = self.company_email_line_edit.text()
        phone = self.company_phone_line_edit.text()
        ceo = self.company_ceo_line_edit.text()

        if name == '' or address == '' or email == '' or phone == '' or ceo == '':
            self.empty_field_error_box.exec_()
            return

        cursor = self.database.cursor()

        company_select_query = (
            "SELECT * FROM Firma "
            "WHERE nazwa = '{}' "
        ).format(name)
        
        print(company_select_query)

        cursor.execute(company_select_query)
        company_rows = cursor.fetchall()

        if company_rows != []:
            company_error_box = CriticalMessageBox(text='Firma o takiej nazwie juz istnieje!')
            company_error_box.exec_()
            cursor.close()
            return

        company_query = (
            "INSERT INTO Firma (nazwa, adres, email, nr_telefonu, szef) VALUES ('{}', '{}', '{}', '{}', '{}')"
        ).format(name, address, email, phone, ceo)

        try:
            cursor = self.database.cursor()
            cursor.execute(company_query)
            self.database.commit()
            cursor.close()
        except Exception as e:
            print(e)
            self.insert_error_box.exec_()
            cursor.close()
            return

        print(company_query)

        self.success_box.exec_()

    def company_modify_slot(self):
        name = self.company_name_combo_box.currentText()
        address = self.company_address_line_edit_2.text()
        email = self.company_email_line_edit_2.text()
        phone = self.company_phone_line_edit_2.text()
        ceo = self.company_ceo_line_edit_2.text()

        if name == '' or address == '' or email == '' or phone == '' or ceo == '':
            self.empty_field_error_box.exec_()
            return

        company_modify_query = (
            "UPDATE Firma "
            "SET adres = '{}', email = '{}', nr_telefonu = '{}', szef = '{}' "
            "WHERE nazwa = '{}'"
        ).format(address, email, phone, ceo, name)

        cursor = self.database.cursor()

        try:
            cursor.execute(company_modify_query)
            self.database.commit()
            print(company_modify_query)
        except Exception as e:
            self.modify_error_box.exec_()
            print(e)

        if cursor.rowcount == 0:
            self.modify_warning_box.exec_()
        else:
            self.success_box.exec_()

        cursor.close()

    def company_delete_slot(self):
        company_name = self.company_name_combo_box.currentText()

        if company_name == '':
            self.empty_field_error_box.exec_()
            return

        company_delete_query = (
            "DELETE FROM Firma "
            "WHERE nazwa = '{}'"
        ).format(company_name)

        cursor = self.database.cursor()

        try:
            cursor.execute(company_delete_query)
            self.database.commit()
            print(company_delete_query)
            self.success_box.exec_()
            
            self.load_company_names_for_company_modify()
            self.load_company_data_for_company_modify()
        except Exception as e:
            self.delete_error_box.exec_()
            print(e)

        cursor.close()

    def load_company_data_for_company_modify(self):
        name = self.company_name_combo_box.currentText()

        select_company_data_query = (
            "SELECT adres, email, nr_telefonu, szef "
            "FROM Firma "
            "WHERE nazwa = '{}'"
        ).format(name)
        
        cursor = self.database.cursor()
        cursor.execute(select_company_data_query)
        address, email, phone, ceo = cursor.fetchone()

        self.company_address_line_edit_2.setText(address)
        self.company_email_line_edit_2.setText(email)
        self.company_phone_line_edit_2.setText(phone)
        self.company_ceo_line_edit_2.setText(ceo)

    def load_view_data(self):
        select_query = (
            "SELECT * FROM {};"
        ).format(self.view_combo_box.currentText())

        try:
            cursor = self.database.cursor()
            cursor.execute(select_query)

            column_names = [i[0] for i in cursor.description]

            print(column_names)

            for row in range(self.view_table.rowCount() - 1, -1, -1):
                self.view_table.removeRow(row)

            self.view_table.setColumnCount(len(column_names))
            self.view_table.setHorizontalHeaderLabels(column_names)

            for i, row in enumerate(cursor):
                self.view_table.insertRow(i)
                for j, value in enumerate(row):
                    self.view_table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            print(e)
            self.insert_error_box.exec_()
            cursor.close()
            return          

        cursor.close()      

if __name__ == "__main__":
    app = QApplication([])

    database = mysql.connector.connect(
                host=HOST, 
                user=ADMIN_NAME, 
                password=ADMIN_PASSWORD, 
                database=DATABASE)

    win = AdminWindow()
    win.set_database(database)
    win.show()
    sys.exit(app.exec())
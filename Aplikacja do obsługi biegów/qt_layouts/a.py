# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_layouts/admin.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_adminWindow(object):
    def setupUi(self, adminWindow):
        adminWindow.setObjectName("adminWindow")
        adminWindow.resize(595, 415)
        self.add_tab = QtWidgets.QWidget()
        self.add_tab.setObjectName("add_tab")
        self.AddTabWidget = QtWidgets.QTabWidget(self.add_tab)
        self.AddTabWidget.setGeometry(QtCore.QRect(20, 0, 541, 381))
        self.AddTabWidget.setTabsClosable(False)
        self.AddTabWidget.setMovable(False)
        self.AddTabWidget.setTabBarAutoHide(False)
        self.AddTabWidget.setObjectName("AddTabWidget")
        self.event_add_tab = QtWidgets.QWidget()
        self.event_add_tab.setObjectName("event_add_tab")
        self.layoutWidget = QtWidgets.QWidget(self.event_add_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 60, 281, 194))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.event_line_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.event_line_edit.setObjectName("event_line_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.event_line_edit)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.organizer_line_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.organizer_line_edit.setObjectName("organizer_line_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.organizer_line_edit)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.date_edit = QtWidgets.QDateEdit(self.layoutWidget)
        self.date_edit.setObjectName("date_edit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.date_edit)
        self.verticalLayout.addLayout(self.formLayout)
        self.event_add_button = QtWidgets.QPushButton(self.layoutWidget)
        self.event_add_button.setObjectName("event_add_button")
        self.verticalLayout.addWidget(self.event_add_button)
        self.event_add_button.raise_()
        self.AddTabWidget.addTab(self.event_add_tab, "")
        self.run_add_tab = QtWidgets.QWidget()
        self.run_add_tab.setObjectName("run_add_tab")
        self.layoutWidget1 = QtWidgets.QWidget(self.run_add_tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(140, 60, 239, 194))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.event_combo_box = QtWidgets.QComboBox(self.layoutWidget1)
        self.event_combo_box.setObjectName("event_combo_box")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.event_combo_box)
        self.label_24 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_24.setObjectName("label_24")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_24)
        self.run_name_line_edit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.run_name_line_edit.setObjectName("run_name_line_edit")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.run_name_line_edit)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.date_time_edit = QtWidgets.QDateTimeEdit(self.layoutWidget1)
        self.date_time_edit.setObjectName("date_time_edit")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.date_time_edit)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.type_combo_box = QtWidgets.QComboBox(self.layoutWidget1)
        self.type_combo_box.setObjectName("type_combo_box")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.type_combo_box)
        self.distance_spin_box = QtWidgets.QSpinBox(self.layoutWidget1)
        self.distance_spin_box.setMinimum(1)
        self.distance_spin_box.setMaximum(100)
        self.distance_spin_box.setObjectName("distance_spin_box")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.distance_spin_box)
        self.verticalLayout_3.addLayout(self.formLayout_3)
        self.run_add_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.run_add_button.setObjectName("run_add_button")
        self.verticalLayout_3.addWidget(self.run_add_button)
        self.AddTabWidget.addTab(self.run_add_tab, "")
        self.sponsor_add_tab = QtWidgets.QWidget()
        self.sponsor_add_tab.setObjectName("sponsor_add_tab")
        self.layoutWidget_3 = QtWidgets.QWidget(self.sponsor_add_tab)
        self.layoutWidget_3.setGeometry(QtCore.QRect(130, 90, 251, 141))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.company_combo_box = QtWidgets.QComboBox(self.layoutWidget_3)
        self.company_combo_box.setObjectName("company_combo_box")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.company_combo_box)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.event_combo_box_2 = QtWidgets.QComboBox(self.layoutWidget_3)
        self.event_combo_box_2.setObjectName("event_combo_box_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.event_combo_box_2)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.amount_spin_box = QtWidgets.QSpinBox(self.layoutWidget_3)
        self.amount_spin_box.setMaximum(1000000)
        self.amount_spin_box.setSingleStep(100)
        self.amount_spin_box.setProperty("value", 1000)
        self.amount_spin_box.setObjectName("amount_spin_box")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.amount_spin_box)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.sponsor_add_button = QtWidgets.QPushButton(self.layoutWidget_3)
        self.sponsor_add_button.setObjectName("sponsor_add_button")
        self.verticalLayout_2.addWidget(self.sponsor_add_button)
        self.AddTabWidget.addTab(self.sponsor_add_tab, "")
        self.time_add_tab = QtWidgets.QWidget()
        self.time_add_tab.setObjectName("time_add_tab")
        self.layoutWidget2 = QtWidgets.QWidget(self.time_add_tab)
        self.layoutWidget2.setGeometry(QtCore.QRect(120, 30, 321, 271))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.run_combo_box = QtWidgets.QComboBox(self.layoutWidget2)
        self.run_combo_box.setObjectName("run_combo_box")
        self.horizontalLayout.addWidget(self.run_combo_box)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.run_time_table = QtWidgets.QTableWidget(self.layoutWidget2)
        self.run_time_table.setDragEnabled(True)
        self.run_time_table.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.run_time_table.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.run_time_table.setObjectName("run_time_table")
        self.run_time_table.setColumnCount(3)
        self.run_time_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.run_time_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.run_time_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.run_time_table.setHorizontalHeaderItem(2, item)
        self.run_time_table.horizontalHeader().setCascadingSectionResizes(False)
        self.run_time_table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.run_time_table)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.time_add_button = QtWidgets.QPushButton(self.layoutWidget2)
        self.time_add_button.setObjectName("time_add_button")
        self.horizontalLayout_2.addWidget(self.time_add_button)
        self.time_delete_button = QtWidgets.QPushButton(self.layoutWidget2)
        self.time_delete_button.setObjectName("time_delete_button")
        self.horizontalLayout_2.addWidget(self.time_delete_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.AddTabWidget.addTab(self.time_add_tab, "")
        self.club_add_tab = QtWidgets.QWidget()
        self.club_add_tab.setObjectName("club_add_tab")
        self.layoutWidget3 = QtWidgets.QWidget(self.club_add_tab)
        self.layoutWidget3.setGeometry(QtCore.QRect(160, 100, 225, 128))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_8.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_23 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_23.setObjectName("label_23")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_23)
        self.club_name_line_edit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.club_name_line_edit.setObjectName("club_name_line_edit")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.club_name_line_edit)
        self.label_31 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_31.setObjectName("label_31")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_31)
        self.founder_line_edit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.founder_line_edit.setObjectName("founder_line_edit")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.founder_line_edit)
        self.label_33 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_33.setObjectName("label_33")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_33)
        self.city_line_edit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.city_line_edit.setObjectName("city_line_edit")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.city_line_edit)
        self.verticalLayout_8.addLayout(self.formLayout_8)
        self.club_add_button = QtWidgets.QPushButton(self.layoutWidget3)
        self.club_add_button.setObjectName("club_add_button")
        self.verticalLayout_8.addWidget(self.club_add_button)
        self.AddTabWidget.addTab(self.club_add_tab, "")
        adminWindow.addTab(self.add_tab, "")
        self.modify_tab = QtWidgets.QWidget()
        self.modify_tab.setObjectName("modify_tab")
        self.ModifyTabWidget = QtWidgets.QTabWidget(self.modify_tab)
        self.ModifyTabWidget.setGeometry(QtCore.QRect(10, 10, 541, 381))
        self.ModifyTabWidget.setObjectName("ModifyTabWidget")
        self.event_modify_tab = QtWidgets.QWidget()
        self.event_modify_tab.setObjectName("event_modify_tab")
        self.layoutWidget4 = QtWidgets.QWidget(self.event_modify_tab)
        self.layoutWidget4.setGeometry(QtCore.QRect(150, 80, 251, 131))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_14.setObjectName("label_14")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.organizer_modify_line_edit = QtWidgets.QLineEdit(self.layoutWidget4)
        self.organizer_modify_line_edit.setObjectName("organizer_modify_line_edit")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.organizer_modify_line_edit)
        self.label_15 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_15.setObjectName("label_15")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.event_date_modify_edit = QtWidgets.QDateEdit(self.layoutWidget4)
        self.event_date_modify_edit.setObjectName("event_date_modify_edit")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.event_date_modify_edit)
        self.event_modify_combo_box = QtWidgets.QComboBox(self.layoutWidget4)
        self.event_modify_combo_box.setObjectName("event_modify_combo_box")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.event_modify_combo_box)
        self.verticalLayout_5.addLayout(self.formLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.event_modify_button = QtWidgets.QPushButton(self.layoutWidget4)
        self.event_modify_button.setObjectName("event_modify_button")
        self.horizontalLayout_3.addWidget(self.event_modify_button)
        self.event_delete_button = QtWidgets.QPushButton(self.layoutWidget4)
        self.event_delete_button.setObjectName("event_delete_button")
        self.horizontalLayout_3.addWidget(self.event_delete_button)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.ModifyTabWidget.addTab(self.event_modify_tab, "")
        self.run_modify_tab = QtWidgets.QWidget()
        self.run_modify_tab.setObjectName("run_modify_tab")
        self.layoutWidget5 = QtWidgets.QWidget(self.run_modify_tab)
        self.layoutWidget5.setGeometry(QtCore.QRect(160, 70, 229, 194))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_16 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_16.setObjectName("label_16")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.run_modify_event_combo_box = QtWidgets.QComboBox(self.layoutWidget5)
        self.run_modify_event_combo_box.setObjectName("run_modify_event_combo_box")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.run_modify_event_combo_box)
        self.label_30 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_30.setObjectName("label_30")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_30)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_17.setObjectName("label_17")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.run_modify_date_edit = QtWidgets.QDateTimeEdit(self.layoutWidget5)
        self.run_modify_date_edit.setObjectName("run_modify_date_edit")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.run_modify_date_edit)
        self.label_18 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_18.setObjectName("label_18")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.label_19 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_19.setObjectName("label_19")
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.run_type_combo_box = QtWidgets.QComboBox(self.layoutWidget5)
        self.run_type_combo_box.setObjectName("run_type_combo_box")
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.run_type_combo_box)
        self.run_name_combo_box = QtWidgets.QComboBox(self.layoutWidget5)
        self.run_name_combo_box.setObjectName("run_name_combo_box")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.run_name_combo_box)
        self.distance_spin_box_2 = QtWidgets.QSpinBox(self.layoutWidget5)
        self.distance_spin_box_2.setObjectName("distance_spin_box_2")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.distance_spin_box_2)
        self.verticalLayout_6.addLayout(self.formLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.run_modify_button = QtWidgets.QPushButton(self.layoutWidget5)
        self.run_modify_button.setObjectName("run_modify_button")
        self.horizontalLayout_4.addWidget(self.run_modify_button)
        self.run_delete_button = QtWidgets.QPushButton(self.layoutWidget5)
        self.run_delete_button.setObjectName("run_delete_button")
        self.horizontalLayout_4.addWidget(self.run_delete_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.ModifyTabWidget.addTab(self.run_modify_tab, "")
        self.sponsor_modify_tab = QtWidgets.QWidget()
        self.sponsor_modify_tab.setObjectName("sponsor_modify_tab")
        self.layoutWidget6 = QtWidgets.QWidget(self.sponsor_modify_tab)
        self.layoutWidget6.setGeometry(QtCore.QRect(170, 100, 209, 130))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget6)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_20 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_20.setObjectName("label_20")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.sponsor_modify_company_combo_box = QtWidgets.QComboBox(self.layoutWidget6)
        self.sponsor_modify_company_combo_box.setObjectName("sponsor_modify_company_combo_box")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sponsor_modify_company_combo_box)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_21.setObjectName("label_21")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.sponsor_modify_event_combo_box = QtWidgets.QComboBox(self.layoutWidget6)
        self.sponsor_modify_event_combo_box.setObjectName("sponsor_modify_event_combo_box")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sponsor_modify_event_combo_box)
        self.label_22 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_22.setObjectName("label_22")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_22)
        self.sponsor_modify_amount_spin_box = QtWidgets.QSpinBox(self.layoutWidget6)
        self.sponsor_modify_amount_spin_box.setMinimum(1000)
        self.sponsor_modify_amount_spin_box.setMaximum(1000000)
        self.sponsor_modify_amount_spin_box.setSingleStep(100)
        self.sponsor_modify_amount_spin_box.setObjectName("sponsor_modify_amount_spin_box")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sponsor_modify_amount_spin_box)
        self.verticalLayout_7.addLayout(self.formLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.sponsor_modify_button = QtWidgets.QPushButton(self.layoutWidget6)
        self.sponsor_modify_button.setObjectName("sponsor_modify_button")
        self.horizontalLayout_5.addWidget(self.sponsor_modify_button)
        self.sponsor_delete_button = QtWidgets.QPushButton(self.layoutWidget6)
        self.sponsor_delete_button.setObjectName("sponsor_delete_button")
        self.horizontalLayout_5.addWidget(self.sponsor_delete_button)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.ModifyTabWidget.addTab(self.sponsor_modify_tab, "")
        adminWindow.addTab(self.modify_tab, "")
        self.view_tab = QtWidgets.QWidget()
        self.view_tab.setObjectName("view_tab")
        self.view_combo_box = QtWidgets.QComboBox(self.view_tab)
        self.view_combo_box.setGeometry(QtCore.QRect(280, 30, 104, 26))
        self.view_combo_box.setObjectName("view_combo_box")
        self.ViewTableView = QtWidgets.QTableView(self.view_tab)
        self.ViewTableView.setGeometry(QtCore.QRect(90, 90, 411, 281))
        self.ViewTableView.setObjectName("ViewTableView")
        self.label_11 = QtWidgets.QLabel(self.view_tab)
        self.label_11.setGeometry(QtCore.QRect(190, 30, 60, 16))
        self.label_11.setObjectName("label_11")
        adminWindow.addTab(self.view_tab, "")

        self.retranslateUi(adminWindow)
        adminWindow.setCurrentIndex(2)
        self.AddTabWidget.setCurrentIndex(4)
        self.ModifyTabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(adminWindow)

    def retranslateUi(self, adminWindow):
        _translate = QtCore.QCoreApplication.translate
        adminWindow.setWindowTitle(_translate("adminWindow", "TabWidget"))
        self.label.setText(_translate("adminWindow", "Nazwa wydarzenia"))
        self.label_2.setText(_translate("adminWindow", "Organizator"))
        self.label_3.setText(_translate("adminWindow", "Data wydarzenia"))
        self.event_add_button.setText(_translate("adminWindow", "Dodaj"))
        self.AddTabWidget.setTabText(self.AddTabWidget.indexOf(self.event_add_tab), _translate("adminWindow", "Wydarzenie"))
        self.label_7.setText(_translate("adminWindow", "Wydarzenie"))
        self.label_24.setText(_translate("adminWindow", "Nazwa biegu"))
        self.label_8.setText(_translate("adminWindow", "Data startu"))
        self.label_9.setText(_translate("adminWindow", "Dystans"))
        self.label_10.setText(_translate("adminWindow", "Rodzaj"))
        self.run_add_button.setText(_translate("adminWindow", "Dodaj"))
        self.AddTabWidget.setTabText(self.AddTabWidget.indexOf(self.run_add_tab), _translate("adminWindow", "Bieg"))
        self.label_6.setText(_translate("adminWindow", "Firma"))
        self.label_4.setText(_translate("adminWindow", "Wydarzenie"))
        self.label_5.setText(_translate("adminWindow", "Kwota"))
        self.sponsor_add_button.setText(_translate("adminWindow", "Dodaj"))
        self.AddTabWidget.setTabText(self.AddTabWidget.indexOf(self.sponsor_add_tab), _translate("adminWindow", "Sponsor"))
        self.label_12.setText(_translate("adminWindow", "Bieg"))
        item = self.run_time_table.horizontalHeaderItem(0)
        item.setText(_translate("adminWindow", "PESEL"))
        item = self.run_time_table.horizontalHeaderItem(1)
        item.setText(_translate("adminWindow", "Czas"))
        item = self.run_time_table.horizontalHeaderItem(2)
        item.setText(_translate("adminWindow", "Miejsce"))
        self.time_add_button.setText(_translate("adminWindow", "Dodaj"))
        self.time_delete_button.setText(_translate("adminWindow", "Usu??"))
        self.AddTabWidget.setTabText(self.AddTabWidget.indexOf(self.time_add_tab), _translate("adminWindow", "Czas"))
        self.label_23.setText(_translate("adminWindow", "Nazwa"))
        self.label_31.setText(_translate("adminWindow", "Za??o??yciel"))
        self.label_33.setText(_translate("adminWindow", "Miejscowo????"))
        self.club_add_button.setText(_translate("adminWindow", "Dodaj"))
        self.AddTabWidget.setTabText(self.AddTabWidget.indexOf(self.club_add_tab), _translate("adminWindow", "Klub"))
        adminWindow.setTabText(adminWindow.indexOf(self.add_tab), _translate("adminWindow", "Dodaj"))
        self.label_13.setText(_translate("adminWindow", "Nazwa wydarzenia"))
        self.label_14.setText(_translate("adminWindow", "Organizator"))
        self.label_15.setText(_translate("adminWindow", "Data wydarzenia"))
        self.event_modify_button.setText(_translate("adminWindow", "Modyfikuj"))
        self.event_delete_button.setText(_translate("adminWindow", "Usu??"))
        self.ModifyTabWidget.setTabText(self.ModifyTabWidget.indexOf(self.event_modify_tab), _translate("adminWindow", "Wydarzenie"))
        self.label_16.setText(_translate("adminWindow", "Wydarzenie"))
        self.label_30.setText(_translate("adminWindow", "Nazwa biegu"))
        self.label_17.setText(_translate("adminWindow", "Data startu"))
        self.label_18.setText(_translate("adminWindow", "Dystans"))
        self.label_19.setText(_translate("adminWindow", "Rodzaj"))
        self.run_modify_button.setText(_translate("adminWindow", "Modyfikuj"))
        self.run_delete_button.setText(_translate("adminWindow", "Usu??"))
        self.ModifyTabWidget.setTabText(self.ModifyTabWidget.indexOf(self.run_modify_tab), _translate("adminWindow", "Bieg"))
        self.label_20.setText(_translate("adminWindow", "Firma"))
        self.label_21.setText(_translate("adminWindow", "Wydarzenie"))
        self.label_22.setText(_translate("adminWindow", "Kwota"))
        self.sponsor_modify_button.setText(_translate("adminWindow", "Modyfikuj"))
        self.sponsor_delete_button.setText(_translate("adminWindow", "Usu??"))
        self.ModifyTabWidget.setTabText(self.ModifyTabWidget.indexOf(self.sponsor_modify_tab), _translate("adminWindow", "Sponsor"))
        adminWindow.setTabText(adminWindow.indexOf(self.modify_tab), _translate("adminWindow", "Modyfikuj"))
        self.label_11.setText(_translate("adminWindow", "Wy??wietl"))
        adminWindow.setTabText(adminWindow.indexOf(self.view_tab), _translate("adminWindow", "Podgl??d"))

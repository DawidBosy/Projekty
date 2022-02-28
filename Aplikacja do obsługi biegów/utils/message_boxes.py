import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

class CriticalMessageBox(QMessageBox):
    def __init__(self, window_title='Błąd', text='', parent=None):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setText(text)
        self.setIcon(QMessageBox.Critical)

class WarningMessageBox(QMessageBox):
    def __init__(self, window_title='Ostrzezenie', text='', parent=None):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setText(text)
        self.setIcon(QMessageBox.Warning)

class SuccessMessageBox(QMessageBox):
    def __init__(self, window_title='Operacja powiodła się', text='', parent=None):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setText(text)
        self.setIcon(QMessageBox.Information)

if __name__ == '__main__':
    app = QApplication([])
    box = CriticalMessageBox()
    box.exec_()
    sys.exit(app.exec())
    
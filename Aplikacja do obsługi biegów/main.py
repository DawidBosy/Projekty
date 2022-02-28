import sys
from login import LoginWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
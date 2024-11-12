import sys
from PySide6 import QtWidgets

from scripts import Window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec())
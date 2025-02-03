#
# ============== TEXT FLOW ==============
# Script written by Istomin Mikhail
# Powered Developer <https://github.com/PoweredDeveloper>
#

import sys
from PySide6 import QtWidgets

from scripts import Window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(720, 480)
    window.show()

    sys.exit(app.exec())
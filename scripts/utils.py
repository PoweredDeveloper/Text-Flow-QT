from PySide6.QtGui import *
from PySide6.QtCore import *

def create_action(icon_path: str, text: str, func: object, parent: QObject, shortcut: QKeySequence | QKeyCombination | QKeySequence.StandardKey | str | int | None = None, tooltip: str = '') -> QAction:
    action = QAction(QIcon(icon_path), text, parent)
    action.setStatusTip(tooltip if tooltip != '' else text)
    if shortcut != None:
        action.setShortcut(shortcut)
    action.triggered.connect(func)
    return action
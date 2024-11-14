#
# ============== TEXT FLOW ==============
# Script written by Istomin Mikhail
# Powered Developer <https://github.com/PoweredDeveloper>
#

from PySide6.QtGui import *
from PySide6.QtCore import *

def create_action(icon_path: str,
                  text: str,
                  func: object,
                  parent: QObject,
                  shortcut: QKeySequence | QKeyCombination | QKeySequence.StandardKey | str | int | None = None,
                  tooltip: str = '',
                  checkable: bool = False,
                  checked: bool = False
                  ) -> QAction:
    action = QAction(QIcon(icon_path), text, parent)
    action.setStatusTip(tooltip if tooltip != '' else text)
    action.setCheckable(checkable)
    if shortcut != None:
        action.setShortcut(shortcut)
    
    if checkable:
        action.toggled.connect(func)
        action.setChecked(checked)
    else:
        action.triggered.connect(func)

    return action

def blockSignals(objects: list, block: bool) -> None:
    for object in objects:
        object.blockSignals(block)
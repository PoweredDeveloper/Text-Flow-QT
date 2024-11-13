from PySide6.QtWidgets import *
from PySide6.QtGui import *

class Editor(QTextEdit):
    def init(self) -> None:
        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.selectionChanged.connect(self.updateFormat)
        self.setFont(QFont('Calibri', 11))
        self.setFontPointSize(11)
    
    def updateFormat(self) -> None:
        ...

    def toggle_wrap(self) -> None:
        if self.lineWrapMode() == self.LineWrapMode.NoWrap:
            self.setLineWrapMode(self.LineWrapMode.WidgetWidth)
        else:
            self.setLineWrapMode(self.LineWrapMode.NoWrap)
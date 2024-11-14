#
# ============== TEXT FLOW ==============
# Script written by Istomin Mikhail
# Powered Developer <https://github.com/PoweredDeveloper>
#

from PySide6.QtWidgets import *
from PySide6.QtGui import *

from .utils import blockSignals

class Editor(QTextEdit):
    def init(self, actions: dict, text_update_funcs: list[object]) -> None:
        self.interact_actions = actions 
        self.text_update_funcs = text_update_funcs

        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.setLineWrapMode(self.LineWrapMode.WidgetWidth)

        self.clear_styles()

        self.selectionChanged.connect(self.updateFormat)
        self.textChanged.connect(self.handleTextChanges)
    
    def updateFormat(self) -> None:
        actions = list(self.interact_actions.values())
        blockSignals(actions, True)

        self.interact_actions['font_picker'].setCurrentFont(self.currentFont())
        self.interact_actions['font_size'].setCurrentText(str(int(self.fontPointSize())))
        
        self.interact_actions['bold_action'].setChecked(self.fontWeight() == QFont.Weight.Bold)
        self.interact_actions['italic_action'].setChecked(self.fontItalic())
        self.interact_actions['underline_action'].setChecked(self.fontUnderline())

        self.interact_actions['align_left'].setChecked(self.alignment() == Qt.AlignmentFlag.AlignLeft)
        self.interact_actions['align_center'].setChecked(self.alignment() == Qt.AlignmentFlag.AlignCenter)
        self.interact_actions['align_right'].setChecked(self.alignment() == Qt.AlignmentFlag.AlignRight)
        self.interact_actions['align_justify'].setChecked(self.alignment() == Qt.AlignmentFlag.AlignJustify)

        blockSignals(actions, False)

    def setAlignment(self, a) -> None:
        super().setAlignment(a)
        self.updateFormat()

    def handleTextChanges(self) -> None:
        if self.fontPointSize() == 0.0:
            self.setFontPointSize(float(int(self.interact_actions['font_size'].currentText())))

        for func in self.text_update_funcs:
            func()

    def clear_styles(self) -> None:
        self.selectAll()
        self.setFont(QFont('Calibri', 11))
        print('cleared')
        self.setFontPointSize(11)
        self.setTextColor(QColor('#000000'))
        self.setTextBackgroundColor(QColor('#ffffff'))
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setFontWeight(QFont.Weight.Normal)
        self.setFontItalic(False)
        self.setFontUnderline(False)

    def toggle_wrap(self) -> None:
        if self.lineWrapMode() == self.LineWrapMode.NoWrap:
            self.setLineWrapMode(self.LineWrapMode.WidgetWidth)
        else:
            self.setLineWrapMode(self.LineWrapMode.NoWrap)
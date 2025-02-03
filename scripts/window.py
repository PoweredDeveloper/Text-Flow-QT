#
# ============== TEXT FLOW ==============
# Script written by Istomin Mikhail
# Powered Developer <https://github.com/PoweredDeveloper>
#

import webbrowser
import re

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtPrintSupport import *
from .paths import *
from .editor import Editor
from .utils import create_action

FONT_SIZES = [8, 9, 10, 11, 12, 14, 16, 18, 24, 36, 48, 72]

class Window(QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()

        # Initializing Window
        self.path = ''
        self.saved = False

        self.setWindowIcon(QIcon(APP_ICON))
        self.update_title()

        self.editor = Editor()
        self.initUI()

        actions = {
            'bold_action': self._actions['edit']['bold'],
            'italic_action': self._actions['edit']['italic'],
            'underline_action': self._actions['edit']['underline'],
            'align_left': self._actions['edit']['align_left'],
            'align_center': self._actions['edit']['align_center'],
            'align_right': self._actions['edit']['align_right'],
            'align_justify': self._actions['edit']['align_justify'],
            'font_picker': self._font_picker,
            'font_size': self._font_size
        }

        self.editor.init(actions, [self.update_footer])

        self.editor.updateFormat()

        # Layout
        self.setCentralWidget(QWidget())
        main_layout = QGridLayout()

        main_layout.addWidget(self.editor, 0, 0, 1, 2)
        main_layout.addLayout(self.footer(), 1, 0, 1, 2)

        main_layout.setColumnStretch(0, 3)
        main_layout.setColumnStretch(1, 1)
        self.centralWidget().setLayout(main_layout)

    def initUI(self) -> None:
        self._actions: dict[str, dict[str, QAction]] = {
            'file': {
                'new': create_action(ICON_FILE, 'New File', self.new_file, self, QKeySequence.StandardKey.New, 'Create a new text file'),
                'open': create_action(ICON_OPEN, 'Open File', self.open_file, self, QKeySequence.StandardKey.Open, 'Opens a file'),
                'save': create_action(ICON_SAVE, 'Save', self.save, self, QKeySequence.StandardKey.Save, 'Save created file'),
                'saveas': create_action(ICON_SAVE_AS, 'Save As', self.save_as, self, QKeySequence.StandardKey.SaveAs, 'Save created file as new'),
                'print': create_action(ICON_PRINT, 'Print', self.print_document, self, QKeySequence.StandardKey.Print, 'Print Document'),
                'exit': create_action(ICON_RED_CROSS, 'Exit', self.close, self, 'Ctrl+Q', 'Exit application without saving')
            },
            'edit': {
                'undo': create_action(ICON_UNDO, 'Undo', self.editor.undo, self, QKeySequence.StandardKey.Undo),
                'redo': create_action(ICON_REDO, 'Redo', self.editor.redo, self, QKeySequence.StandardKey.Redo),
                'copy': create_action(ICON_COPY, 'Copy', self.editor.copy, self, QKeySequence.StandardKey.Copy),
                'paste': create_action(ICON_PASTE, 'Paste', self.editor.paste, self, QKeySequence.StandardKey.Paste),
                'cut': create_action(ICON_CUT, 'Cut', self.editor.cut, self, QKeySequence.StandardKey.Cut),
                'bold': create_action(ICON_BOLD, 'Bold', lambda x: self.editor.setFontWeight(QFont.Weight.Bold if x else QFont.Weight.Normal), self, QKeySequence.StandardKey.Bold, checkable = True),
                'italic': create_action(ICON_ITALIC, 'Italic', self.editor.setFontItalic, self, QKeySequence.StandardKey.Italic, checkable = True),
                'underline': create_action(ICON_UNDERLINE, 'Underline', self.editor.setFontUnderline, self, QKeySequence.StandardKey.Underline, checkable = True),
                'align_left': create_action(ICON_TEXT_LEFT, 'Align Left', lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft), self, checkable = True),
                'align_center': create_action(ICON_TEXT_CENTER, 'Align Center', lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter), self, checkable = True),
                'align_right': create_action(ICON_TEXT_RIGHT, 'Align Right', lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignRight), self, checkable = True),
                'align_justify': create_action(ICON_TEXT_JUSTIFY, 'Justify Text', lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignJustify), self, checkable = True),
                'foreground_color': create_action(ICON_COLOR, 'Text Color', lambda: self.editor.setTextColor(QColorDialog.getColor()), self),
                'background_color': create_action(ICON_BACKGROUND, 'Highlight Color', lambda: self.editor.setTextBackgroundColor(QColorDialog.getColor()), self),
                'select_all': create_action(ICON_SELECT_ALL, 'Select All', self.editor.selectAll, self, QKeySequence.StandardKey.SelectAll)
            },
            'view': {
                'darkmode': create_action(ICON_LIGHT, 'Page Color', lambda: self.editor.setStyleSheet(f'background: {QColorDialog.getColor().name()};'), self, tooltip = 'Sets a background color for page'),
                'wrap': create_action(ICON_WRAP, 'Wrap to Window', self.editor.toggle_wrap, self, tooltip = 'Wraps text to window', checkable = True, checked = True)
            },
            'about': {
                'github': create_action(ICON_GITHUB, 'Github Link', lambda: webbrowser.open('https://github.com/PoweredDeveloper/Text-Flow-QT'), self, tooltip = 'Sends you to github repository')
            }
        }

        separators: dict[str, list[int]] = {
            'file': [1, 3],
            'edit': [1, 4, 7, 11],
            'view': [],
            'about': []
        }

        # Menubar
        menubar = self.menuBar()
        for menu in self._actions.keys():
            menu_tab = menubar.addMenu(menu[0].capitalize() + menu[1:])
            for index, action in enumerate(self._actions[menu].values()):
                menu_tab.addAction(action)
                if separators[menu].count(index) > 0:
                    menu_tab.addSeparator()

        # Toolbar
        self._font_picker = QFontComboBox()
        self._font_picker.currentFontChanged.connect(lambda font: self.editor.setFontFamily(font.family()))
        self._font_picker.setItemIcon(0, QIcon(ICON_FONT))

        self._font_size = QComboBox()
        self._font_size.setMinimumWidth(40)
        self._font_size.addItems([str(s) for s in FONT_SIZES])
        self._font_size.currentIndexChanged.connect(lambda s: self.editor.setFontPointSize(float(FONT_SIZES[s])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        for index, action in enumerate(self._actions['edit'].values()):
            toolbar.addAction(action)
            if separators['edit'].count(index) > 0:
                toolbar.addSeparator()
            if index == len(self._actions['edit'].values()) - 2:
                toolbar.addWidget(self._font_picker)
                toolbar.addWidget(self._font_size)
                toolbar.addSeparator()

        self.addToolBar(toolbar)

    def footer(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.letter_counter = QLabel('Words: 0 | Letters: 0')
        layout.addWidget(self.letter_counter)
        layout.addStretch()
        layout.addWidget(QLabel('v0.2'))

        return layout
    
    def dialog_critical(self, message):
        dialog = QMessageBox(self)
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Icon.Critical)
        dialog.show()

    def new_file(self) -> None:
        if self.saved:
            self.saved = False
            self.clear_editor()
            return
        
        if (self.path == '' and self.editor.toPlainText() == ''): return

        dialog = QMessageBox()
        dialog.setText("You have opened file. Save this file?")
        dialog.setWindowTitle("Warning!")
        dialog.setWindowIcon(QIcon(APP_ICON))
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        button = dialog.exec()

        if button == QMessageBox.StandardButton.Save:
            if self.editor.toPlainText() != '' and self.path == '':
                print('save as')
                # self.save_as()
            if not self.saved and self.path != '':
                self.save()

            self.clear_editor()
            self.saved = False


        elif button == QMessageBox.StandardButton.No:
            self.clear_editor()
            self.saved = False

    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, 'Open file', os.path.join(os.environ['USERPROFILE'], 'Desktop'), 'FLOW documents (*.flow);Text documents (*.txt); HTML documents (*.HTML); All files (*.*)')

        if path == '': return

        try:
            with open(path, 'r', newline='', encoding='utf-8') as file:
                text = file.read()
            self.clear_editor()
            self.editor.setText(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.saved = True
            self.path = path
            self.update_title()

    def save(self) -> None:
        if self.path == '':
            self.save_as()
            return
        
        if self.saved: return

        text = self.editor.toHtml() if os.path.splitext(self.path)[1].lower() in ['.html', '.htm', '.flow'] else self.editor.toPlainText()
        
        try:
            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                file.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.saved = True
            self.update_title()

    def save_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save file", os.path.join(os.environ['USERPROFILE'], 'Desktop', 'document.flow'), 'FLOW documents (*.flow);Text documents (*.txt); HTML documents (*.HTML); All files (*.*)')
        
        if not path: return
        text = self.editor.toHtml() if os.path.splitext(path)[1].lower() in ['.html', '.htm', '.flow'] else self.editor.toPlainText()

        try:
            with open(path, 'w', newline='', encoding='utf-8') as file:
                file.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.saved = True
            self.update_title()

    def print_document(self):
        printer = QPrinter(mode = QPrinter.PrinterMode.HighResolution)
        printer.setPageSize(QPageSize.PageSizeId.A4)

        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.Accepted:
            current_widget = self.editor
            current_widget.print_(printer)
            
    def update_title(self) -> None:
        self.setWindowTitle(f'{os.path.basename(self.path) if self.path != '' else 'Untitled'}{'*' if not self.saved else ''} - Text Flow')

    def clear_editor(self) -> None:
        self.path = ''
        self.editor.clear()
        self.editor.clear_styles()
        self.update_title()

    def update_footer(self) -> None:
        self.saved = False
        self.update_title()
        text = list(filter(lambda x: x != '', re.sub(' +', ' ', self.editor.toPlainText()).split(' ')))
        letters = len(re.sub(' +', '', self.editor.toPlainText()))
        self.letter_counter.setText(f'Words: {len(text)} | Letters: {letters}')

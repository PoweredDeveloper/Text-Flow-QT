import webbrowser

from PySide6.QtWidgets import *
from PySide6.QtGui import *

from .paths import *
from .editor import Editor
from .utils import create_action

class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Initializing Window
        self.setWindowTitle("Text Flow")
        self.setFixedSize(720, 480)

        self.editor = Editor()
        self.initUI()

        self.setCentralWidget(QWidget())
        main_layout = QGridLayout()

        main_layout.addWidget(self.editor, 0, 0, 1, 2)

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 3)
        self.centralWidget().setLayout(main_layout)

    def initUI(self) -> None:
        actions = {
            'file': {
                'new': create_action(ICON_FILE, 'New File', lambda: print('new'), self, QKeySequence.StandardKey.New, 'Create a new text file'),
                'open': create_action(ICON_OPEN, 'Open File', lambda: print('open'), self, QKeySequence.StandardKey.Open, 'Opens a file'),
                'save': create_action(ICON_SAVE, 'Save', lambda: print('save'), self, QKeySequence.StandardKey.Save, 'Save created file'),
                'saveas': create_action(ICON_SAVE_AS, 'Save As', lambda: print('save as'), self, QKeySequence.StandardKey.SaveAs, 'Save created file as new'),
                'exit': create_action(ICON_RED_CROSS, 'Exit', self.close, self, 'Ctrl+Q', 'Exit application without saving')
            },
            'edit': {
                'undo': create_action(ICON_UNDO, 'Undo', self.editor.undo, self, QKeySequence.StandardKey.Undo),
                'redo': create_action(ICON_REDO, 'Redo', self.editor.redo, self, QKeySequence.StandardKey.Redo),
                'copy': create_action(ICON_COPY, 'Copy', self.editor.copy, self, QKeySequence.StandardKey.Copy),
                'paste': create_action(ICON_PASTE, 'Paste', self.editor.paste, self, QKeySequence.StandardKey.Paste),
                'cut': create_action(ICON_CUT, 'Cut', self.editor.cut, self, QKeySequence.StandardKey.Cut),
                'select_all': create_action(ICON_SELECT_ALL, 'Select All', self.editor.selectAll, self, QKeySequence.StandardKey.SelectAll)
            },
            'view': {
                'darkmode': create_action(ICON_LIGHT, 'Toggle Dark Mode', lambda: print('Toggle dark mode'), self, tooltip = 'Toggles dark mode'),
                'wrap': create_action(ICON_WRAP, 'Wrap to Window', self.editor.toggle_wrap, self, tooltip = 'Wraps text to window')
            },
            'about': {
                'github': create_action(ICON_GITHUB, 'Github Link', lambda: webbrowser.open('https://github.com/PoweredDeveloper/Text-Flow-QT'), self, tooltip = 'Sends you to github repository')
            }
        }

        separators: dict[str, list[int]] = {
            'file': [1, 3],
            'edit': [1, 4],
            'view': [],
            'about': []
        }

        # Menubar
        menubar = self.menuBar()
        for menu in actions.keys():
            menu_tab = menubar.addMenu(menu[0].capitalize() + menu[1:])
            for index, action in enumerate(actions[menu].values()):
                menu_tab.addAction(action)
                if separators[menu].count(index) > 0:
                    menu_tab.addSeparator()
                

    def toolbar(self) -> QHBoxLayout:
        toolbar_layout = QHBoxLayout()

        bold_button = QPushButton(QIcon(ICON_BOLD), '')
        italic_button = QPushButton(QIcon(ICON_ITALIC), '')
        underline_button = QPushButton(QIcon(ICON_UNDERLINE), '')

        toolbar_layout.addWidget(bold_button)
        toolbar_layout.addWidget(italic_button)
        toolbar_layout.addWidget(underline_button)
        toolbar_layout.addStretch()

        return toolbar_layout

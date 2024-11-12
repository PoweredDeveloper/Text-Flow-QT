import webbrowser

from PySide6.QtWidgets import *
from PySide6.QtGui import *

from .paths import *

class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        # Initializing Window
        self.setWindowTitle("Text Flow")
        self.setFixedSize(1200, 800)

        self.init_menubar()

    def init_menubar(self) -> None:
        # File Menu
        newAction = QAction(QIcon(ICON_FILE), 'New File', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create a new text file')
        newAction.triggered.connect(lambda: print('new'))

        openAction = QAction(QIcon(ICON_OPEN), 'Open File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Opens a file')
        openAction.triggered.connect(lambda: print('open'))

        saveAction = QAction(QIcon(ICON_SAVE), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save created file')
        saveAction.triggered.connect(lambda: print('save'))

        saveAsAction = QAction(QIcon(ICON_SAVE_AS), 'Save As', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.setStatusTip('Save created file as...')
        saveAsAction.triggered.connect(lambda: print('save as'))

        exitAction = QAction(QIcon(ICON_RED_CROSS), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application without saving')
        exitAction.triggered.connect(self.close)

        # View
        darkModeAction = QAction(QIcon(ICON_SUN), 'Toggle Dark Mode', self)
        exitAction.setShortcut('Ctrl+D')
        darkModeAction.setStatusTip('Toggles dark mode')
        darkModeAction.triggered.connect(lambda: print('Toggle dark mode'))

        # About Menu
        githubAction = QAction(QIcon(ICON_GITHUB), 'Github Link', self)
        githubAction.setStatusTip('Sends you to github repository')
        githubAction.triggered.connect(lambda: webbrowser.open('https://github.com/PoweredDeveloper'))

        # Menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        viewMenu = menubar.addMenu('View')
        viewMenu.addAction(darkModeAction)

        aboutMenu = menubar.addMenu('About')
        aboutMenu.addAction(githubAction)
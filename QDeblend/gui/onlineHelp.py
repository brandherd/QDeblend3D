from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__='0.1.2'


class HelpForm(QDialog):
    def __init__(self,  page,  parent=None):
        super(HelpForm, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_GroupLeader)
        
       # backAction = QAction(QIcon(":/back.png"), self.tr("&Back"), self)
        #backAction.setShortcut(QKeySequence.Back)
        #homeAction = QAction(QIcon(":/home.png"), self.tr("&Home"), self)
        #homeAction.setShortcut(self.tr("Home"))
        #self.pageLabel = QLabel()
        
        #toolBar = QToolBar()
        #toolBar.addAction(backAction)
        #toolBar.addAction(homeAction)
        #toolBar.addWidget(self.pageLabel)
        self.textBrowser = QTextBrowser()
        
        layout = QVBoxLayout()
        #layout.addWidget(toolBar)
        layout.addWidget(self.textBrowser, 1)
        self.setLayout(layout)
        
        self.textBrowser.setSearchPaths([":/"])
        self.textBrowser.setSource(QUrl(page))
        #self.connect(backAction,  SIGNAL("triggered()"), self.textBrowser, SLOT("backward()"))
        #self.connect(homeAction, SIGNAL("triggered()"), self.textBrowser, SLOT("home()"))
        self.connect(self.textBrowser,  SIGNAL("sourceChange(QUrl)"), self.updatePageTitle)
        self.resize(800, 700)
        self.setWindowTitle(self.tr("%1 Online Manual").arg(QApplication.applicationName()))
                
    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())
        

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class HelpForm(QDialog):
    def __init__(self,  page,  parent=None):
        super(HelpForm, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_GroupLeader)
        self.textBrowser = QTextBrowser()
        
        layout = QVBoxLayout()
        layout.addWidget(self.textBrowser, 1)
        self.setLayout(layout)
        
        self.textBrowser.setSearchPaths([":/"])
        self.textBrowser.setSource(QUrl(page))
        self.connect(self.textBrowser,  SIGNAL("sourceChange(QUrl)"), self.updatePageTitle)
        self.resize(800, 700)
        self.setWindowTitle(self.tr("%1 Online Manual").arg(QApplication.applicationName()))
                
    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())
        

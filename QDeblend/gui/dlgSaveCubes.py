import ui_dlgSaveCubes
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


__version__='0.1.2'


class dlgSaveCubes(QDialog, ui_dlgSaveCubes.Ui_dlgSaveCubes):
    def __init__(self, QSOcube,  EELRcube, parent=None):
        super(dlgSaveCubes,  self ).__init__(parent)
        self.setupUi(self)
        self.QSOCube = QSOcube
        self.EELRCube = EELRcube
        self.directory=''
        
        wave = self.EELRCube.wave
        step = wave[1]-wave[0]
        self.dStart.setValue(wave[0]-step/2)
        self.dEnd.setValue(wave[-1]+step/2)
        self.connect(self.bDirSelect, SIGNAL('pressed()'), self.getDir)
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.saveCubes)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)
        
        
    def getDir(self):
        dir = QFileDialog.getExistingDirectory(parent=self, caption = 'Select Directory', directory=os.getcwd())
        if not dir=='':
            self.lineDir.setText(dir)
            self.directory=dir
    
    def saveCubes(self):
        if self.linePrefix.text()=='':
            warning = QMessageBox.critical(self,'Run-time Error', 'No Prefix specified!')
        else:
            if self.directory=='':
                warning = QMessageBox.critical(self,'Run-time Error', 'No Directory selected!')
            else:
                self.EELRCube.subCube(self.dStart.value(), self.dEnd.value())
                self.QSOCube.subCube(self.dStart.value(), self.dEnd.value())
                self.EELRCube.writeFitsData(str(self.directory)+'/'+str(self.linePrefix.text())+'_EELR.fits')
                self.QSOCube.writeFitsData(str(self.directory)+'/'+str(self.linePrefix.text())+'_QSO.fits')
                self.accept()

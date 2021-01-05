# Copyright 2011 Bernd Husemann
#
#
#This file is part of QDeblend3D.
#
#QDeblend3D is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License  as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.
#
#QDeblend3D  is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with QDeblend3D.  If not, see <http://www.gnu.org/licenses/>.


import ui_dlgEditHostModel
import own_classes

from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = '0.1.2'

class DlgEditHostModel(QDialog, ui_dlgEditHostModel.Ui_dlgEditHostModel):
    def __init__(self, hostContainer, mode, title, parent=None):
        super(DlgEditHostModel,  self ).__init__(parent)
        self.setupUi(self)
        self.hostContainer = hostContainer
        self.parent=parent
        self.mode=mode
        self.setWindowTitle(title)
        if self.hostContainer.selected !=None and self.mode=='change':
            model = self.hostContainer.selected 
            self.dMag.setValue(model.mag)
            self.dDeltax.setValue(model.x)
            self.dDeltay.setValue(model.y)
            self.dEffRadius.setValue(model.re)
            self.dSersic.setValue(model.sersic)
            self.dElip.setValue(model.e)
            self.dPA.setValue(model.theta)
            
        self.connect(self.buttonBox.button(QDialogButtonBox.Ok), SIGNAL("clicked()"), self.updateModel)
        self.connect(self.buttonBox.button(QDialogButtonBox.Cancel), SIGNAL("clicked()"), self.reject)
            
    def updateModel(self):
        hostModel = own_classes.hostModel(self.dMag.value(), self.dDeltax.value(), self.dDeltay.value(), self.dEffRadius.value(), self.dSersic.value(), self.dElip.value(), self.dPA.value())
        if self.mode=='add':
            self.hostContainer.add(hostModel)
        if self.mode=='change':
            self.hostContainer.updateSelected(hostModel)
        self.parent.updateTable()
        self.parent.updateImag()
        self.accept()
        
        



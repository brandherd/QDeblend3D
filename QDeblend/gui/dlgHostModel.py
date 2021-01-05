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


import ui_dlgHostModel
import dlgEditHostModel
import copy
import numpy
import matplotlib
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = '0.1.2'

class dlgHostModel(QDialog, ui_dlgHostModel.Ui_dlgHostModel):
    def __init__(self, hostContainer, parent=None):
        super(dlgHostModel,  self ).__init__(parent)
        self.setupUi(self)
        self.container = hostContainer
        self.initcontainer = copy.deepcopy(hostContainer)
        self.updateTable()
  #      print self.container.models()
        if self.container.models()>0:
            if self.dispHostModel.image is None:
                self.dispHostModel.image=self.dispHostModel.axes.imshow(numpy.ones(self.container.dim), origin='lower',interpolation='nearest', cmap=matplotlib.cm.get_cmap('gray'), norm = matplotlib.colors.LogNorm())        
                self.dispHostModel.axes.set_xticks([])
                self.dispHostModel.axes.set_yticks([])
                self.dispHostModel.fig.canvas.draw()
            self.updateImag()
        else:
            self.dispHostModel.image=self.dispHostModel.axes.imshow(numpy.ones(self.container.dim), origin='lower',interpolation='nearest', cmap=matplotlib.cm.get_cmap('gray'), norm = matplotlib.colors.LogNorm())        
            self.dispHostModel.axes.set_xticks([])
            self.dispHostModel.axes.set_yticks([])
            self.dispHostModel.fig.canvas.draw()
        
        self.connect(self.bAddModel, SIGNAL("pressed()"), self.editModel)
        self.connect(self.bChangeModel, SIGNAL("pressed()"), self.editModel)
        self.connect(self.bDeleteModel, SIGNAL("pressed()"), self.deleteModel)
        self.connect(self.buttonBox.button(QDialogButtonBox.Cancel),SIGNAL("clicked()"), self.rejectChanges)
        self.connect(self.tableHost, SIGNAL("itemSelectionChanged ()"), self.setSelection)
        
    def updateTable(self, current=None):
        
        self.tableHost.clear()
        self.tableHost.setRowCount(len(self.container))
        self.tableHost.setHorizontalHeaderLabels(["Magnitude", "Delta x", "Delta y", "Eff. Radius", "Sersic index", "Ellipticity", "PA"])
        selected=None
        for row,  model in enumerate(self.container):
            item = QTableWidgetItem("%.2f" %(model.mag))
            self.tableHost.setItem(row, 0, item)
            if current is not None and current == id(model):
                selected = item
            item = QTableWidgetItem("%.2f" %(model.x))
            self.tableHost.setItem(row, 1, item)
            item = QTableWidgetItem("%.2f" %(model.y))
            self.tableHost.setItem(row, 2, item)
            item = QTableWidgetItem("%.2f" %(model.re))
            self.tableHost.setItem(row, 3, item)
            item = QTableWidgetItem("%.2f" %(model.sersic))
            self.tableHost.setItem(row, 4, item)
            item = QTableWidgetItem("%.2f" %(model.e))
            self.tableHost.setItem(row, 5, item)
            item = QTableWidgetItem("%.2f" %(model.theta))
            self.tableHost.setItem(row, 6, item)
        self.tableHost.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.tableHost.setCurrentItem(selected)
            self.table.scrolltoItem(selected)
            
            
    def updateImag(self):
        array=self.container.createHostModel()
        if array[0]!=False:
            self.dispHostModel.image.set_data(array[1])
            self.dispHostModel.image.set_clim(numpy.min(array[1]), numpy.max(array[1]))
            self.dispHostModel.fig.canvas.draw()
        else:
            self.dispHostModel.image.set_data(numpy.ones(self.container.dim))
            self.dispHostModel.image.set_clim(1.0, 1.0)
            self.dispHostModel.fig.canvas.draw()
            
    def setSelection(self):
        if len(self.container)!=0:
            row = self.tableHost.currentRow()   
            model= self.container.returnModel(row)
            self.container.setSelected(model)
        else:
            self.container.setSelected(None)
     
    def deleteModel(self):
         if self.container.selected!=None:
            self.container.delete(self.container.selected)
            self.container.selected=None
            self.updateTable()
            self.updateImag()
            
    def rejectChanges(self):
        self.container.copyContainer(self.initcontainer)
        self.reject()
         
    def editModel(self):
        sender = self.sender()
        if sender==self.bAddModel:
            dlg = dlgEditHostModel.DlgEditHostModel(self.container, mode='add',title='Add', parent=self)
            dlg.exec_()
        elif sender == self.bChangeModel:
            if not self.container.selected==None:
                dlg = dlgEditHostModel.DlgEditHostModel(self.container, mode='change',title='Change', parent=self)
                dlg.exec_()

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



import ui_dlgColorProperties
import pickle, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = '0.1.2'

class DlgColorProperties(QDialog,ui_dlgColorProperties.Ui_dlgColorProperties):
    def __init__(self, CPspec, CPspax, CPspax2, CPQSOspax, CPQSOspec, parent=None):
        super(DlgColorProperties,  self ).__init__(parent)
        self.setupUi(self)
        self.parent=parent
        self.CPspec=CPspec
        self.CPspax=CPspax
        self.CPspax2=CPspax2
        self.CPQSOspec=CPQSOspec
        self.CPQSOspax=CPQSOspax
        self.updateForm()
        
        self.connect(self.buttonBox.button(QDialogButtonBox.Apply), SIGNAL("clicked()"), self.apply)
        self.connect(self.buttonBox.button(QDialogButtonBox.Cancel), SIGNAL("clicked()"), self.close)
        self.connect(self.buttonBox.button(QDialogButtonBox.Save), SIGNAL("clicked()"), self.saveSettings)
        self.connect(self.buttonBox.button(QDialogButtonBox.Open), SIGNAL("clicked()"), self.loadSettings)
        self.connect(self.buttonBox.button(QDialogButtonBox.RestoreDefaults), SIGNAL("clicked()"), self.restore)
    
    
    def updateForm(self):
        self.comboBoxCSpec1.setCurrentIndex(color_index(map_from_pylab(self.CPspec.spec1['color'])))
        self.comboBoxCSpec2.setCurrentIndex(color_index(map_from_pylab(self.CPspec.spec2['color'])))
        self.comboBoxCSlicer.setCurrentIndex(color_index(map_from_pylab(self.CPspec.slicer['color'])))
        self.comboBoxCZoom.setCurrentIndex(color_index(map_from_pylab(self.CPspec.zoom['color'])))
        self.comboBoxCSelect.setCurrentIndex(color_index(map_from_pylab(self.CPspec.select['color'])))
        
        self.comboBoxSSpec1.setCurrentIndex(style_index(map_from_pylab(self.CPspec.spec1['style'])))
        self.comboBoxSSpec2.setCurrentIndex(style_index(map_from_pylab(self.CPspec.spec2['style'])))
        self.comboBoxSSlicer.setCurrentIndex(style_index(map_from_pylab(self.CPspec.slicer['style'])))
        self.comboBoxSZoom.setCurrentIndex(style_index(map_from_pylab(self.CPspec.zoom['style'])))
        self.comboBoxSSelect.setCurrentIndex(style_index(map_from_pylab(self.CPspec.select['style'])))
        
        self.spinBoxWSpec1.setValue(self.CPspec.spec1['width'])
        self.spinBoxWSpec2.setValue(self.CPspec.spec2['width'])
        self.spinBoxWSlicer.setValue(self.CPspec.slicer['width'])
        self.spinBoxWZoom.setValue(self.CPspec.zoom['width'])
        self.spinBoxWSelect.setValue(self.CPspec.select['width'])
        
        self.comboBoxHSelect.setCurrentIndex(hatch_index(self.CPspec.select['hatch']))
        self.spinBoxASelect.setValue(self.CPspec.select['alpha'])
        
        
        
        self.comboBoxMImage.setCurrentIndex(self.comboBoxMImage.findText(self.CPspax.image['colormap']))
        self.checkBoxRmapImage.setChecked(self.CPspax.image['reversed'])
        self.comboBoxIImage.setCurrentIndex(self.comboBoxIImage.findText(self.CPspax.image['interpolation']))
        self.comboBoxSImage.setCurrentIndex(self.comboBoxSImage.findText(self.CPspax.image['scaling']))
        self.spinBoxRImage.setValue(self.CPspax.image['radius'])
        
        self.comboBoxCMarker.setCurrentIndex(color_index(map_from_pylab(self.CPspax.marker['color'])))
        self.spinBoxWMarker.setValue(self.CPspax.marker['width'])
        self.comboBoxHMarker.setCurrentIndex(self.comboBoxHMarker.findText(self.CPspax.marker['hatch']))
        self.spinBoxAMarker.setValue(self.CPspax.marker['alpha'])
        
        self.comboBoxCSpaxSelect.setCurrentIndex(color_index(map_from_pylab(self.CPspax.select['color'])))
        self.spinBoxWSpaxSelect.setValue(self.CPspax.select['width'])
        self.comboBoxHSpaxSelect.setCurrentIndex(self.comboBoxHSpaxSelect.findText(self.CPspax.select['hatch']))
        self.spinBoxASpaxSelect.setValue(self.CPspax.select['alpha'])
        
        self.comboBoxCQSOSpax.setCurrentIndex(color_index(map_from_pylab(self.CPQSOspax.QSO['color'])))
        self.spinBoxWQSOSpax.setValue(self.CPQSOspax.QSO['width'])
        self.comboBoxHQSOSpax.setCurrentIndex(self.comboBoxHQSOSpax.findText(self.CPQSOspax.QSO['hatch']))
        self.spinBoxAQSOSpax.setValue(self.CPQSOspax.QSO['alpha'])
        
        self.comboBoxCEELRSpax.setCurrentIndex(color_index(map_from_pylab(self.CPQSOspax.EELR['color'])))
        self.spinBoxWEELRSpax.setValue(self.CPQSOspax.EELR['width'])
        self.comboBoxHEELRSpax.setCurrentIndex(self.comboBoxHEELRSpax.findText(self.CPQSOspax.EELR['hatch']))
        self.spinBoxAEELRSpax.setValue(self.CPQSOspax.EELR['alpha'])
    
        self.comboBoxCQSOcont.setCurrentIndex(color_index(map_from_pylab(self.CPQSOspec.cont['color'])))
        self.spinBoxWQSOcont.setValue(self.CPQSOspec.cont['width'])
        self.comboBoxHQSOcont.setCurrentIndex(self.comboBoxHQSOcont.findText(self.CPQSOspec.cont['hatch']))
        self.spinBoxAQSOcont.setValue(self.CPQSOspec.cont['alpha'])
        
        self.comboBoxCQSObroad.setCurrentIndex(color_index(map_from_pylab(self.CPQSOspec.broad['color'])))
        self.spinBoxWQSObroad.setValue(self.CPQSOspec.broad['width'])
        self.comboBoxHQSObroad.setCurrentIndex(self.comboBoxHQSOcont.findText(self.CPQSOspec.broad['hatch']))
        self.spinBoxAQSObroad.setValue(self.CPQSOspec.broad['alpha'])
        
        
    def apply(self):
        spec1 = {'color':map_to_pylab(str(self.comboBoxCSpec1.currentText())), 'width':self.spinBoxWSpec1.value(), 'style':map_to_pylab(str(self.comboBoxSSpec1.currentText()))}
        spec2 = {'color':map_to_pylab(str(self.comboBoxCSpec2.currentText())), 'width':self.spinBoxWSpec2.value(), 'style':map_to_pylab(str(self.comboBoxSSpec2.currentText()))}
        slicer = {'color':map_to_pylab(str(self.comboBoxCSlicer.currentText())), 'width':self.spinBoxWSlicer.value(), 'style':map_to_pylab(str(self.comboBoxSSlicer.currentText()))}
        zoom = {'color':map_to_pylab(str(self.comboBoxCZoom.currentText())), 'width':self.spinBoxWZoom.value(), 'style':map_to_pylab(str(self.comboBoxSZoom.currentText()))}        
        select = {'color':map_to_pylab(str(self.comboBoxCSelect.currentText())), 'width':self.spinBoxWSelect.value(), 'style':map_to_pylab(str(self.comboBoxSSelect.currentText())), 'hatch':str(self.comboBoxHSelect.currentText()),'alpha':self.spinBoxASelect.value()}
        if select['hatch']=='None':
            select['hatch']=None
        imag = {'colormap':str(self.comboBoxMImage.currentText()), 'reversed':self.checkBoxRmapImage.isChecked(), 'interpolation':str(self.comboBoxIImage.currentText()), 'radius':self.spinBoxRImage.value(),'scaling':str(self.comboBoxSImage.currentText())}
        marker =  {'color':map_to_pylab(str(self.comboBoxCMarker.currentText())), 'width':self.spinBoxWMarker.value(), 'hatch':str(self.comboBoxHMarker.currentText()), 'alpha':self.spinBoxAMarker.value()}
        spaxsel = {'color':map_to_pylab(str(self.comboBoxCSpaxSelect.currentText())), 'width':self.spinBoxWSpaxSelect.value(), 'hatch':str(self.comboBoxHSpaxSelect.currentText()), 'alpha':self.spinBoxASpaxSelect.value()}
        
        QSObroad =  {'color':map_to_pylab(str(self.comboBoxCQSObroad.currentText())), 'width':self.spinBoxWQSObroad.value(), 'hatch':str(self.comboBoxHQSObroad.currentText()), 'alpha':self.spinBoxAQSObroad.value()}
        QSOcont =  {'color':map_to_pylab(str(self.comboBoxCQSOcont.currentText())), 'width':self.spinBoxWQSOcont.value(), 'hatch':str(self.comboBoxHQSOcont.currentText()), 'alpha':self.spinBoxAQSOcont.value()}
        QSOSpax =  {'color':map_to_pylab(str(self.comboBoxCQSOSpax.currentText())), 'width':self.spinBoxWQSOSpax.value(), 'hatch':str(self.comboBoxHQSOSpax.currentText()), 'alpha':self.spinBoxAQSOSpax.value()}    
        EELRSpax =  {'color':map_to_pylab(str(self.comboBoxCEELRSpax.currentText())), 'width':self.spinBoxWEELRSpax.value(), 'hatch':str(self.comboBoxHEELRSpax.currentText()), 'alpha':self.spinBoxAEELRSpax.value()}    
        self.CPspec.update(spec1, spec2, slicer, zoom, select)
        self.CPspax.update(imag, marker, spaxsel)
        self.CPspax2.update(imag, marker, spaxsel)
        self.CPQSOspec.update(broad=QSObroad, cont=QSOcont)
        self.CPQSOspax.update(QSO=QSOSpax, EELR=EELRSpax)
        self.accept()
        
    
    def saveSettings(self):
        self.file_name = QFileDialog.getSaveFileName(self.parent, 
    caption="Save Color Setting", directory=os.getcwd(), filter="Settings (*.cf)")
        try:
            pickle_objects = [self.CPspec.__dict__, self.CPspax.__dict__, self.CPQSOspec.__dict__, self.CPQSOspax.__dict__]
            file = open(file_name[0], 'w')
            pickle.dump(pickle_objects, file)
            file.close()
        except:
            pass
            
    def loadSettings(self):
        
        self.file_name = QFileDialog.getOpenFileName(self.parent,
     caption="Open Color Setting", directory=os.getcwd(), filter="Settings (*.cf)")
        try:
            file = open(file_name, 'r')
            list = pickle.load(file)
            file.close()
            self.CPspec.update(list[0]['spec1'], list[0]['spec2'], list[0]['slicer'], list[0]['zoom'], list[0]['select'])
            self.CPspax.update(list[1]['image'], llist[1]['marker'], list[1]['select'])
            
            self.CPspax2.update(list[1]['image'], list[1]['marker'], list[1]['select'])
            self.CPQSOspax.update(list[2]['QSO'], list[2]['EELR'])
            self.CPQSOspex.update(list[3]['broad'], list[e]['cont'])
    
        except:
            pass
            
        
    
    def restore(self):
        self.CPspec.default_values()
        self.CPspax.default_values()
        self.CPspax2.default_values()
        self.CPQSOspec.default_values()
        self.CPQSOspax.default_values()
        self.updateForm()
        
        
def map_to_pylab(input):
    trans = {'black':'k', 'blue':'b', 'red':'r', 'green':'g', 'yellow':'y', 'magenta':'m', 
    'solid':'-', 'dashed':'--', 'dotted':':', 'dash-dot':'-.','points':'.', 'circles':'o'}
    return trans[input]
    
def map_from_pylab(input):
    trans = {'k':'black', 'b':'blue', 'r':'red', 'g':'green', 'y':'yellow', 'm':'magenta', 
    '-':'solid', '--':'dashed', ':':'dotted', '-.':'dash-dot','.':'points', 'o':'circles'}
    return trans[input]
    
def color_index(item):
    index = {'black':0, 'blue':1, 'red':2, 'green':3, 'yellow':4, 'magenta':5}
    return index[item]

def style_index(item):
    index = {'solid':0, 'dashed':1, 'dotted':2, 'dash-dot':3, 'points':4, 'circles':5}
    return index[item]
    
def hatch_index(item):
    index = {'None':0, '/':1, '|':2, '-':3, '+':4, 'o':5, 'O':6, '+':7, '.':8, '*':9}
    return index[item]

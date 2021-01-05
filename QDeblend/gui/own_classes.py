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


import mask_def
import host_profiles
import dlgHostModel
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox

__version__ = '0.1.2'

class limitWidget(QObject):
    def __init__(self, edit_min, edit_max, check_edit):
        QObject.__init__(self)
        self.max_box = edit_max
        self.min_box = edit_min
        self.check_box =check_edit
        self.connect(self.check_box, SIGNAL("clicked()"), self.updateCheck)
        self.connect(self.min_box, SIGNAL("editingFinished()"), self.changedLimits)
        self.connect(self.max_box, SIGNAL("editingFinished()"), self.changedLimits)
        try:
            self.max = float(self.max_box.text())
        except:
            self.max = None
        try:
            self.min = float(self.min_box.text())
        except:
            self.min = None
        self.auto = self.check_box.isChecked()
        
    def setLimits(self, min=None, max=None):
        if min!=None:
            self.min = min
            self.min_box.setText('%.3e'%(self.min))
        if max!=None:
            self.max = max
            self.max_box.setText('%.3e'%(self.max))
            
    def setAuto(self):
        self.setChecked(True)
        self.setEnabled(True)
        
    def setManual(self):
        self.setChecked(False)
        self.setEnabled(True)
    def setChecked(self, state):
        self.auto = state
        self.check_box.setChecked(self.auto)
        
    def isAuto(self):
        if self.auto==True:
            return True
        else:
            False
        
    def setEnabled(self, state):
        self.check_box.setEnabled(state)
        self.auto = self.check_box.isChecked()
        if self.auto == True:
            self.max_box.setEnabled(False)
            self.min_box.setEnabled(False)
        else:
            self.max_box.setEnabled(True)
            self.min_box.setEnabled(True)
    
    def updateCheck(self):
        self.setEnabled(True)
    
    def changedLimits(self):
        self.min = float(self.min_box.text())
        self.max = float(self.max_box.text())
        self.emit(SIGNAL("limitsChanged"), self.min, self.max)

class regionsSpaxWidget(QObject):
    def __init__(self, boxQSOSize, boxEELRWidth, radioRegular, radioCustom, boxDisplay, buttonSaveQSO, buttonChangeQSO, buttonSaveEELR, buttonChangeEELR, CPScheme, parent=None):
        QObject.__init__(self)
        self.parent=parent
        self.boxQSOSize = boxQSOSize
        self.boxEELRWidth = boxEELRWidth
        self.radioRegular = radioRegular
        self.radioCustom = radioCustom
        self.boxDisplay = boxDisplay
        self.buttonSaveQSO = buttonSaveQSO
        self.buttonChangeQSO = buttonChangeQSO
        self.buttonSaveEELR = buttonSaveEELR
        self.buttonChangeEELR = buttonChangeEELR
        self.colorScheme = CPScheme
        self.cube = None
        self.centQSO = None
        
        self.connect(self.radioRegular, SIGNAL("clicked()"), self.regionRegularToggled)
        self.connect(self.radioCustom, SIGNAL("clicked()"), self.regionCustomToggled)
        self.connect(self.boxQSOSize, SIGNAL("valueChanged(int)"), self.updateQSOSizeReg)
        self.connect(self.boxEELRWidth, SIGNAL("valueChanged(int)"), self.updateEELRWidthReg)
        self.connect(self.boxDisplay, SIGNAL("stateChanged(int)"), self.displayRegionMasks)
        self.connect(self.buttonSaveQSO, SIGNAL("pressed()"), self.saveRegionCustom)
        self.connect(self.buttonSaveEELR, SIGNAL("pressed()"), self.saveRegionCustom)
        self.connect(self.buttonChangeQSO, SIGNAL("pressed()"), self.changeRegionCustom)
        self.connect(self.buttonChangeEELR, SIGNAL("pressed()"), self.changeRegionCustom)
        self.connect(self.colorScheme, SIGNAL("changed()"), self.updateColorScheme)
    

    def clearMasks(self):
        self.maskEELRCustom.emptyMask()
        self.maskQSOCustom.emptyMask()
        self.buttonChangeEELR.setEnabled(False)
        self.buttonChangeQSO.setEnabled(False)
        self.boxDisplay.setChecked(False)
        self.regionRegularToggled()
        self.boxQSOSize.setValue(1)
        self.boxEELRWidth.setValue(1)
        self.cube=None
        self.centQSO=None 
        
    def initLimits(self, cube):
        self.cube = cube
        self.centQSO= self.cube.findMaximum()
        self.centQSOAuto = True
        self.xmax = min(self.centQSO[1][1]+1, self.cube.xDim-self.centQSO[1][1])
        self.ymax = min(self.centQSO[1][0]+1, self.cube.yDim-self.centQSO[1][0])
        self.maxQSOSize()
        self.maxEELRWidth()
    
    def setQSOCentManual(self, center):
        if center[1]>0 and center[0]>0 and center[0]<self.cube.yDim-1 and center[1]<self.cube.xDim-1:
            self.centQSO = ['Manual', center ]
            self.centQSOAuto = False
            self.xmax = min(self.centQSO[1][1]+1, self.cube.xDim-self.centQSO[1][1])
            self.ymax = min(self.centQSO[1][0]+1, self.cube.yDim-self.centQSO[1][0])
            self.maskQSORegular.maskBox(self.centQSO[1], 1)
            self.maskEELRRegular.maskShell(self.centQSO[1], 1, 1)
            self.boxQSOSize.setValue(1)
            self.boxEELRWidth.setValue(1)
            self.maxQSOSize()
            self.maxEELRWidth()
        else:
            QMessageBox.critical(self.parent, 'Error Message', 'QSO center at the edge of the FOV!\n Please selected a different QSO center..')
        
    
    def maxEELRWidth(self):
        self.boxEELRWidth.setMaximum((min(self.xmax, self.ymax)-1)-(self.boxQSOSize.value()-1)/2)
        
    def maxQSOSize(self):
        self.boxQSOSize.setMaximum(2*(min(self.xmax, self.ymax)-(self.boxEELRWidth.value())-1)+1)
        
    def setupMasks(self, displayWidg):
        self.displayWidg = displayWidg
        region = mask_def.mask((self.cube.yDim, self.cube.xDim))
        region.maskShell(self.centQSO[1], self.boxQSOSize.value(), self.boxEELRWidth.value())
        if  self.colorScheme.EELR['hatch']!='None':
            fill = False
            hatch = self.colorScheme.EELR['hatch']
        else:
            fill = True
            hatch = None
        self.maskEELRRegular =  mask_def.displayImgMask(self.displayWidg, (self.cube.yDim, self.cube.xDim), region.mask, color=self.colorScheme.EELR['color'], hatch=hatch, fill=fill,  alpha=self.colorScheme.EELR['alpha'], visible=False)
        self.maskEELRCustom =  mask_def.displayImgMask(self.displayWidg, (self.cube.yDim, self.cube.xDim), color=self.colorScheme.EELR['color'], hatch=hatch, fill=fill,  alpha=self.colorScheme.EELR['alpha'], visible=False)
        region = mask_def.mask((self.cube.yDim, self.cube.xDim))
        region.maskBox(self.centQSO[1], self.boxQSOSize.value())
        if  self.colorScheme.QSO['hatch']!='None':
            fill = False
            hatch = self.colorScheme.QSO['hatch']
        else:
            fill = True
            hatch = None
        self.maskQSORegular =  mask_def.displayImgMask(self.displayWidg, (self.cube.yDim, self.cube.xDim), region.mask, color=self.colorScheme.QSO['color'],   hatch=hatch,fill=fill,  alpha=self.colorScheme.QSO['alpha'], visible=False)
        self.maskQSOCustom =  mask_def.displayImgMask(self.displayWidg, (self.cube.yDim, self.cube.xDim),  color=self.colorScheme.QSO['color'],  hatch=hatch,fill=fill,  alpha=self.colorScheme.QSO['alpha'], visible=False)
        self.boxDisplay.setEnabled(True)
        
    def regionRegularToggled(self):
        self.radioRegular.setChecked(True)
        self.radioCustom.setChecked(False)
        self.boxDisplay.setEnabled(True)
        self.boxQSOSize.setEnabled(True)
        self.boxEELRWidth.setEnabled(True)
        self.buttonSaveQSO.setEnabled(False)
        self.buttonSaveEELR.setEnabled(False)
        self.buttonChangeQSO.setEnabled(False)
        self.buttonChangeEELR.setEnabled(False)
        self.displayRegionMasks(2)
        
    
    def regionCustomToggled(self):
        self.radioRegular.setChecked(False)
        self.radioCustom.setChecked(True)
        self.boxQSOSize.setEnabled(False)
        self.boxEELRWidth.setEnabled(False)
            
        if self.maskQSOCustom.area!=[]:
            self.buttonSaveQSO.setEnabled(True)
            self.buttonChangeQSO.setEnabled(True)
        else:
            self.buttonSaveQSO.setEnabled(True)
            self.buttonChangeQSO.setEnabled(False)
        
        if self.maskEELRCustom.area!=[]:
            self.buttonSaveEELR.setEnabled(True)
            self.buttonChangeEELR.setEnabled(True)
        else:
            self.buttonSaveEELR.setEnabled(True)
            self.buttonChangeEELR.setEnabled(False)
        self.displayRegionMasks(2)
        
    def isRegular(self):
        if self.radioRegular.isChecked():
            return True
        else:
            return False
            
    def getQSOMask(self):
        if self.isRegular():
            qso = self.maskQSORegular.getMask()
        else:
            qso = self.maskQSOCustom.getMask()
        return qso
        
    def getEELRMask(self):
        if self.isRegular():
            eelr = self.maskEELRRegular.getMask()
        else:
            eelr = self.maskEELRCustom.getMask()
        return eelr   
        
    def getSettings(self):
        out=[]
        out.append(self.isRegular())
        out.append( self.boxQSOSize.value())
        out.append( self.boxEELRWidth.value())
        out.append(list(self.maskQSOCustom.mask.mask))
        out.append(list(self.maskEELRCustom.mask.mask))
        out.append(self.boxDisplay.isChecked())
        out.append(self.centQSO)
        out.append(self.centQSOAuto)
        return out
        
    def loadSettings(self, set):
        self.centQSO  = set[6]
        self.radioRegular.setChecked(set[0])
        self.maskQSOCustom.maskArray(set[3])
        self.maskEELRCustom.maskArray(set[4])
        self.radioRegular.setChecked(set[0])
        self.boxDisplay.setChecked(set[5])
        if set[7]==False:
            self.setQSOCentManual(set[6][1])
        self.maskQSORegular.maskBox(self.centQSO[1], set[1])
        self.maskEELRRegular.maskShell(self.centQSO[1], set[1], set[2])
        self.boxQSOSize.setValue(set[1])
        self.boxEELRWidth.setValue(set[2])
        self.maxQSOSize()
        self.maxEELRWidth()
        
        
    def updateQSOSizeReg(self, size):
            self.maskQSORegular.maskBox(self.centQSO[1], size)
            self.maskEELRRegular.maskShell(self.centQSO[1], size, self.boxEELRWidth.value())
            self.maxEELRWidth()
            
    def updateEELRWidthReg(self, size):
            self.maskEELRRegular.maskShell(self.centQSO[1], self.boxQSOSize.value(),  size)
            self.maxQSOSize()
            
    def saveRegionCustom(self):
        sender =self.sender()
        if sender == self.buttonSaveQSO:
            self.maskQSOCustom.setMask(self.displayWidg.selectSpaxMask.mask.mask)
            self.displayWidg.selectSpaxMask.emptyMask()
            if self.maskQSOCustom.isEmpty()==True:
                self.buttonChangeQSO.setEnabled(False)
            else:
                self.buttonChangeQSO.setEnabled(True)
        elif sender == self.buttonSaveEELR:
            self.maskEELRCustom.setMask(self.displayWidg.selectSpaxMask.mask.mask)
            self.displayWidg.selectSpaxMask.emptyMask()
            if self.maskEELRCustom.isEmpty()==True:
                self.buttonChangeEELR.setEnabled(False)
            else:
                self.buttonChangeEELR.setEnabled(True)
        if not self.boxDisplay.isChecked():
            self.maskQSOCustom.setVisible(False)
            self.maskEELRCustom.setVisible(False)
                
    def changeRegionCustom(self):
        sender =self.sender()
        if sender == self.buttonChangeQSO:
            self.displayWidg.selectSpaxMask.setMask(self.maskQSOCustom.mask.mask)
        elif sender == self.buttonChangeEELR:
            self.displayWidg.selectSpaxMask.setMask(self.maskEELRCustom.mask.mask)
        self.emit(SIGNAL("maskChanges"))
            
    def displayRegionMasks(self, state):
        if state==2:
            status =True
        elif state==0:
            status = False
        if self.radioRegular.isChecked() == True:
            self.maskQSORegular.setVisible(status)
            self.maskEELRRegular.setVisible(status)
            self.maskQSOCustom.setVisible(False)
            self.maskEELRCustom.setVisible(False)
        else:
            self.maskQSORegular.setVisible(False)
            self.maskEELRRegular.setVisible(False)
            self.maskQSOCustom.setVisible(status)
            self.maskEELRCustom.setVisible(status)
    
    def updateColorScheme(self):
        if  self.colorScheme.QSO['hatch']!='None':
            fill = False
            hatch = self.colorScheme.QSO['hatch']
        else:
            fill = True
            hatch = None
        self.maskQSOCustom.setHatch(hatch)
        self.maskQSOCustom.setFill(fill)
        self.maskQSOCustom.setColor(self.colorScheme.QSO['color'])
        self.maskQSOCustom.setAlpha(self.colorScheme.QSO['alpha'])
        self.maskQSORegular.setHatch(hatch)
        self.maskQSORegular.setFill(fill)
        self.maskQSORegular.setColor(self.colorScheme.QSO['color'])
        self.maskQSORegular.setAlpha(self.colorScheme.QSO['alpha'])
        
        if  self.colorScheme.EELR['hatch']!='None':
            fill = False
            hatch = self.colorScheme.EELR['hatch']
        else:
            fill = True
            hatch = None
        self.maskEELRCustom.setHatch(hatch)
        self.maskEELRCustom.setFill(fill)
        self.maskEELRCustom.setColor(self.colorScheme.EELR['color'])
        self.maskEELRCustom.setAlpha(self.colorScheme.EELR['alpha'])
        self.maskEELRRegular.setHatch(hatch)
        self.maskEELRRegular.setFill(fill)
        self.maskEELRRegular.setColor(self.colorScheme.EELR['color'])
        self.maskEELRRegular.setAlpha(self.colorScheme.EELR['alpha'])
        
        
class sliderWidget(QObject):
    def __init__(self, slider, sliderLabel, cube):
            QObject.__init__(self)
            self.cube = cube
            self.slider = slider
            self.sliderLabel = sliderLabel
            self.slider.setMaximum(self.cube.wDim)
            self.slider.setSliderPosition(1)
            self.slider.setValue(1)
            self.slider.setTickInterval(50)
            self.sliderLabel.setText('1')
            
    def updateSlider(self, value):
        self.sliderLabel.setText(str(value)) 
        
    def setEnabled(self, bool):
        self.slider.setEnabled(bool)
        
class regionsSpecWidget(QObject):
    def __init__(self, comboBoxRegions, buttonSaveBroad1, buttonSaveBroad2, buttonChangeBroad1, buttonChangeBroad2, buttonSaveCont1, buttonSaveCont2, buttonChangeCont1, buttonChangeCont2, checkInterpCont, checkDisplayRegion, CPScheme):
        QObject.__init__(self)
        self.comboRegions = comboBoxRegions
        self.bSaveBroad1 = buttonSaveBroad1
        self.bSaveBroad2 = buttonSaveBroad2
        self.bChangeBroad1 = buttonChangeBroad1
        self.bChangeBroad2 = buttonChangeBroad2
        
        self.bSaveCont1 = buttonSaveCont1
        self.bSaveCont2 = buttonSaveCont2
        self.bChangeCont1 = buttonChangeCont1
        self.bChangeCont2 = buttonChangeCont2
        
        self.boxInterpCont = checkInterpCont
        self.interpCont = self.boxInterpCont.isChecked()
        self.boxDisplay  = checkDisplayRegion
        self.display = self.boxDisplay.isChecked()
        self.colorScheme = CPScheme
        self.colorCont = 'b'
        self.colorBroad ='g'
        
        self.connect(self.comboRegions, SIGNAL("currentIndexChanged (int)"), self.changeSpecRegionSelect)
        self.connect(self.boxDisplay, SIGNAL("stateChanged (int)"), self.displaySpecRegionsSelect)
        self.connect(self.bSaveBroad1, SIGNAL("clicked()"), self.saveRegionSpec)
        self.connect(self.bSaveBroad2, SIGNAL("clicked()"), self.saveRegionSpec)
        self.connect(self.bSaveCont1, SIGNAL("clicked()"), self.saveRegionSpec)
        self.connect(self.bSaveCont2, SIGNAL("clicked()"), self.saveRegionSpec)
        self.connect(self.bChangeBroad1, SIGNAL("clicked()"), self.changeRegionSpec)
        self.connect(self.bChangeBroad2, SIGNAL("clicked()"), self.changeRegionSpec)
        self.connect(self.bChangeCont1, SIGNAL("clicked()"), self.changeRegionSpec)
        self.connect(self.bChangeCont2, SIGNAL("clicked()"), self.changeRegionSpec)
        
    def clearMasks(self):
        self.regionCont1.emptyRegion()
        self.regionCont2.emptyRegion()
        self.regionBroad1.emptyRegion()
        self.regionBroad2.emptyRegion()
        self.changeSpecRegionSelect(0)
        self.bChangeBroad1.setEnabled(True)
        self.bChangeCont1.setEnabled(True)
        self.boxInterpCont.setChecked(False)
        self.boxDisplay.setChecked(False)
        self.display = False
        self.interpCont=False
        self.comboRegions.setCurrentIndex(0)
        
    def setupMasks(self, displayWidg):
        self.displayWidg = displayWidg
        self.regionCont1 = mask_def.displaySpecRegion(self.displayWidg, color=self.colorCont, picker=False)
        self.regionCont2 = mask_def.displaySpecRegion(self.displayWidg, color=self.colorCont, picker=False)
        self.regionBroad1 = mask_def.displaySpecRegion(self.displayWidg, color=self.colorBroad, picker=False)
        self.regionBroad2 = mask_def.displaySpecRegion(self.displayWidg, color=self.colorBroad, picker=False)
        self.boxDisplay.setEnabled(True)
        self.bSaveBroad1.setEnabled(True)
        self.bSaveCont1.setEnabled(True)
        self.boxInterpCont.setEnabled(False)
        
    def copySelectMask(self, mask):
        mask.copyMask(self.displayWidg.selectSpecMask)
        
    def changeSpecRegionSelect(self, index):
        if index ==0:
            self.bSaveBroad2.setEnabled(False)
            self.bChangeBroad2.setEnabled(False)
            self.bSaveCont2.setEnabled(False)
            self.bChangeCont2.setEnabled(False)
            self.boxInterpCont.setEnabled(False)
            self.boxInterpCont.setChecked(False)
        elif index ==1:
            self.bSaveBroad2.setEnabled(True)
            self.boxInterpCont.setEnabled(False)
            self.boxInterpCont.setChecked(False)
            if self.regionBroad2.isEmpty():
                self.bChangeBroad2.setEnabled(False)
            else:
                self.bChangeBroad2.setEnabled(True)
            self.bSaveCont2.setEnabled(False)
            self.bChangeCont2.setEnabled(False)
        elif index ==2:
            self.boxInterpCont.setEnabled(True)
            self.bSaveBroad2.setEnabled(False)
            self.bChangeBroad2.setEnabled(False)
            self.bSaveCont2.setEnabled(True)
            if self.regionCont2.isEmpty():
                self.bChangeCont2.setEnabled(False)
            else:
                self.bChangeCont2.setEnabled(True)
        elif index ==3:
            self.bSaveBroad2.setEnabled(True)
            self.boxInterpCont.setEnabled(True)
            if self.regionBroad2.isEmpty():
                self.bChangeBroad2.setEnabled(False)
            else:
                self.bChangeBroad2.setEnabled(True)
            self.bSaveCont2.setEnabled(True)
            if self.regionCont2.isEmpty():
                self.bChangeCont2.setEnabled(False)
            else:
                self.bChangeCont2.setEnabled(True)
        self.displaySpecRegionsSelect()
    
    def displaySpecRegionsSelect(self):
        self.display = self.boxDisplay.isChecked()
        regions=[self.regionCont1, self.regionCont2, self.regionBroad1, self.regionBroad2 ]
        buttons=[self.bSaveCont1, self.bSaveCont2, self.bSaveBroad1, self.bSaveBroad2]
        for i in range(len(regions)):
            if buttons[i].isEnabled()==True and self.display:
                regions[i].setVisible(True)
            else:
                regions[i].setVisible(False)
        
    
    def saveRegionSpec(self):
        sender =self.sender()
        regions=[self.regionCont1, self.regionCont2, self.regionBroad1, self.regionBroad2 ]
        buttons=[self.bSaveCont1, self.bSaveCont2, self.bSaveBroad1, self.bSaveBroad2]
        cbuttons=[self.bChangeCont1, self.bChangeCont2, self.bChangeBroad1, self.bChangeBroad2]
        idx = buttons.index(sender)
        regions[idx].copyMask(self.displayWidg.selectSpecMask)
        self.displayWidg.selectSpecMask.emptyRegion()
        if regions[idx].isEmpty()==True:
            cbuttons[idx].setEnabled(False)
        else:
            cbuttons[idx].setEnabled(True)
        self.displaySpecRegionsSelect()

    def changeRegionSpec(self):
        sender =self.sender()
        regions=[self.regionCont1, self.regionCont2, self.regionBroad1, self.regionBroad2 ]
        cbuttons=[self.bChangeCont1, self.bChangeCont2, self.bChangeBroad1, self.bChangeBroad2]
        idx = cbuttons.index(sender)
        self.displayWidg.selectSpecMask.copyMask(regions[idx])
        self.emit(SIGNAL("maskChanges"))
        
        
    def getSettings(self):
        out=[]
        out.append(self.comboRegions.currentIndex())
        out.append(self.boxInterpCont.isChecked())
        out.append(self.boxDisplay.isChecked())
        out.append(self.regionCont1.Limit())
        out.append(self.regionCont2.Limit())
        out.append(self.regionBroad1.Limit())
        out.append(self.regionBroad2.Limit())
        return out
        
    def loadSettings(self, set):
        self.regionCont1.setLimit(set[3])
        self.regionCont2.setLimit(set[4])
        self.regionBroad1.setLimit(set[5])
        self.regionBroad2.setLimit(set[6])
        if self.regionCont1.isEmpty()==False:
            self.bChangeCont1.setEnabled(True)
        if self.regionCont2.isEmpty()==False:
            self.bChangeCont2.setEnabled(True)
        if self.regionBroad1.isEmpty()==False:
            self.bChangeBroad1.setEnabled(True)
        if self.regionBroad2.isEmpty()==False:
            self.bChangeBroad2.setEnabled(True)
        self.comboRegions.setCurrentIndex(set[0])
        self.boxInterpCont.setChecked(set[1])
        self.boxDisplay.setChecked(set[2])
        
class modeWidget(QObject):
    def __init__(self, comboCorrMode, boxSFBFactor,  buttonEditHost,  boxIterations,  comboRegion,  radioRadius, boxRadius, parent=None):
        QObject.__init__(self)
        self.comboCorrMode = comboCorrMode
        self.boxSFBFactor = boxSFBFactor
        self.sfbFactor = float(self.boxSFBFactor.text())
        self.buttonEditHost = buttonEditHost
        self.boxIterations = boxIterations
        self.iteration = self.boxIterations.value()
        self.comboRegion = comboRegion
        self.radioRadius = radioRadius
        self.boxRadius = boxRadius
        self.radius = float(self.boxRadius.text())
        self.hostModel = hostContainer()
        self.parent = parent
                
        self.connect(self.comboCorrMode, SIGNAL("currentIndexChanged(const QString&)"), self.changeCorrectMode)
        self.connect(self.radioRadius, SIGNAL("toggled(bool)"), self.selectRadius)
        self.connect(self.buttonEditHost, SIGNAL("pressed()"), self.openHostDialog)
    
    def reset(self):
        self.comboRegion.setCurrentIndex(0)
        self.comboCorrMode.setCurrentIndex(0)
        self.changeCorrectMode(QString('None'))
        self.boxIterations.setValue(1)
        self.iterations=1
        self.boxRadius.setText('0.0')
        self.boxSFBFactor.setText('0.0')
        self.sfbFactor=0.0
        self.radioRadius.setChecked(False)
        self.boxRadius.setEnabled(False)
        
        
    def enable(self):
        self.comboCorrMode.setEnabled(True)
        self.boxSFBFactor.setEnabled(False)
        self.buttonEditHost.setEnabled(False)
        self.boxIterations.setEnabled(False)
        self.comboRegion.setEnabled(True)
        self.radioRadius.setEnabled(True)
        if self.radioRadius.isChecked()==True:
            self.boxRadius.setEnabled(True) 
        else:
            self.boxRadius.setEnabled(False)     
        
        
    def changeCorrectMode(self, mode):
        if mode == QString("None"):
            self.boxSFBFactor.setEnabled(False)
            self.buttonEditHost.setEnabled(False)
            self.boxIterations.setEnabled(False)
            self.boxIterations.setValue(1)
        elif mode == QString("Constant SFB"):
            self.boxSFBFactor.setEnabled(False)
            self.buttonEditHost.setEnabled(False)
            self.boxIterations.setEnabled(True)
        elif mode == QString("Manual factor"):
            self.boxSFBFactor.setEnabled(True)
            self.buttonEditHost.setEnabled(False)
            self.boxIterations.setEnabled(True)
        elif mode == QString("Host SFB model"):
            self.boxSFBFactor.setEnabled(False)
            self.buttonEditHost.setEnabled(True)
            self.boxIterations.setEnabled(True)
            
    def selectRadius(self, checked):
        if checked==True:
            self.boxRadius.setEnabled(True) 
        else:
            self.boxRadius.setEnabled(False) 
        
    def getSettings(self):    
        out=[]
        out.append(self.comboCorrMode.currentIndex())
        out.append(float(self.boxSFBFactor.text()))
        out.append(self.boxIterations.value())
        out.append(self.comboRegion.currentIndex())
        out.append(self.radioRadius.isChecked())
        out.append(float(self.boxRadius.text()))
        out.append(self.hostModel.getModels())
        return out   
            
    def loadSettings(self, settings):
        self.comboCorrMode.setCurrentIndex(settings[0])
        self.boxSFBFactor.setText(str(settings[1]))
        self.boxIterations.setValue(settings[2])
        self.comboRegion.setCurrentIndex(settings[3])
        self.radioRadius.setChecked(settings[4])
        self.boxRadius.setText(str(settings[5]))
        self.selectRadius(settings[4])
        self.hostModel.clear()
        for i in range(len(settings[6])):
            self.hostModel.add(hostModel(settings[6][i][0], settings[6][i][1], settings[6][i][2], settings[6][i][3], settings[6][i][4], settings[6][i][5], settings[6][i][6]))
        
        
    def openHostDialog(self):
        self.dialog = dlgHostModel.dlgHostModel(self.hostModel, self.parent)
        self.dialog.show()

            
class colorSchemeSpec(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()
        
        
    def default_values(self):
        self.spec1 = {'color':'k', 'width':1.0, 'style':'-'}
        self.spec2 = {'color':'r', 'width':1.0, 'style':'-'}
        self.slicer = {'color':'r', 'width':1.0, 'style':'-'}
        self.zoom = {'color':'r', 'width':3.0, 'style':'-'}
        self.select = {'color':'r', 'width':1.0, 'style':'-', 'hatch':'/', 'alpha':1.0}
        
    def update(self, spec1={}, spec2={}, slicer={}, zoom={}, select={}):
        if spec1!={}:
            for i in spec1.keys():
                self.spec1[i]=spec1[i]
        if spec2!={}:
            for i in spec2.keys():
                self.spec2[i]=spec2[i]
        
        if slicer!={}:
            for i in slicer.keys():
                self.slicer[i]=slicer[i]
                
        if zoom!={}:
            for i in zoom.keys():
                self.zoom[i]=zoom[i]
                
        if select!={}:
            for i in select.keys():
                self.select[i]=select[i]
        self.emit(SIGNAL("changed()"))
        
class colorSchemeSpax(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()
        
    def default_values(self):
        self.image = {'colormap':'hot', 'reversed':False, 'interpolation':'nearest', 'radius':1.0, 'scaling':'Linear'}
        self.marker = {'color':'b', 'width':1.0, 'hatch':'None', 'alpha':0.5}
        self.select = {'color':'r',  'width':1.0, 'hatch':'/', 'alpha':0.5}
        
        
    def update(self, image={}, marker={}, select={}):
        if image!={}:
            for i in image.keys():
                self.image[i]=image[i]
                
        if marker!={}:
            for i in marker.keys():
                self.marker[i]=marker[i]
        
        if select!={}:
            for i in select.keys():
                self.select[i]=select[i]
        self.emit(SIGNAL("changed()"))        
    
class colorsQSOSpax(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()
        
    def default_values(self):
        self.QSO = {'color':'r', 'width':1.0, 'hatch':'/', 'alpha':0.5}
        self.EELR = {'color':'g',  'width':1.0, 'hatch':'/', 'alpha':0.5}
        
    def update(self, QSO={}, EELR={}):
        if QSO!={}:
            for i in QSO.keys():
                self.QSO[i]=QSO[i]
                
        if EELR!={}:
            for i in EELR.keys():
                self.EELR[i]=EELR[i]
        self.emit(SIGNAL("changed()"))     


class colorsQSOSpec(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.default_values()
        
    def default_values(self):
        self.cont = {'color':'b', 'width':1.0, 'hatch':'None', 'alpha':0.5}
        self.broad = {'color':'r',  'width':1.0, 'hatch':'None', 'alpha':0.5}
        
    def update(self, cont={}, broad={}):
        if cont!={}:
            for i in cont.keys():
                self.cont[i]=cont[i]                
        if broad!={}:
            for i in broad.keys():
                self.broad[i]=broad[i]
        self.emit(SIGNAL("changed()"))      
        
        
class hostModel(object):
    def __init__(self, mag, x, y, re, sersic, e, theta):
        self.mag = mag
        self.x = x
        self.y = y
        self.re = re
        self.sersic = sersic
        self.e = e
        self.theta = theta
        
    def getModel(self):
        return [self.mag, self.x, self.y, self.re, self.sersic, self.e, self.theta]
        
class hostContainer(object):
    
    def __init__(self):
        self.__hostModels=[]
        self.__hostFromId= {}
        self.__empty=True
        self.__center=[]
        self.__dim=[]
        self.selected=None
    
    def __len__(self):
        return len(self.__hostModels)
    
    def __iter__(self):
        for pair in iter(self.__hostModels):
            yield pair
            
    def clear(self):
        self.__hostModels=[]
        self.__hostFromId= {}
        self.__empty=True
        self.selected=None
        
    def setCenter(self, center):
        self.center=center
        
    def setDim(self, dim):
        self.dim=dim
        
    def add(self, hostModel):
        if id(hostModel) in self.__hostFromId:
            return False
        else:
            self.__hostModels.append(hostModel)
            self.__hostFromId[id(hostModel)] = hostModel
            self.__empty=False
    
    def delete(self, hostModel):
        if id(hostModel) not in self.__hostFromId:
            return False
        else:
            for i in range(len(self.__hostModels)):
                if self.__hostModels[i] == hostModel:
                    del self.__hostModels[i]
                    del self.__hostFromId[id(hostModel)]
                    break
            return True
            
    def returnModel(self, index):
        return self.__hostModels[index]
    
    def models(self):
        return len(self.__hostModels)
        
    def getModels(self):
        hosts=[]
        for i in range(len(self.__hostModels)):
            hosts.append(self.__hostModels[i].getModel())
        return hosts
    
    def copyContainer(self, container):
        self.clear()
        for i in range(len(container)):
            self.add(container.__hostModels[i])
        
    def setSelected(self, hostModel):
        if hostModel==None:
            self.selected == None
        else:
            self.selected = self.__hostFromId[id(hostModel)]
            
    def createHostModel(self):
        if len(self.__hostModels)!=0 and self.dim!=[] and self.center!=[]:
            array = numpy.zeros(self.dim, dtype=numpy.float32)
            for i in range(len(self.__hostModels)):
                sersic = host_profiles.Sersic(self.dim, self.center[1]+self.__hostModels[i].x, self.center[0]+self.__hostModels[i].y, self.__hostModels[i].mag, self.__hostModels[i].sersic, self.__hostModels[i].re,self.__hostModels[i].e, self.__hostModels[i].theta/180.0*numpy.pi)
                array = array + sersic.array
            return [True, array]
        else:
            return [False, []]

    def updateSelected(self, hostModel):
        for i in range(len(self.__hostModels)):
                if self.__hostModels[i] == self.selected:
                    self.__hostModels[i]=hostModel
                    del self.__hostFromId[id(self.selected)]
                    self.__hostFromId[id(hostModel)]=hostModel
                    self.selected=hostModel
                    break
        
class setMonteCarlo(object):
    def __init__(self, dir='', var_name = '',  prefix='',  simulations=0, width_random=0.0, wavelength_start=None,  wavelength_end = None):
        self.dir = dir
        self.var_name = var_name
        self.prefix = prefix
        self.simulations = simulations
        self.width_random = width_random
        self.wavelength_start = wavelength_start
        self.wavelength_end = wavelength_end
    
    def getSettings(self):
        return [self.dir, self.var_name, self.prefix, self.simulations, self.width_random, self.wavelength_start, self.wavelength_end]
        
    def loadSettings(self, settings):
        self.dir = settings[0]
        self.var_name = settings[1]
        self.prefix = settings[2]
        self.simulations = settings[3]
        self.width_random = settings[4]
        self.wavelength_start = settings[5]
        self.wavelength_end =  settings[6]
    

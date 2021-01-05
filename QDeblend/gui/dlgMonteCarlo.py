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

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from own_exceptions import *
import ui_dlgMonteCarlo
import dlgEditHostModel

__version__ = '0.1.2'

class dlgMonteCarlo(QDialog, ui_dlgMonteCarlo.Ui_dlgMonteCarlo):
    def __init__(self, parent, setMonte):
        super(dlgMonteCarlo,  self ).__init__(parent)
        self.setupUi(self)
        self.setMonte = setMonte
        self.directory = self.setMonte.dir
        self.lineDir.setText(self.directory)
        self.var_name = self.setMonte.var_name
        self.lineVariance.setText(self.var_name)
        self.prefix = self.setMonte.prefix
        self.linePrefix.setText(self.prefix)
        self.parent = parent
        if self.setMonte.wavelength_start== None or self.setMonte.wavelength_end==None:
            wave = parent.inputCube.wave
            step = wave[1]-wave[0]
            self.dStart.setValue(wave[0]-step/2)
            self.dEnd.setValue(wave[-1]+step/2)
            self.setMonte.wavelength_start = wave[0]-step/2
            self.setMonte.wavelength_end = wave[1]+step/2
        else:
            self.dStart.setValue(self.setMonte.wavelength_start)
            self.dEnd.setValue(self.setMonte.wavelength_end)
        if self.setMonte.simulations!=0:
            self.dBoxSimul.setValue(self.setMonte.simulations)
        if self.setMonte.width_random!=0:
            self.dBoxRandom.setValue(self.setMonte.width_random)   
        
        self.connect(self.bDirSelect, SIGNAL('pressed()'), self.getDir)
        self.connect(self.bVarSelect, SIGNAL('pressed()'), self.openVariance)
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.startMonteCarlo)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)
        
    def getDir(self):
        dir = QFileDialog.getExistingDirectory(parent=self, caption = 'Select Directory', directory=os.getcwd())
        if not dir=='':
            self.lineDir.setText(dir)
            self.directory=dir
            
    
    def openVariance(self):
        var_name = QFileDialog.getOpenFileName(self,
 caption="Open IFU Variance Cube", directory=os.getcwd(), filter="Fits Files (*.fit *.fits)")
        if not var_name =='':
            self.lineVariance.setText(var_name)
            self.var_name=str(var_name)
            
    def startMonteCarlo(self):
        if self.linePrefix.text()=='':
            warning = QMessageBox.critical(self,'Run-time Error', 'No Prefix specified!')
        else:
            if self.directory=='':
                warning = QMessageBox.critical(self,'Run-time Error', 'No Directory selected!')
            else:
                if self.var_name=='':
                    warning = QMessageBox.critical(self,'Run-time Error', 'No Variance Cube loaded!')
                else:
                    progress = QProgressDialog('Monte Carlo Simulations', '', 0, self.dBoxSimul.value()-1, parent=self)
                    progress.forceShow()
                    progress.setValue(0)
                    progress.setLabelText('Perocessing Cube %i/%i'%(1, self.dBoxSimul.value()))
                    try:
                        self.parent.inputCube.loadFitsVarCube(self.var_name)
                        for i in range(self.dBoxSimul.value()):
                                progress.setValue(i)
                                progress.setLabelText('Perocessing Cube %i/%i'%(i+1, self.dBoxSimul.value()))
                                randomCube = self.parent.inputCube.errorRandomCube()
                                broad1 =  self.parent.regionsSpecWidg.regionBroad1.getMask(self.parent.inputCube.wave,self.dBoxRandom.value())
                                cont1 =  self.parent.regionsSpecWidg.regionCont1.getMask(self.parent.inputCube.wave,self.dBoxRandom.value())
                                if self.parent.comboBoxRegions.currentIndex()==0:
                                    broad_region = [broad1, broad1]
                                    cont_region = [cont1, cont1]
                                elif self.parent.comboBoxRegions.currentIndex()==1:
                                    broad2 =   self.parent.regionsSpecWidg.regionBroad2.getMask(self.parent.inputCube.wave,self.dBoxRandom.value())
                                    broad_region = [broad1, broad2]
                                    cont_region = [cont1, cont1]
                                elif self.parent.comboBoxRegions.currentIndex()==2:
                                    cont2 =   self.parent.regionsSpecWidg.regionCont2.getMask(self.parent.inputCube.wave,self.dBoxRandom.value())
                                    broad_region = [broad1, broad1]
                                    cont_region = [cont1, cont2]
                                elif self.parent.comboBoxRegions.currentIndex()==3:
                                    broad2 =   self.parent.regionsSpecWidg.regionBroad2.getMask(self.parent.inputCube.wave,self.dBoxRandom.value())
                                    cont2 =   self.parent.regionsSpecWidg.regionCont2.getMask(self.parent.inputCube.wave,self.dBoxRandom.value())
                                    broad_region = [broad1, broad2]
                                    cont_region = [cont1, cont2]
                                
                                iter = self.parent.modeWidg.boxIterations.value()
                                mode = self.parent.modeWidg.comboCorrMode.currentIndex()
    
                                qso_mask = self.parent.regionsSpaxWidg.getQSOMask()
                                if mode==0:
                                    eelr_mask=None
                                    iter = 1
                                    factor=None
                                    hostimage=None
                                elif mode==1:
                                    eelr_mask=self.parent.regionsSpaxWidg.getEELRMask()
                                    factor = None
                                    hostimage=None
                                elif mode==2:
                                    eelr_mask=self.parent.regionsSpaxWidg.getEELRMask()
                                    factor = float(self.parent.lineEditSFBFactor.text())
                                    hostimage=None
                                elif mode==3:
                                    eelr_mask=self.parent.regionsSpaxWidg.getEELRMask()
                                    factor = None
                                    hostmodel = self.parent.modeWidg.hostModel.createHostModel()
                                    if hostmodel[0]==True:
                                        hostimage = hostmodel[1]
                                    else:
                                        raise EmptyHostImage
                                else:
                                    factor=None
                                mode_region=str(self.parent.comboBoxRegionMeasure.currentText())
                                
                                if self.parent.modeWidg.radioRadius.isChecked()==True:
                                    radius = float(self.parent.modeWidg.boxRadius.text())
                                else:
                                    radius = None
                                center = self.parent.regionsSpaxWidg.centQSO
                                subtracted = randomCube.deblendQSOHost(center, qso_mask, broad_region, cont_region , iter, mode_region,  eelr_mask=eelr_mask, interpolate_cont=self.parent.checkBoxInterpCont.isChecked(), subtract_region=None, radius=radius,  host_image=hostimage, factor=factor, showProgress=None)
                                subtracted[0].subCube(self.dStart.value(), self.dEnd.value())
                                subtracted[1].subCube(self.dStart.value(), self.dEnd.value())
                                subtracted[0].writeFitsData(str(self.directory)+'/'+str(self.linePrefix.text())+'_EELR_sim_%i.fits'%(i+1))
                                subtracted[1].writeFitsData(str(self.directory)+'/'+str(self.linePrefix.text())+'_QSO_sim_%i.fits'%(i+1))
                                
                    except UnfilledMaskError, error:
                        progress.setAutoClose(True)
                        warning = QMessageBox.critical(self,'Run-time Error', error.msg)
    
                    except EmptyHostImage, error:
                        progress.setAutoClose(True)
                        warning = QMessageBox.critical(self,'Run-time Error', error.msg)
                    except IFUcubeIOError, error:
                        progress.setAutoClose(True)
                        warning = QMessageBox.critical(self,'Run-time Error', error.msg)
                    self.setMonte.loadSettings([str(self.directory), str(self.var_name), str(self.linePrefix.text()), self.dBoxSimul.value(),  self.dBoxRandom.value(),  self.dStart.value() , self.dEnd.value() ])
                self.accept()

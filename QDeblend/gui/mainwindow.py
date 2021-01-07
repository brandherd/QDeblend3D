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

import sys
import os
import pickle
import numpy
import math
from astropy.io import fits as pyfits
import matplotlib
matplotlib.use('Qt4Agg')
from QDeblend.process import IFU_cube
from QDeblend.widgets import widgets
from QDeblend.widgets import color_schema
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QDeblend.ui import ui_mainwindow
import dlgColorProperties
import dlgSaveCubes
import dlgMonteCarlo
import onlineHelp
import QDeblend

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    """
    Primary class of QDeblend3D initialising the main GUI, setup its components and controlling the user actions.
    
    Attributes are:
        cubeinname->name of the input cube, String object
        cubeSlider->Qt3 Slider object
        inputcube -> IFU_cube object
        EELRcube -> IFU_cube object
        QSOcube -> IFU_cube obejct
        displayOutCube -> IFU_cube obejct
        spaxWidg1-> Spaxel Widget object
        spaxWidg2-> Spaxel Widget object
        specWidg-> Spectrum Widget object
        modeWidg->Mode Widget object
        regionsSpaxWidget-> Spaxel Regions Widget object
        regionsSpecWidget-> Spectrum Regions Widget object
        LWImg ->Limit Widget Object for the Spaxel Widgets
        LWSpec ->Limit Widget Object for the Spectrum Widget
        MonteSettings->Monte Carlo definition Object 
        
    Methods are:
        about(self) -> Display basic information about QDeblend3d
        aboutQt(self) -> Display basic information about Qt3 from Trolltech
        changeMouseMode(self) -> setup the correct Mouse Mode, e.g. after a triggering event, depending on the sender
        changeOutCube(self) -> switch between the EELR and QSO cube 
        changedSlider(self,value(int)) -> change the Slider and displayed slice of the Datacube
        getSpaxPos(self,xdata(float),ydata(float)) -> help function do convert float window coordinates into indicies of the cube
        loadSession(self,file_name(string))->load a previously stored session from file
        onlineManual(self)->display the online manual resources
        saveCubes(self)->display Save Dialog to store the EELR and QSO cube to disc
        saveSession(self)-> display Save Dialog to store the current Session in a file to disc
        ....
    """

    
    def __init__(self, parent=None, file=''):
        super(MainWindow, self ).__init__(parent)
        self.setupUi(self)
        self.cubeinname=''
        self.inputCube = IFU_cube.IFUcube()
        self.EELRcube = IFU_cube.IFUcube()
        self.QSOcube = IFU_cube.IFUcube()
        self.LWSpec = widgets.limitWidget(self.lineEditMinSpec, self.lineEditMaxSpec, self.checkBoxAutoSpec)
        self.LWImg = widgets.limitWidget(self.lineEditMinImg, self.lineEditMaxImg, self.checkBoxAutoImg)
        self.specWidg = self.bothSpectrumWidget
        self.specWidg.setLimitsWidget(self.LWSpec)
        self.spaxWidg1 = self.inputSpaxelWidget
        self.spaxWidg1.setLimitsWidget(self.LWImg)
        self.spaxWidg2 = self.outputSpaxelWidget
        self.spaxWidg2.setLimitsWidget(self.LWImg)
        self.regionsSpaxWidg = widgets.regionsSpaxWidget(self.spinBoxQSORegionSize,
                                                         self.spinBoxEELRRegionWidth,
                                                         self.radioButtonRegionRegular,
                                                         self.radioButtonRegionManual,
                                                         self.checkBoxDisplayMask,
                                                         self.buttonQSOSaveMask,
                                                         self.buttonQSOChangeMask,
                                                         self.buttonEELRSaveMask,
                                                         self.buttonEELRChangeMask,
                                                         color_schema.colorsQSOSpax(), parent=self)
        self.regionsSpecWidg = widgets.regionsSpecWidget(self.comboBoxRegions,
                                                         self.buttonSaveBroad1,
                                                         self.buttonSaveBroad2,
                                                         self.buttonChangeBroad1,
                                                         self.buttonChangeBroad2,
                                                         self.buttonSaveCont1,
                                                         self.buttonSaveCont2,
                                                         self.buttonChangeCont1,
                                                         self.buttonChangeCont2,
                                                         self.checkBoxInterpCont,
                                                         self.checkBoxShowRegion,
                                                         color_schema.colorsQSOSpec())
        self.modeWidg = widgets.modeWidget(self.comboBoxCorrMode, self.lineEditSFBFactor,
                                           self.pushButtonEditHostModel,
                                           self.spinBoxIterations,
                                           self.comboBoxRegionMeasure,
                                           self.radioButtonRadius,
                                           self.lineEditRadius)
        self.MonteSettings = dlgMonteCarlo.setMonteCarlo()
        
        self.connect(self.actionSetColours, SIGNAL("triggered()"), self.setColourScheme)
        self.connect(self.actionSave_Configuration, SIGNAL("triggered()"), self.saveSession)
        self.connect(self.actionLoad_Configuration, SIGNAL("triggered()"), self.loadSession)
        self.connect(self.actionLoad_Cube, SIGNAL("triggered()"), self.OpenFile)
        self.connect(self.pushButtonSaveResults,  SIGNAL("clicked()"), self.saveCubes)
        self.connect(self.actionSave_Results,  SIGNAL("triggered()"), self.saveCubes)
        self.connect(self.actionMonte_Carlo_run,  SIGNAL("triggered()"), self.startMonteCarlo)
        self.connect(self.verticalSliderSlice, SIGNAL("valueChanged(int)"), self.changedSlider)

        self.connect(self.spaxWidg1, SIGNAL("mouse_press_event"), self.spaxFigMousePress)
        self.connect(self.spaxWidg2, SIGNAL("mouse_press_event"), self.spaxFigMousePress)
        self.connect(self.spaxWidg1, SIGNAL("mouse_move_event"), self.spaxFigMouseMove)
        self.connect(self.spaxWidg2, SIGNAL("mouse_move_event"), self.spaxFigMouseMove)
        self.connect(self.spaxWidg1, SIGNAL("mouse_release_event"), self.spaxFigMouseRelease)
        self.connect(self.spaxWidg2, SIGNAL("mouse_release_event"), self.spaxFigMouseRelease)
        self.connect(self.specWidg, SIGNAL("mouse_press_event"), self.specFigMousePress)
        self.connect(self.specWidg, SIGNAL("mouse_move_event"), self.specFigMouseMove)
        self.connect(self.specWidg, SIGNAL("mouse_release_event"), self.specFigMouseRelease)

        self.connect(self.radioButtonModeView, SIGNAL("clicked()"), self.changeMouseMode)
        self.connect(self.radioButtonModeZoom, SIGNAL("clicked()"), self.changeMouseMode)
        self.connect(self.radioButtonModeSelect, SIGNAL("clicked()"), self.changeMouseMode)

        self.connect(self.radioButtonHost, SIGNAL("clicked()"), self.changeOutCube)
        self.connect(self.radioButtonQSO, SIGNAL("clicked()"), self.changeOutCube)
        
        self.connect(self.regionsSpecWidg, SIGNAL("maskChanges"), self.toggleSelectMouse)
        self.connect(self.pushButtonStartSubtract, SIGNAL("clicked()"), self.startSubtractQSO)
        self.connect(self.actionSubtraction,  SIGNAL("triggered()"), self.startSubtractQSO)
        self.connect(self.actionSetQSOcentre,  SIGNAL("triggered()"), self.setQSOcent)
        
        self.connect(self.actionManual, SIGNAL("triggered()"), self.onlineManual)
        self.connect(self.actionAboutQt, SIGNAL("triggered()"), self.aboutQt)
        self.connect(self.actionAbout, SIGNAL("triggered()"), self.about)
        
        if file!='':
            if '.fits' in file or '.fit' in file or '.fits.gz' in file:
                self.OpenFile(file)
            elif '.q3d' in file:
                self.loadSession(file)
            else:
                raise IOError('No correct file selected for import. Please review your selection.')
        
    def OpenFile(self, filename=''):
        if filename=='':
            self.cubeinname = QFileDialog.getOpenFileName(self, caption="Open IFU Cube", directory=os.getcwd(),
                                                          filter="Fits Files (*.fit *.fits *fits.gz)")
        else:
            self.cubeinname=filename
        if self.cubeinname!='':
            try:
                ## Load Cube
                self.inputCube.loadFitsCube(str(self.cubeinname))
                self.lineCubeIn.setText(QString(self.cubeinname.split('/')[-1]))
                self.EELRcube.emptyCube()
                self.QSOcube.emptyCube()
                self.spaxWidg1.clearWidget()
                self.spaxWidg2.clearWidget()
                self.specWidg.clearWidget()
                self.modeWidg.reset()
                self.radioButtonQSO.setEnabled(False)
                self.radioButtonHost.setEnabled(False)    
                try:
                    self.regionsSpecWidg.clearMasks()
                except:
                    pass
                try:
                    self.regionsSpaxWidg.clearMasks()
                except:
                    pass   
                try:
                    del self.cubeSlider
                except:
                    pass
                
                ## Init Slider
                self.cubeSlider = widgets.sliderWidget(self.verticalSliderSlice, self.labelSlice, self.inputCube)
                
                ## Init first spectral image and init the selected Spaxel to 0,0
                self.spaxWidg1.initImage(self.inputCube.dataCube[0, :, :])
                self.spaxWidg1.initShowSpax(0, 0, True)
                self.spaxWidg1.initSpaxMask(False)
                self.LWImg.setEnabled(True)
                self.pushButtonSaveResults.setEnabled(False)
                self.actionSave_Results.setEnabled(False)
                self.menuStart.setEnabled(True)
                self.actionSetQSOcentre.setEnabled(True)
                
                ## Set limits on EELR and QSO regions and initialize Masks
                self.regionsSpaxWidg.initLimits(self.inputCube)
                self.regionsSpaxWidg.setupMasks(self.spaxWidg1)
                self.regionsSpecWidg.setupMasks(self.specWidg)

                ## Initialize spaxel spectrum and view line and set current xlimits of spectrum
                self.specWidg.initSpec1(self.inputCube.wave, spec1=self.inputCube.dataCube[:, 0, 0])
                self.specWidg.initViewLine(self.inputCube.wave[0])
                self.specWidg.initSpecMask(waveLimit=None)
                self.specWidg.setXLim((self.inputCube.wave[0], self.inputCube.wave[-1]))
                self.LWSpec.setEnabled(True)
                self.bothSpectrumWidget.axes.set_xlabel('wavelength [$\AA$]',  fontsize=12)
                
                self.modeWidg.enable()
                self.toggleViewMouse()          
                self.checkBoxModeBoth.setChecked(False)
                self.checkBoxModeBoth.setEnabled(False)
                self.radioButtonModeView.setEnabled(True)
                self.radioButtonModeZoom.setEnabled(True)
                self.radioButtonModeSelect.setEnabled(True)
                self.groupBoxSelectRegions.setEnabled(True)
                self.groupBoxSpecRegions.setEnabled(True)
                self.groupBoxMethod.setEnabled(True)
                
                self.modeWidg.hostModel.setCenter(self.regionsSpaxWidg.centQSO[1])
                self.modeWidg.hostModel.setDim((self.inputCube.yDim, self.inputCube.xDim))
                
            except IOError:
                warning = QMessageBox.critical(self,'Fits File I/O Error', 'This file is not a 3D cube fits file!')

    def saveCubes(self):
        dialog = dlgSaveCubes.dlgSaveCubes(self.QSOcube, self.EELRcube, parent=self)
        dialog.show()
        
    def saveSession(self):  
        file_name = QFileDialog.getSaveFileName(self, caption="Save Session File", directory=os.getcwd(),
                                                filter="Q3D session (*.q3d)")
        out1=self.modeWidg.getSettings()
        out2 = self.regionsSpecWidg.getSettings()
        out3 = self.regionsSpaxWidg.getSettings()
        out4 = self.MonteSettings.getSettings()
        pickle_objects = [__version__, self.cubeinname, out1, out2, out3, out4]
        if file_name!='':
            file = open(file_name, 'w')
            pickle.dump(pickle_objects, file)
            file.close()
        
    def loadSession(self, file_name=''):
        if file_name=='':
            file_name = QFileDialog.getOpenFileName(self, caption="Open Session File", directory=os.getcwd(),
                                                    filter="Q3D session (*.q3d)")
        if file_name!='':
            file = open(file_name, 'r')
            list = pickle.load(file)
            file.close()
            if list[0]>='0.1.0':
                self.OpenFile(list[1])
                self.modeWidg.loadSettings(list[2])
                self.regionsSpecWidg.loadSettings(list[3])
                self.regionsSpaxWidg.loadSettings(list[4])
                self.MonteSettings.loadSettings(list[5])
            else:
                QMessageBox.critical(self, 'Error Message', 'Session file was stored with a incompatible '
                                                            'QDeblend3D Version!\n Cannot load Session File...')

    def getSpaxPos(self, xdata, ydata):
        sx = math.floor(xdata+0.5)
        if sx-xdata > 0.5:
            sx+=1
        sy = math.floor(ydata + 0.5)
        if sy-ydata > 0.5:
            sy+=1
        return int(sx), int(sy)
        
    def spaxFigMousePress(self, button, x, y, xdata, ydata):
        sender = self.sender()
        both = self.checkBoxModeBoth.isChecked()
        if (not xdata is None) and (not ydata is None):
            pos = self.getSpaxPos(xdata, ydata)
            
        if (button == 1) and self.radioButtonModeView.isChecked() and (not xdata is None) and (not ydata is None):
            if both:
                if not self.inputCube.empty and not self.EELRcube.empty:
                    spec1 = self.inputCube.dataCube[:, int(pos[1]), int(pos[0])]
                    spec2 = self.displayOutCube.dataCube[:, int(pos[1]), int(pos[0])]
                    self.specWidg.updateSpec1(self.inputCube.wave, spec1=spec1, limits=False)
                    self.specWidg.updateSpec2(self.displayOutCube.wave, spec2=spec2, limits=False)
                    min = numpy.min([numpy.min(spec1), numpy.min(spec2)])
                    max = numpy.max([numpy.max(spec1), numpy.max(spec2)])
                    auto = self.LWSpec.isAuto()
                    if auto:
                        self.specWidg.setYLim(min, max)
                        self.LWSpec.setLimits(min, max)
                    self.spaxWidg1.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
                    self.spaxWidg2.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
                
            elif  sender == self.spaxWidg1 and not self.inputCube.empty:
                spec1 = self.inputCube.dataCube[:, pos[1], pos[0]]
                self.specWidg.updateSpec1(self.inputCube.wave, spec1=spec1)
                if self.specWidg.spec2 is not None and self.specWidg.spec2_vis:
                    self.specWidg.setVisibleSpec2(False)
                self.spaxWidg1.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
                
            elif  sender == self.spaxWidg2 and not self.EELRcube.empty:
                spec2 = self.displayOutCube.dataCube[:, pos[1], pos[0]]
                self.specWidg.updateSpec2(self.displayOutCube.wave, spec2=spec2)
                if self.specWidg.spec1 is not None and self.specWidg.spec1_vis:
                    self.specWidg.setVisibleSpec1(False)
                self.spaxWidg2.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
            
        if (button == 1) and self.radioButtonModeZoom.isChecked()  and (xdata is not None) and (ydata is not None):
            if both:
                self.spaxWidg1.initZoomBox(pos[0], pos[1])
                self.spaxWidg2.initZoomBox(pos[0], pos[1])
            else:    
                sender.initZoomBox(pos[0], pos[1])

        if (button == 1) and self.radioButtonModeSelect.isChecked() and (xdata is not None) and (ydata is not None):
            if sender == self.spaxWidg1 and not self.inputCube.empty:
                if self.spaxWidg1.selectSpaxMask.isMasked((pos[1], pos[0])):
                    self.spaxWidg1.selectSpaxMask.unmaskPixel((pos[1], pos[0])) 
                else:
                    self.spaxWidg1.selectSpaxMask.maskPixel((pos[1],  pos[0])) 
                spec = self.inputCube.extractSpecMask(self.spaxWidg1.selectSpaxMask.mask.mask, mode='sum')
                self.specWidg.updateSpec1(self.inputCube.wave, spec1=spec)
     
        if (button == 3) and self.radioButtonModeSelect.isChecked():
            if sender == self.spaxWidg1 and not self.inputCube.empty:
                self.spaxWidg1.selectSpaxMask.emptyMask()
                spec = numpy.zeros(self.inputCube.wDim, dtype=numpy.float32)
                self.specWidg.updateSpec1(self.inputCube.wave, spec1=spec)
        
    def spaxFigMouseMove(self, button, x, y, xdata, ydata):
        sender = self.sender()
        both = self.checkBoxModeBoth.isChecked()
        
        if (xdata is not None) and (ydata is not None):
            pos = self.getSpaxPos(xdata, ydata)
        
        if (button == 1) and self.radioButtonModeView.isChecked() and (xdata is not None) and (not ydata is not None):
            if both:
                if not self.inputCube.empty and not self.EELRcube.empty:
                    spec1 = self.inputCube.dataCube[:, int(pos[1]), int(pos[0])]
                    spec2 = self.displayOutCube.dataCube[:, int(pos[1]), int(pos[0])]
                    self.specWidg.updateSpec1(self.inputCube.wave, spec1=spec1)
                    self.specWidg.updateSpec2(self.displayOutCube.wave, spec2=spec2)
                    min = numpy.min([numpy.min(spec1), numpy.min(spec2)])
                    max = numpy.max([numpy.max(spec1), numpy.max(spec2)])
                    auto = self.LWSpec.isAuto()
                    if auto:
                        self.specWidg.setYLim(min, max)
                        self.LWSpec.setLimits(min, max)
                    self.spaxWidg1.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
                    self.spaxWidg2.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
                
            elif  sender == self.spaxWidg1 and not self.inputCube.empty:
                spec1 = self.inputCube.dataCube[:, int(pos[1]), int(pos[0])]
                self.specWidg.updateSpec1(self.inputCube.wave, spec1=spec1)
                self.spaxWidg1.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
                
            elif  sender == self.spaxWidg2 and not self.EELRcube.empty:
                spec2 = self.displayOutCube.dataCube[:, int(pos[1]), int(pos[0])]
                self.specWidg.updateSpec2(self.displayOutCube.wave, spec2=spec2)
                self.spaxWidg2.moveSelectSpax(pos[0]-0.5, pos[1]-0.5)
            
        if (button == 1) and self.radioButtonModeZoom.isChecked() and (xdata is not None) and (ydata is not None):
            if both:
                self.spaxWidg1.resizeZoomBox(pos[0], pos[1])
                self.spaxWidg2.resizeZoomBox(pos[0], pos[1])
            else:
                sender.resizeZoomBox(pos[0], pos[1])
        
        if not self.inputCube.empty and (button == 1) and self.radioButtonModeSelect.isChecked()  and \
                (xdata is not None) and (ydata is not None):
            if both:
                pass
            elif sender == self.spaxWidg1 and not self.inputCube.empty:
                if not self.spaxWidg1.selectSpaxMask.isMasked((pos[1], pos[0])):
                    self.spaxWidg1.selectSpaxMask.maskPixel((pos[1],  pos[0])) 
                spec = self.inputCube.extractSpecMask(self.spaxWidg1.selectSpaxMask.mask.mask, mode='sum')
                self.specWidg.updateSpec1(self.inputCube.wave, spec1=spec)
            
    def spaxFigMouseRelease(self, button, x, y, xdata, ydata):
        both = self.checkBoxModeBoth.isChecked()
        sender = self.sender()
        if (button == 1) and self.radioButtonModeZoom.isChecked():
            limits = sender.getZoomLimit()
            if both:
                if limits is not None:
                    self.spaxWidg1.axes.set_xlim(limits[0], limits[1])
                    self.spaxWidg1.axes.set_ylim(limits[2], limits[3])
                    self.spaxWidg1.delZoomBox()
                    self.spaxWidg2.axes.set_xlim(limits[0], limits[1])
                    self.spaxWidg2.axes.set_ylim(limits[2], limits[3])
                    self.spaxWidg2.delZoomBox()
            else:
                if limits is not None:
                    sender.axes.set_xlim(limits[0], limits[1])
                    sender.axes.set_ylim(limits[2], limits[3])
                    sender.delZoomBox()
            
        if (button == 3) and self.radioButtonModeZoom.isChecked():
            if both:
                self.spaxWidg1.zoomOut()
                self.spaxWidg2.zoomOut()
            else:
                sender.zoomOut()
            
    def specFigMousePress(self, button, x, y, xdata, ydata):
        if (xdata is not None) and (ydata is not None):
            pos = self.getSpaxPos(xdata, ydata)
        
        if not self.inputCube.empty and (button == 1) and self.radioButtonModeView.isChecked() and \
                (xdata is not None) and (ydata is not None):
            s = numpy.fabs(self.inputCube.wave-xdata)
            slice = numpy.argsort(s)[0]
            self.verticalSliderSlice.setValue(slice+1)
            
        if not self.inputCube.empty and (button == 1) and self.radioButtonModeZoom.isChecked() and \
                (xdata is not None) and (ydata is not None):
            self.specWidg.initZoomBox(xdata, ydata)
        
        if not self.inputCube.empty and (button == 3) and self.radioButtonModeSelect.isChecked():
            self.specWidg.selectSpecMask.emptyRegion()
            
    def specFigMouseMove(self,button, x, y, xdata, ydata):
        if not self.inputCube.empty == False and (button == 2) and self.radioButtonModeView.isChecked() and \
                (xdata is not None) and (ydata is not None):
            s = numpy.fabs(self.inputCube.wave - xdata)
            slice = numpy.argsort(s)[0]
            self.verticalSliderSlice.setValue(slice + 1)
            
        if not self.inputCube.empty and (button == 1) and self.radioButtonModeZoom.isChecked()\
                and (xdata is not None) and (ydata is not None):
            self.specWidg.resizeZoomBox(xdata,  ydata)
            
        if not self.inputCube.empty and (button == 1) and self.radioButtonModeSelect.isChecked()==True and \
                (xdata is not None) and (ydata is not None):
            if self.specWidg.pickedSpecRegion[0] and self.specWidg.pickedSpecRegion[1].waveLimit is not None:
                if self.specWidg.pickedSpecRegion[2] == 'left':
                    self.specWidg.pickedSpecRegion[1].setLimit([xdata, self.specWidg.pickedSpecRegion[1].waveLimit[1]])
                else:
                    self.specWidg.pickedSpecRegion[1].setLimit([self.specWidg.pickedSpecRegion[1].waveLimit[0], xdata])
            elif not self.specWidg.changeSelectSpec:
                self.specWidg.selectSpecMask.setLimit([xdata, xdata])   
                self.specWidg.changeSelectSpec=True
            else:
                limits = self.specWidg.selectSpecMask.Limit()
                if xdata>=limits[0]:
                    self.specWidg.selectSpecMask.setLimit([limits[0], xdata])
                else:
                    self.specWidg.selectSpecMask.setLimit([xdata, limits[1]])   
            limits = self.specWidg.selectSpecMask.Limit()       
            img = self.inputCube.extractImage(limits[0], limits[1])
            self.spaxWidg1.updateImage(img)

    def specFigMouseRelease(self, button, x, y, xdata, ydata):
        if not self.inputCube.empty and (button == 1) and self.radioButtonModeZoom.isChecked():
            limits = self.specWidg.getZoomLimit()
            if limits is not None:
                self.specWidg.axes.set_xlim(limits[0], limits[1])
                self.specWidg.axes.set_ylim(limits[2], limits[3])
                self.LWSpec.setLimits(limits[2], limits[3])
                self.LWSpec.setManual()
                self.specWidg.delZoomBox()
            
        if not self.inputCube.empty and (button == 3) and self.radioButtonModeZoom.isChecked():
            self.specWidg.zoomOut()
            self.LWSpec.setAuto()
        
        if not self.inputCube.empty and (button == 1) and self.radioButtonModeSelect.isChecked():
            self.specWidg.changeSelectSpec=False

    def changedSlider(self, value):        
        if not self.inputCube.empty and self.radioButtonModeView.isChecked():
            try:
                self.cubeSlider.updateSlider(value)
                self.spaxWidg1.updateImage(self.inputCube.dataCube[value-1, :, :])
                if not self.EELRcube.isEmpty():
                    self.spaxWidg2.updateImage(self.displayOutCube.dataCube[value-1, :, :], limits=False)
                self.specWidg.updateViewLine(self.inputCube.wave[value-1])
            except:
                pass

    def changeOutCube(self):
        sender = self.sender()
        if sender == self.radioButtonHost:
            self.radioButtonHost.setChecked(True)
            self.radioButtonQSO.setChecked(False)
        elif sender == self.radioButtonQSO:
            self.radioButtonHost.setChecked(False)
            self.radioButtonQSO.setChecked(True)
            
        if self.radioButtonHost.isChecked() == True:
            self.displayOutCube = self.EELRcube
        elif self.radioButtonQSO.isChecked() == True:
            self.displayOutCube = self.QSOcube
            
        self.radioButtonModeView.setChecked(True)
        self.radioButtonModeZoom.setChecked(False)
        self.radioButtonModeSelect.setChecked(False)
        self.checkBoxModeBoth.setChecked(True)
        self.changedSlider(self.cubeSlider.slider.value())
        self.spaxFigMousePress(1, None, None, self.spaxWidg1.showSpax[0][0]+0.5, self.spaxWidg1.showSpax[0][1]+0.5)
        
    def changeMouseMode(self):
        sender = self.sender()
        if sender == self.radioButtonModeView:
            self.radioButtonModeView.setChecked(True)
            self.radioButtonModeZoom.setChecked(False)
            self.radioButtonModeSelect.setChecked(False)
            
        elif sender == self.radioButtonModeZoom:
            self.radioButtonModeView.setChecked(False)
            self.radioButtonModeZoom.setChecked(True)
            self.radioButtonModeSelect.setChecked(False)
            
        elif sender == self.radioButtonModeSelect:
            self.radioButtonModeView.setChecked(False)
            self.radioButtonModeZoom.setChecked(False)
            self.radioButtonModeSelect.setChecked(True)
         
        if self.radioButtonModeView.isChecked():           
            self.spaxWidg1.pickRectangle.set_visible(True)
            self.spaxWidg1.selectSpaxMask.setVisible(False)
            self.specWidg.selectSpecMask.setVisible(False)
            self.specWidg.viewLine.set_visible(True)
            self.cubeSlider.setEnabled(True)
            self.actionSetQSOcentre.setEnabled(True)
            
        elif self.radioButtonModeZoom.isChecked():           
            self.radioButtonModeView.setChecked(False)
            self.radioButtonModeZoom.setChecked(True)
            self.radioButtonModeSelect.setChecked(False)
            self.spaxWidg1.pickRectangle.set_visible(False)
            self.spaxWidg1.selectSpaxMask.setVisible(False)
            self.specWidg.selectSpecMask.setVisible(False)
            self.specWidg.viewLine.set_visible(False)
            self.cubeSlider.setEnabled(False)
            self.actionSetQSOcentre.setEnabled(False)
            
        elif self.radioButtonModeSelect.isChecked(): 
            self.radioButtonModeView.setChecked(False)
            self.radioButtonModeZoom.setChecked(False)
            self.radioButtonModeSelect.setChecked(True)
            self.spaxWidg1.pickRectangle.set_visible(False)
            self.spaxWidg1.selectSpaxMask.setVisible(True)
            self.specWidg.selectSpecMask.setVisible(True)
            self.specWidg.viewLine.set_visible(False)
            self.cubeSlider.setEnabled(False)
            self.actionSetQSOcentre.setEnabled(False)

    def setQSOcent(self):
        pos = self.spaxWidg1.showSpax
        self.regionsSpaxWidg.setQSOCentManual([pos[0][1]+1, pos[0][0]+1])
        self.modeWidg.hostModel.setCenter([pos[0][1]+1,  pos[0][0]+1])
            
    def toggleSelectMouse(self):
        self.radioButtonModeSelect.setChecked(True)
        self.radioButtonModeView.setChecked(False)
        self.radioButtonModeZoom.setChecked(False)
        self.changeMouseMode()
        
    def toggleViewMouse(self):
        self.radioButtonModeView.setChecked(True)
        self.radioButtonModeZoom.setChecked(False)
        self.radioButtonModeSelect.setChecked(False)
        self.changeMouseMode()
        
    def startMonteCarlo(self):
        dialog = dlgMonteCarlo.dlgMonteCarlo(self, self.MonteSettings)
        dialog.show()
        
    def startSubtractQSO(self):
        try:
            broad1 =  self.regionsSpecWidg.regionBroad1.getMask(self.inputCube.wave)
            cont1 =  self.regionsSpecWidg.regionCont1.getMask(self.inputCube.wave)
            if self.comboBoxRegions.currentIndex()==0:
                broad_region = [broad1, broad1]
                cont_region = [cont1, cont1]
            elif self.comboBoxRegions.currentIndex()==1:
                broad2 =   self.regionsSpecWidg.regionBroad2.getMask(self.inputCube.wave)
                broad_region = [broad1, broad2]
                cont_region = [cont1, cont1]
            elif self.comboBoxRegions.currentIndex()==2:
                cont2 =   self.regionsSpecWidg.regionCont2.getMask(self.inputCube.wave)
                broad_region = [broad1, broad1]
                cont_region = [cont1, cont2]
            elif self.comboBoxRegions.currentIndex()==3:
                broad2 =   self.regionsSpecWidg.regionBroad2.getMask(self.inputCube.wave)
                cont2 =   self.regionsSpecWidg.regionCont2.getMask(self.inputCube.wave)
                broad_region = [broad1, broad2]
                cont_region = [cont1, cont2]
            
            iter = self.modeWidg.boxIterations.value()
            mode = self.modeWidg.comboCorrMode.currentIndex()
            qso_mask = self.regionsSpaxWidg.getQSOMask()
            if mode==0:
                eelr_mask = None
                iter = 1
                factor = None
                hostimage = None
            elif mode==1:
                eelr_mask=self.regionsSpaxWidg.getEELRMask()
                factor = None
                hostimage = None
            elif mode==2:
                eelr_mask=self.regionsSpaxWidg.getEELRMask()
                factor = float(self.lineEditSFBFactor.text())
                hostimage = None
            elif mode==3:
                eelr_mask=self.regionsSpaxWidg.getEELRMask()
                factor = None
                hostmodel = self.modeWidg.hostModel.createHostModel()
                if hostmodel[0]:
                    hostimage = hostmodel[1]
                else:
                    raise EmptyHostImage
            else:
                factor = None
            mode_region = str(self.comboBoxRegionMeasure.currentText())
            
            if self.modeWidg.radioRadius.isChecked():
                radius = float(self.modeWidg.boxRadius.text())
            else:
                radius = None

            if not iter==1:
                progress = QProgressDialog('Perform Subtraction', '', 1, iter, parent=self)
                progress.forceShow()
            else:
                progress=None
            center = self.regionsSpaxWidg.centQSO
            subtracted = self.inputCube.deblendQSOHost(center, qso_mask, broad_region, cont_region , iter, mode_region,
                                                       eelr_mask=eelr_mask,
                                                       interpolate_cont=self.checkBoxInterpCont.isChecked(),
                                                       subtract_region=None, radius=radius,  host_image=hostimage,
                                                       factor=factor, showProgress=progress)
            if self.EELRcube.isEmpty():
                empty = 1
            else:
                empty = 0

            self.QSOcube = subtracted[1]
            self.EELRcube = subtracted[0]
            self.radioButtonHost.setEnabled(True)
            self.radioButtonQSO.setEnabled(True)
            if self.radioButtonHost.isChecked():
                self.displayOutCube = self.EELRcube
            else:
                self.displayOutCube = self.QSOcube
            self.pushButtonSaveResults.setEnabled(True)
            self.actionSave_Results.setEnabled(True)
            slice = self.verticalSliderSlice.value()
            if empty==1:
                self.spaxWidg2.initImage(self.displayOutCube.dataCube[slice-1, :, :], limits=True)
                self.spaxWidg2.initShowSpax(0, 0, True)
                self.specWidg.initSpec2(self.displayOutCube.wave, spec2=self.EELRcube.dataCube[:, 0, 0])
                self.specWidg.setXLim((self.inputCube.wave[0], self.inputCube.wave[-1]))
            else:
                self.spaxWidg2.updateImage(self.displayOutCube.dataCube[slice-1, :, :], True)
                self.specWidg.updateSpec2(self.displayOutCube.wave,  spec2=self.EELRcube.dataCube[:,0, 0])
            self.changeOutCube()
            self.checkBoxModeBoth.setEnabled(True)
        except UnfilledMaskError, error:
            warning = QMessageBox.critical(self,'Run-time Error', error.msg)
            
        except EmptyHostImage, error:
            warning = QMessageBox.critical(self,'Run-time Error', error.msg)
        
    def setColourScheme(self):
        dialog = dlgColorProperties.DlgColorProperties(self.specWidg.colorScheme, self.spaxWidg1.colorScheme,
                                                       self.spaxWidg2.colorScheme, self.regionsSpaxWidg.colorScheme,
                                                       self.regionsSpecWidg.colorScheme, parent=self)
        dialog.show()
        
    def onlineManual(self):
        manualpath = os.path.join(os.path.dirname(__file__), "../../docs/html")
        form = onlineHelp.HelpForm(manualpath+"/index.html", self)
        form.show()
        
    def aboutQt(self):
        QMessageBox.aboutQt(self, 'About Qt')
        
    def about(self):
        QMessageBox.about(self, 'Version', QString('''<b>QDeblend<sup>3D</sup> version:  %s</b><p>
        QDeblend<sup>3D</sup> is a dedicated Graphical User Interface to control and perform the deblending
        of QSO and host galaxy emission for 3D data of integral field spectrographs. <p>
            
        QDeblend<sup>3D</sup> is free software: you can redistribute it and/or modify
        it under the terms of the MIT License.
        <p>
        QDeblend<sup>3D</sup> is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
        <p>
        Copyright (C) 2020 Bernd Husemann'''%(QDeblend.__version__)))
from QDeblend.ui import ui_dlgEditHostModel
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
        self.__hostModels = []
        self.__hostFromId = {}
        self.__empty = True
        self.__center = []
        self.__dim = []
        self.selected = None

    def __len__(self):
        return len(self.__hostModels)

    def __iter__(self):
        for pair in iter(self.__hostModels):
            yield pair

    def clear(self):
        self.__hostModels = []
        self.__hostFromId = {}
        self.__empty = True
        self.selected = None

    def setCenter(self, center):
        self.center = center

    def setDim(self, dim):
        self.dim = dim

    def add(self, hostModel):
        if id(hostModel) in self.__hostFromId:
            return False
        else:
            self.__hostModels.append(hostModel)
            self.__hostFromId[id(hostModel)] = hostModel
            self.__empty = False

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
        hosts = []
        for i in range(len(self.__hostModels)):
            hosts.append(self.__hostModels[i].getModel())
        return hosts

    def copyContainer(self, container):
        self.clear()
        for i in range(len(container)):
            self.add(container.__hostModels[i])

    def setSelected(self, hostModel):
        if hostModel == None:
            self.selected == None
        else:
            self.selected = self.__hostFromId[id(hostModel)]

    def createHostModel(self):
        if len(self.__hostModels) != 0 and self.dim != [] and self.center != []:
            array = numpy.zeros(self.dim, dtype=numpy.float32)
            for i in range(len(self.__hostModels)):
                sersic = host_profiles.Sersic(self.dim, self.center[1] + self.__hostModels[i].x,
                                              self.center[0] + self.__hostModels[i].y, self.__hostModels[i].mag,
                                              self.__hostModels[i].sersic, self.__hostModels[i].re,
                                              self.__hostModels[i].e, self.__hostModels[i].theta / 180.0 * numpy.pi)
                array = array + sersic.array
            return [True, array]
        else:
            return [False, []]

    def updateSelected(self, hostModel):
        for i in range(len(self.__hostModels)):
            if self.__hostModels[i] == self.selected:
                self.__hostModels[i] = hostModel
                del self.__hostFromId[id(self.selected)]
                self.__hostFromId[id(hostModel)] = hostModel
                self.selected = hostModel
                break

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
        hostModel = hostModel(self.dMag.value(), self.dDeltax.value(), self.dDeltay.value(), self.dEffRadius.value(),
                              self.dSersic.value(), self.dElip.value(), self.dPA.value())
        if self.mode=='add':
            self.hostContainer.add(hostModel)
        if self.mode=='change':
            self.hostContainer.updateSelected(hostModel)
        self.parent.updateTable()
        self.parent.updateImag()
        self.accept()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlgEditHostModel.ui'
#
# Created: Sun Feb  6 13:10:44 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgEditHostModel(object):
    def setupUi(self, dlgEditHostModel):
        dlgEditHostModel.setObjectName("dlgEditHostModel")
        dlgEditHostModel.setWindowModality(QtCore.Qt.WindowModal)
        dlgEditHostModel.resize(247, 287)
        dlgEditHostModel.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(dlgEditHostModel)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(dlgEditHostModel)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.dMag = QtGui.QDoubleSpinBox(dlgEditHostModel)
        self.dMag.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.dMag.setMinimum(-100.0)
        self.dMag.setMaximum(100.99)
        self.dMag.setSingleStep(0.1)
        self.dMag.setProperty("value", 0.0)
        self.dMag.setObjectName("dMag")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.dMag)
        self.label_2 = QtGui.QLabel(dlgEditHostModel)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.dDeltax = QtGui.QDoubleSpinBox(dlgEditHostModel)
        self.dDeltax.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.dDeltax.setMinimum(-100.0)
        self.dDeltax.setMaximum(100.99)
        self.dDeltax.setSingleStep(0.1)
        self.dDeltax.setProperty("value", 0.0)
        self.dDeltax.setObjectName("dDeltax")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.dDeltax)
        self.label_3 = QtGui.QLabel(dlgEditHostModel)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.dDeltay = QtGui.QDoubleSpinBox(dlgEditHostModel)
        self.dDeltay.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.dDeltay.setMinimum(-100.0)
        self.dDeltay.setMaximum(100.99)
        self.dDeltay.setSingleStep(0.1)
        self.dDeltay.setProperty("value", 0.0)
        self.dDeltay.setObjectName("dDeltay")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dDeltay)
        self.label_4 = QtGui.QLabel(dlgEditHostModel)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.dEffRadius = QtGui.QDoubleSpinBox(dlgEditHostModel)
        self.dEffRadius.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.dEffRadius.setMinimum(-1.0)
        self.dEffRadius.setMaximum(100.99)
        self.dEffRadius.setSingleStep(0.1)
        self.dEffRadius.setProperty("value", 3.0)
        self.dEffRadius.setObjectName("dEffRadius")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.dEffRadius)
        self.label_5 = QtGui.QLabel(dlgEditHostModel)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.dSersic = QtGui.QDoubleSpinBox(dlgEditHostModel)
        self.dSersic.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.dSersic.setMinimum(0.0)
        self.dSersic.setMaximum(10.0)
        self.dSersic.setSingleStep(0.1)
        self.dSersic.setProperty("value", 1.0)
        self.dSersic.setObjectName("dSersic")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.dSersic)
        self.label_6 = QtGui.QLabel(dlgEditHostModel)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.dElip = QtGui.QDoubleSpinBox(dlgEditHostModel)
        self.dElip.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.dElip.setMinimum(0.0)
        self.dElip.setMaximum(0.9)
        self.dElip.setSingleStep(0.01)
        self.dElip.setProperty("value", 0.0)
        self.dElip.setObjectName("dElip")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.dElip)
        self.label_7 = QtGui.QLabel(dlgEditHostModel)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.dPA = QtGui.QDoubleSpinBox(dlgEditHostModel)
        self.dPA.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.dPA.setMinimum(-90.0)
        self.dPA.setMaximum(90.0)
        self.dPA.setSingleStep(0.1)
        self.dPA.setProperty("value", 0.0)
        self.dPA.setObjectName("dPA")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.dPA)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(dlgEditHostModel)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(dlgEditHostModel)
        QtCore.QMetaObject.connectSlotsByName(dlgEditHostModel)

    def retranslateUi(self, dlgEditHostModel):
        dlgEditHostModel.setWindowTitle(QtGui.QApplication.translate("dlgEditHostModel", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgEditHostModel", "Magnitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgEditHostModel", "Delta x:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("dlgEditHostModel", "Delta y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dlgEditHostModel", "Eff. Radius", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("dlgEditHostModel", "Sersic Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("dlgEditHostModel", "Ellipiticity:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("dlgEditHostModel", "PA:", None, QtGui.QApplication.UnicodeUTF8))

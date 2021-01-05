# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlgSaveCubes.ui'
#
# Created: Sun Feb  6 13:29:44 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgSaveCubes(object):
    def setupUi(self, dlgSaveCubes):
        dlgSaveCubes.setObjectName("dlgSaveCubes")
        dlgSaveCubes.resize(532, 210)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgSaveCubes.sizePolicy().hasHeightForWidth())
        dlgSaveCubes.setSizePolicy(sizePolicy)
        dlgSaveCubes.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(dlgSaveCubes)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(dlgSaveCubes)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineDir = QtGui.QLineEdit(dlgSaveCubes)
        self.lineDir.setEnabled(False)
        self.lineDir.setDragEnabled(False)
        self.lineDir.setReadOnly(True)
        self.lineDir.setObjectName("lineDir")
        self.horizontalLayout_2.addWidget(self.lineDir)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtGui.QSpacerItem(358, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.bDirSelect = QtGui.QPushButton(dlgSaveCubes)
        self.bDirSelect.setObjectName("bDirSelect")
        self.horizontalLayout_4.addWidget(self.bDirSelect)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtGui.QLabel(dlgSaveCubes)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.linePrefix = QtGui.QLineEdit(dlgSaveCubes)
        self.linePrefix.setObjectName("linePrefix")
        self.horizontalLayout.addWidget(self.linePrefix)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(dlgSaveCubes)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.groupBox = QtGui.QGroupBox(dlgSaveCubes)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.dStart = QtGui.QDoubleSpinBox(self.groupBox)
        self.dStart.setMaximum(99998.0)
        self.dStart.setSingleStep(0.1)
        self.dStart.setObjectName("dStart")
        self.gridLayout.addWidget(self.dStart, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.dEnd = QtGui.QDoubleSpinBox(self.groupBox)
        self.dEnd.setMaximum(100000.0)
        self.dEnd.setSingleStep(0.1)
        self.dEnd.setObjectName("dEnd")
        self.gridLayout.addWidget(self.dEnd, 1, 1, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_5.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.retranslateUi(dlgSaveCubes)
        QtCore.QMetaObject.connectSlotsByName(dlgSaveCubes)

    def retranslateUi(self, dlgSaveCubes):
        dlgSaveCubes.setWindowTitle(QtGui.QApplication.translate("dlgSaveCubes", "Save Output Cubes", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgSaveCubes", "Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.bDirSelect.setText(QtGui.QApplication.translate("dlgSaveCubes", "Choose Dir...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgSaveCubes", "Prefix Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("dlgSaveCubes", "Select Wavelength (Optional)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("dlgSaveCubes", "Start wavelength:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dlgSaveCubes", "End wavelength:", None, QtGui.QApplication.UnicodeUTF8))


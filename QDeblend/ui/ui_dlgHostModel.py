# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlgHostModel.ui'
#
# Created: Sun Feb  6 13:23:54 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dlgHostModel(object):
    def setupUi(self, dlgHostModel):
        dlgHostModel.setObjectName("dlgHostModel")
        dlgHostModel.setWindowModality(QtCore.Qt.ApplicationModal)
        dlgHostModel.resize(882, 305)
        dlgHostModel.setModal(True)
        self.horizontalLayout_5 = QtGui.QHBoxLayout(dlgHostModel)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableHost = QtGui.QTableWidget(dlgHostModel)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableHost.sizePolicy().hasHeightForWidth())
        self.tableHost.setSizePolicy(sizePolicy)
        self.tableHost.setFrameShadow(QtGui.QFrame.Plain)
        self.tableHost.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableHost.setAlternatingRowColors(True)
        self.tableHost.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableHost.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableHost.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableHost.setGridStyle(QtCore.Qt.NoPen)
        self.tableHost.setObjectName("tableHost")
        self.tableHost.setColumnCount(7)
        self.tableHost.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableHost.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableHost.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableHost.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableHost.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableHost.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableHost.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableHost.setHorizontalHeaderItem(6, item)
        self.verticalLayout.addWidget(self.tableHost)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bAddModel = QtGui.QPushButton(dlgHostModel)
        self.bAddModel.setObjectName("bAddModel")
        self.horizontalLayout.addWidget(self.bAddModel)
        self.bChangeModel = QtGui.QPushButton(dlgHostModel)
        self.bChangeModel.setObjectName("bChangeModel")
        self.horizontalLayout.addWidget(self.bChangeModel)
        self.bDeleteModel = QtGui.QPushButton(dlgHostModel)
        self.bDeleteModel.setObjectName("bDeleteModel")
        self.horizontalLayout.addWidget(self.bDeleteModel)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtGui.QSpacerItem(318, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.buttonBox = QtGui.QDialogButtonBox(dlgHostModel)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        spacerItem4 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.frame = QtGui.QFrame(dlgHostModel)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dispHostModel = MatplotlibImgWidget(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dispHostModel.sizePolicy().hasHeightForWidth())
        self.dispHostModel.setSizePolicy(sizePolicy)
        self.dispHostModel.setMinimumSize(QtCore.QSize(270, 270))
        self.dispHostModel.setObjectName("dispHostModel")
        self.horizontalLayout_2.addWidget(self.dispHostModel)
        self.horizontalLayout_4.addWidget(self.frame)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)

        self.retranslateUi(dlgHostModel)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dlgHostModel.accept)
        QtCore.QMetaObject.connectSlotsByName(dlgHostModel)

    def retranslateUi(self, dlgHostModel):
        dlgHostModel.setWindowTitle(QtGui.QApplication.translate("dlgHostModel", "Edit Continuum Host Model", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHost.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("dlgHostModel", "mag", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHost.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("dlgHostModel", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHost.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("dlgHostModel", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHost.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("dlgHostModel", "Eff. Radius", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHost.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("dlgHostModel", "Seric index", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHost.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("dlgHostModel", "Ellipticity", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHost.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("dlgHostModel", "PA", None, QtGui.QApplication.UnicodeUTF8))
        self.bAddModel.setText(QtGui.QApplication.translate("dlgHostModel", "&Add Model", None, QtGui.QApplication.UnicodeUTF8))
        self.bChangeModel.setText(QtGui.QApplication.translate("dlgHostModel", "&Change Model", None, QtGui.QApplication.UnicodeUTF8))
        self.bDeleteModel.setText(QtGui.QApplication.translate("dlgHostModel", "&Delete Model", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibimgwidget import MatplotlibImgWidget

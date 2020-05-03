# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recaptcha.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_recaptcha_ui(object):
    def setupUi(self, recaptcha_ui):
        recaptcha_ui.setObjectName("recaptcha_ui")
        recaptcha_ui.resize(400, 700)
        recaptcha_ui.setMinimumSize(QtCore.QSize(400, 700))
        recaptcha_ui.setMaximumSize(QtCore.QSize(400, 700))
        self.verticalLayout = QtWidgets.QVBoxLayout(recaptcha_ui)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tab_widget = QtWidgets.QTabWidget(recaptcha_ui)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabBarAutoHide(False)
        self.tab_widget.setObjectName("tab_widget")
        self.verticalLayout.addWidget(self.tab_widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.combo_box_gmail = QtWidgets.QComboBox(recaptcha_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_box_gmail.sizePolicy().hasHeightForWidth())
        self.combo_box_gmail.setSizePolicy(sizePolicy)
        self.combo_box_gmail.setMinimumSize(QtCore.QSize(0, 0))
        self.combo_box_gmail.setObjectName("combo_box_gmail")
        self.horizontalLayout.addWidget(self.combo_box_gmail)
        self.push_button_gmail = QtWidgets.QPushButton(recaptcha_ui)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.push_button_gmail.setFont(font)
        self.push_button_gmail.setText("")
        self.push_button_gmail.setObjectName("push_button_gmail")
        self.horizontalLayout.addWidget(self.push_button_gmail)
        self.push_button_add = QtWidgets.QPushButton(recaptcha_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_add.sizePolicy().hasHeightForWidth())
        self.push_button_add.setSizePolicy(sizePolicy)
        self.push_button_add.setMinimumSize(QtCore.QSize(0, 0))
        self.push_button_add.setText("")
        self.push_button_add.setObjectName("push_button_add")
        self.horizontalLayout.addWidget(self.push_button_add)
        self.push_button_delete = QtWidgets.QPushButton(recaptcha_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_delete.sizePolicy().hasHeightForWidth())
        self.push_button_delete.setSizePolicy(sizePolicy)
        self.push_button_delete.setMinimumSize(QtCore.QSize(0, 0))
        self.push_button_delete.setText("")
        self.push_button_delete.setObjectName("push_button_delete")
        self.horizontalLayout.addWidget(self.push_button_delete)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(recaptcha_ui)
        self.tab_widget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(recaptcha_ui)

    def retranslateUi(self, recaptcha_ui):
        _translate = QtCore.QCoreApplication.translate
        recaptcha_ui.setWindowTitle(_translate("recaptcha_ui", "Captcha Queue"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    recaptcha_ui = QtWidgets.QWidget()
    ui = Ui_recaptcha_ui()
    ui.setupUi(recaptcha_ui)
    recaptcha_ui.show()
    sys.exit(app.exec_())

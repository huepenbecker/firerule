import sys

# our classes
from RuleCollection import RuleCollection
from SingleRule import SingleRule
from Building import Building, strToBaustoffCategory, strToSicherheitsCategory
import Database
from imp import reload
# gui
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from MainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):

    # like so?
    def __init__(self):
        super(MainWindow, self).__init__()

        self.coll = RuleCollection()
        self.coll.addRule(Database.LoeWa())
        self.coll.addRule(Database.ZuGa())
        self.coll.addRule(Database.ZweiGe())
        self.coll.addRule(Database.UnterGe())
        self.coll.addRule(Database.RettWeg())
        self.coll.addRule(Database.CheckBrandabschnittsflaeche())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self-setup:
        self.ui.pushStart.clicked.connect(self.check)

        self.ui.squareSpinBox.valueChanged.connect(self.setSquareMeters)
        self.ui.topSpinBox.valueChanged.connect(self.setTopFloors)
        self.ui.subSpinBox.valueChanged.connect(self.setSubFloors)
        self.ui.heightSpinBox.valueChanged.connect(self.setHeight)
        self.ui.sicherheitsCombo.currentIndexChanged.connect(self.updateSicherheits)
        self.ui.baustoffCombo.currentIndexChanged.connect(self.updateBaustoff)
        self.ui.pushNeu.clicked.connect(self.reloadDatabase)
        self.ui.pushBeenden.clicked.connect(QtWidgets.QApplication.quit)

        self.haus = Building(
                squaremeters = self.ui.squareSpinBox.value(),
                height = self.ui.heightSpinBox.value(),
                subfloors = self.ui.subSpinBox.value(),
                topfloors = self.ui.topSpinBox.value(),
                sicherheits = strToSicherheitsCategory(self.ui.sicherheitsCombo.currentText()),
                baustoff = strToBaustoffCategory(self.ui.baustoffCombo.currentText())
                )

        print('running...')
        self.show()

    def check(self):
        self.coll.checkRuleResultForBuilding(self.haus)
    def reloadDatabase(self):

        reload( Database )

        print('Database reloaded...')

    @QtCore.pyqtSlot()
    def updateSicherheits(self):
        self.haus.setSicherheitsFromString(self.ui.sicherheitsCombo.currentText())
    @QtCore.pyqtSlot()
    def updateBaustoff(self):
        self.haus.setBaustoffFromString(self.ui.baustoffCombo.currentText())
    @QtCore.pyqtSlot(float)
    def setHeight(self, height):
        self.haus.height = height
    @QtCore.pyqtSlot(int)
    def setSubFloors(self, subfloors):
        self.haus.subfloors = subfloors
    @QtCore.pyqtSlot(int)
    def setTopFloors(self, topfloors):
        self.haus.topfloors = topfloors
    @QtCore.pyqtSlot(float)
    def setSquareMeters(self, squaremeters):
        self.haus.squaremeters = squaremeters

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

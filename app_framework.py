from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal


import numpy as np
import pyjapc
import ParameterSetting as pc
import ObservableClass as ob
import GetOptimalMultiValueThreadClass as gOVThread
from sceleton import Ui_MainWindow


class MyApp(QMainWindow, Ui_MainWindow):

    japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=False)
    japc.setSelector("LEI.USER.EARLY")
    japc.rbacLogin()
    averageNrValue = 5.
    parameterClass = pc.ParameterClass(japc)
    algorithmSelection = 'Powell'

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        Ui_MainWindow.__init__(self)

        self.imageLabel.setPixmap(QPixmap("Powell.png"))
        self.imageLabel.setScaledContents(True)

        self.runOptimizationButton.clicked.connect(self.runOptimization)
        self.runOptimizationButton.setEnabled(False)

        self.buttonRestoreOldValues.clicked.connect(
                self.buttonRestoreOldValuesPressed)

        self.spinBoxXTolValue.valueChanged.connect(
                self.spinBoxXTolValueChanged)
        self.spinBoxFTolValue.valueChanged.connect(
                self.spinBoxFTolValueChanged)
        self.spinBoxAverageNr.valueChanged.connect(
                self.spinBoxAverageNrChanged)

        self.japc.subscribeParam("ER.BCTDC/Acquisition#intensities",
                                 self.onValueRecieved)

        self.ob = ob.ObservableClass(self.japc, self.averageNrValue)


#        self.visualizeData()
        self.xTol = 0.02
        self.fTol = 0.05
        self.x0 = []

        self.spinBoxXTolValue.setValue(self.xTol)
        self.spinBoxFTolValue.setValue(self.fTol)
        self.spinBoxAverageNr.setValue(self.averageNrValue)
        self.buttonGroup.buttonClicked.connect(self.buttonGroupSelected)
        self.algorithmSelection = self.buttonGroup.checkedButton().text()

        self.listSelector = ListSelector()

        for itemName in self.listSelector.getItems():
            item = QListWidgetItem(itemName)
            if item.text() in self.listSelector.markedItems:
                item.setBackground(QColor(255, 0, 0))
            else:
                item.setBackground(QColor(0, 255, 0))
            self.listWidget.addItem(item)
        self.listWidget.sortItems()   
        self.listWidget.itemSelectionChanged.connect(self.itemsChanged)

    def itemsChanged(self):  # s is a str

        currentSelection = [item.text() for item in
                            self.listWidget.selectedItems()]
        self.listSelector.setSelection(currentSelection)

        if len(self.listSelector.selectionList) > 0:
            self.runOptimizationButton.setEnabled(True)
        else:
            self.runOptimizationButton.setEnabled(False)

    def buttonGroupSelected(self, id):
        self.algorithmSelection = id.text()


    def buttonRestoreOldValuesPressed(self):
        self.setValues(self.x0)

    def spinBoxXTolValueChanged(self):
        self.xTol = self.spinBoxXTolValue.value()

    def spinBoxFTolValueChanged(self):
        self.fTol = self.spinBoxFTolValue.value()

    def spinBoxAverageNrChanged(self):
        self.averageNrValue = self.spinBoxAverageNr.value()
        self.ob.dataLength = self.averageNrValue

    def onValueRecieved(self, parameterName, newValue):
        self.ob.setValue(np.abs(newValue[395]) * (-1.))  # /normVal
#        print('subscibtionRuns')

    def runOptimization(self):
        if self.runOptimizationButton.text() == "Start":

            self.parameterClass.resetParameters()

            self.parameterClass.addParameters(
                    self.listSelector.getSelectedItemsDict())

            self.x0 = self.parameterClass.getStartVector()

            self.getOptimalValueThread = gOVThread.getOptimalMultiValueThread(
                    self.parameterClass, self.ob, self.algorithmSelection,
                    self.xTol, self.fTol)

            self.getOptimalValueThread.signals.setSubscribtion.connect(
                    self.setSubscribtion)
            self.getOptimalValueThread.signals.setValues.connect(
                    self.setValues)
            self.getOptimalValueThread.signals.drawNow.\
                connect(self.visualizeData)
            self.getOptimalValueThread.signals.jobFinished.connect(self.done)
            self.getOptimalValueThread.start()
            self.runOptimizationButton.setText('Cancel')

        elif self.getOptimalValueThread.isRunning():

            self.getOptimalValueThread.cancelFlag = True
            self.getOptimalValueThread.wait()
            self.getOptimalValueThread.quit()
            self.getOptimalValueThread.wait()

            self.runOptimizationButton.setText('Start')

    def setValues(self, x):
        print(x)
        self.parameterClass.setNewValues(x)

    def done(self):
        print("DONE")
        self.runOptimizationButton.setText('Start')
        QMessageBox.information(self, 'Scan succsessful', "Final values at: " +
                                str(self.parameterClass.getValues()) +
                                "\nInitial values: " +
                                str(self.x0),
                                QMessageBox.Close)

    def setSubscribtion(self, suscribtionBool):
        if suscribtionBool:
            self.japc.startSubscriptions()
        else:
            self.japc.stopSubscriptions()

    def visualizeData(self):
#        print("Main draw.......................................")
#        print(self.getOptimalValueThread.injIntensityEvolution)
        plotFrame = self.getOptimalValueThread.parameterEvolution.iloc[:, 1:].T
        self.plotWidget.canvas.axs[1].clear()
        self.plotWidget.canvas.axs[0].clear()
        if plotFrame.shape[0] > 1:
            plotFrame.iloc[:, :-1].plot(ax=self.plotWidget.canvas.axs[0])
            plotFrame.iloc[:, -1].plot(ax=self.plotWidget.canvas.axs[1])
#        print("Main draw.........................")
#        print(plotFrame)

        self.plotWidget.canvas.axs[0].set_title('Parameter evolution')
        self.plotWidget.canvas.axs[1].set_title('Intensity')
        self.plotWidget.canvas.axs[0].set_xlabel('Nr of changes')
        self.plotWidget.canvas.axs[1].set_xlabel('Nr of changes')
        self.plotWidget.canvas.axs[0].set_ylabel('parameters (a.u.)')
        self.plotWidget.canvas.axs[1].set_ylabel('intensity (10e10 c.)')

        self.plotWidget.canvas.fig.tight_layout()
        self.plotWidget.canvas.draw()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.setSubscribtion(False)
            event.accept()
        else:
            event.ignore()


class ListSelector():

    parameterList = {"EI.BVN10/K":
                     {"name": "rmi://virtual_sps/logical.EI.BVN10/K",
                      "type": "scalar"},
                     "EI.BVN20/K":
                         {"name": "rmi://virtual_sps/logical.EI.BVN20/K",
                          "type": "scalar"},
                     "EI.BHN10/K":
                         {"name": "rmi://virtual_sps/logical.EI.BHN10/K",
                          "type": "scalar"},
                     "ETL.BHN20-INJ/K":
                         {"name": "rmi://virtual_sps/logical.ETL.BHN20-INJ/K",
                          "type": "scalar"},
                         "ITH.DHZ10/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DHZ10/K",
                              "type": "scalar"},
                         "ITH.DHZ11/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DHZ11/K",
                              "type": "scalar"},
                         "ITH.DHZ21/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DHZ21/K",
                              "type": "scalar"},
                         "ITE.BHN10/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN10/K",
                              "type": "scalar"},
                         "ITE.BHN20/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN20/K",
                              "type": "scalar"},
                         "ITE.BHN30/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN30/K",
                              "type": "scalar"},
                         "ITE.BHN40-IN-LEI/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN40-IN-LEI/K",
                              "type": "scalar"},
                         "ETL.DHN10-INJ/K":
                             {"name": "rmi://virtual_sps/logical.ETL.DHN10-INJ/K",
                              "type": "scalar"},
                         "ITH.DVT10/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DVT10/K",
                              "type": "scalar"},
                         "ITH.DVT11/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DVT11/K",
                              "type": "scalar"},
                         "ITH.DVT21/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DVT21/K",
                              "type": "scalar"},
                         "ETL.BVN10-INJ/K":
                             {"name": "rmi://virtual_sps/logical.ETL.BVN10-INJ/K",
                              "type": "scalar"},
                         "ETL.BVN20-INJ/K":
                         {"name": "rmi://virtual_sps/logical.ETL.BVN20-INJ/K",
                          "type": "scalar"},
                         "ETL.GSBHN10/KICK":
                             {"name": "rmi://virtual_leir/ETL.GSBHN10/KICK",
                              "type": "function", "time": [110, 660]},
                          "LEIRBEAM/injectionBump_CTRS10_H_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_H_1mm",
                              "type": "function", "time": [200, 750]},
                          "LEIRBEAM/injectionBump_CTRS10_H_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_H_1mrad",
                              "type": "function", "time": [200, 750]},
                          "LEIRBEAM/injectionBump_CTRS10_V_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_H_1mrad",
                              "type": "function", "time": [200, 650]},
                           "LEIRBEAM/injectionBump_CTRS10_V_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_V_1mrad",
                              "type": "function", "time": [200, 650]}
                             }
    markedItems = {"EI.BVN10/K", "EI.BVN20/K", "EI.BHN10/K"}

    def getItems(self):
        return self.parameterList.keys()

    def getSelectedItemsNames(self):
        return [self.parameterList[key] for key in self.selectionList]

    def getSelectedItemsDict(self):
        return {key: self.parameterList[key] for key in self.selectionList}

    def __init__(self):
        self.selectionList = []

    def setSelection(self, selectedItems):
        self.selectionList = selectedItems

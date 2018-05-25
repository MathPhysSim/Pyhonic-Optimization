from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal


import numpy as np
import pyjapc
import ParameterClass as pc
import ObservableClass as ob
import GetOptimalMultiValueThreadClass as gOVThread
from sceleton import Ui_MainWindow


class MyApp(QMainWindow, Ui_MainWindow):

    japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=False)
    japc.setSelector("LEI.USER.EARLY")

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
        self.x0 = self.parameterClass.getValues()

        self.spinBoxXTolValue.setValue(self.xTol)
        self.spinBoxFTolValue.setValue(self.fTol)
        self.spinBoxAverageNr.setValue(self.averageNrValue)
        self.buttonGroup.buttonClicked.connect(self.buttonGroupSelected)
        self.algorithmSelection = self.buttonGroup.checkedButton().text()
        print(self.algorithmSelection)
        
    def buttonGroupSelected(self, id):
        self.algorithmSelection = id.text()
        print(self.algorithmSelection)
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
        print("Helloxxx")
        if self.runOptimizationButton.text() == "Start":
            self.getOptimalValueThread = gOVThread.getOptimalMultiValueThread(
                    self.parameterClass, self.ob, self.algorithmSelection,
                    self.xTol, self.fTol)
            self.getOptimalValueThread.signals.setSubscribtion.connect(
                    self.setSubscribtion)
            self.getOptimalValueThread.signals.setValues.connect(self.setValues)
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
        self.parameterClass.setValues(x)
        print(x)

    def done(self):
        self.runOptimizationButton.setText('Start')
        QMessageBox.information(self, 'Scan succsessful', "Final values at: " 
                             + str(self.parameterClass.getValues()) +
                             "\nInitial values: " +
                                  str(self.x0),
                                     QMessageBox.Close)

    def setSubscribtion(self, suscribtionBool):
        if suscribtionBool:
            self.japc.startSubscriptions()
        else:
            self.japc.stopSubscriptions()

    def visualizeData(self):
        print(self.getOptimalValueThread.parameterEvolution.iloc[:,1:])
        print(self.getOptimalValueThread.injIntensityEvolution)
        self.plotWidget.canvas.axs[1].clear()
        self.plotWidget.canvas.axs[0].clear()
        self.plotWidget.canvas.axs[0].set_title('Parameter evolution')
        self.plotWidget.canvas.axs[1].set_title('Intensity')
        self.plotWidget.canvas.axs[0].set_xlabel('Nr of changes')
        self.plotWidget.canvas.axs[1].set_xlabel('Nr of changes')
        self.plotWidget.canvas.axs[0].set_ylabel('parameters (a.u.)')
        self.plotWidget.canvas.axs[1].set_ylabel('intensity (10e10 c.)')
        self.getOptimalValueThread.parameterEvolution.iloc[:,1:].T.plot(
                ax=self.plotWidget.canvas.axs[0])
        self.plotWidget.canvas.axs[1].plot(self.getOptimalValueThread.
                                                     injIntensityEvolution)
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

import datetime
import numpy as np
import pyjapc
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import GetOptimalMultiValueThreadClass as gOVThread
import ListSelectorClass as lsclass
import ObservableClass as ob
import ParameterSetting as pc
import zen
from sceleton import Ui_MainWindow


class MyApp(QMainWindow, Ui_MainWindow):

    japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=True)
    
    # japc.rbacLogin()
    averageNrValue = 1.
    parameterClass = pc.ParameterClass(japc)
    algorithmSelection = 'Powell'
    observableMethodSelection = 'Maximum'

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        Ui_MainWindow.__init__(self)

        self.imageLabel.setPixmap(QPixmap("Powell.png"))
        self.imageLabel.setScaledContents(True)

        self.listSelector = lsclass.ListSelector()

        self.runOptimizationButton.clicked.connect(self.runOptimization)
        self.runOptimizationButton.setEnabled(False)

        self.buttonRestoreOldValues.clicked.connect(
                self.buttonRestoreOldValuesPressed)
        self.buttonSetMaximum.clicked.connect(
                self.buttonSetMaximumPressed)

        self.spinBoxXTolValue.valueChanged.connect(
                self.spinBoxXTolValueChanged)
        self.spinBoxFTolValue.valueChanged.connect(
                self.spinBoxFTolValueChanged)
        self.spinBoxAverageNr.valueChanged.connect(
                self.spinBoxAverageNrChanged)
        self.doubleSpinBoxStartTime.valueChanged.connect(
                self.doubleSpinBoxStartTimeChanged)
        self.doubleSpinBoxEndTime.valueChanged.connect(
                self.doubleSpinBoxEndTimeChanged)
        self.doubleSpinBoxStartDirection.valueChanged.connect(
                self.doubleSpinBoxStartDirectionChanged)
        self.doubleSpinBoxIntervalBounds.valueChanged.connect(
            self.doubleSpinBoxIntervalBoundsChanged)
        self.doubleSpinBoxObservableStartTime.valueChanged.connect(
                self.doubleSpinBoxObservableStartTimeChanged)
        self.doubleSpinBoxObservableEndTime.valueChanged.connect(
                self.doubleSpinBoxObservableEndTimeChanged)
        self.doubleSpinBoxMinimalAcceptedChange.valueChanged.connect(
            self.doubleSpinBoxMinimalAcceptedChangeChanged)
        self.japc.setSelector("LEI.USER.MDEARLY")
        self.cycle = self.japc.getSelector()
        # TODO: For the intesity change back
        self.japc.subscribeParam("ER.BCTDC/Acquisition",
                                 self.onValueRecieved)

        # self.japc.subscribeParam("LEI.BQS.L/Acquisition",
        #                          self.onValueRecieved)
        self.observable = ob.ObservableClass(self.japc, self.averageNrValue)


#        self.visualizeData()
        self.xTol = 0.000001
        self.fTol = 0.000001
        self.min_accepted_change = []
        self.x0 = []
        self.max_value = []
        self.interval_bound = 0.0
        self.selectedElement = []
        self.observableTime = np.array([0, 0])

        self.spinBoxXTolValue.setValue(self.xTol)
        self.spinBoxFTolValue.setValue(self.fTol)
        self.spinBoxAverageNr.setValue(self.averageNrValue)
        self.doubleSpinBoxIntervalBounds.setValue(self.interval_bound)
        
        self.buttonGroup.buttonClicked.connect(self.buttonGroupSelected)
        self.algorithmSelection = self.buttonGroup.checkedButton().text()

        self.buttonGroupObservable.\
        buttonClicked.connect(self.buttonGroupObservableSelected)
        self.observableMethodSelection = self.buttonGroupObservable.\
        checkedButton().text()
        


        for itemName in self.listSelector.getItems():
            item = QListWidgetItem(itemName)
            if item.text() in self.listSelector.markedItems:
                item.setBackground(QColor(255, 0, 0))
            else:
                item.setBackground(QColor(0, 255, 0))
            self.listWidget.addItem(item)

        self.listWidget.sortItems()   
        self.listWidget.itemSelectionChanged.connect(self.itemsChanged)
        self.listWidget.itemClicked.connect(self.itemSelected)

        for itemName in ["LEI.USER.EARLY", "LEI.USER.NOMINAL",
                         "LEI.USER.MDOPTIC", "LEI.USER.AMDRF",
                         "LEI.USER.MDEARLY", "LEI.USER.AMDOPTIC",
                         "LEI.USER.MDNOM", "LEI.USER.AMDNOM",
                          "LEI.USER.ANOMINAL","LEI.USER.MDRF",
                          "LEI.USER.FL_NO_MD"]:
            item = QListWidgetItem(itemName)
            self.listWidgetCycle.addItem(item)
        self.listWidgetCycle.itemClicked.connect(self.itemsClickedCycle)
        
        self.plot_init()

    def itemsClickedCycle(self, id):
        
        self.japc.setSelector(id.text())
        self.japc.clearSubscriptions()
        # TODO: For the intesity change back
        self.japc.subscribeParam("ER.BCTDC/Acquisition",
                                 self.onValueRecieved)
        # self.japc.subscribeParam("LEI.BQS.L/Acquisition",
        #                          self.onValueRecieved)
        print("Set to:", self.japc.getSelector())
        self.cycle = self.japc.getSelector()
    def itemsChanged(self):  # s is a str

        currentSelection = [item.text() for item in
                            self.listWidget.selectedItems()]
        self.listSelector.setSelection(currentSelection)

        if len(self.listSelector.selectionList) > 0:
            self.runOptimizationButton.setEnabled(True)
        else:
            self.runOptimizationButton.setEnabled(False)

    def itemSelected(self, id):
        self.selectedElement = id.text()
        selectedEntry = self.listSelector.parameterList[self.selectedElement]
        self.doubleSpinBoxStartDirection.setValue(
                    float(selectedEntry['startDirection']))
        self.doubleSpinBoxMinimalAcceptedChange.setValue(
                    float(selectedEntry["minimalAcceptedChange"]))

        if (selectedEntry['type'] == 'functionSquare')|(self.selectedElement=="ETL.GSBHN10/KICK")|(selectedEntry['type'] == 'functionList'):
            self.doubleSpinBoxStartTime.setEnabled(True)
            self.doubleSpinBoxEndTime.setEnabled(True)

            self.doubleSpinBoxStartTime.setValue(
                    float(selectedEntry['time'][0]))
            self.doubleSpinBoxEndTime.setValue(
                    float(selectedEntry['time'][1]))

        else:
            self.doubleSpinBoxStartTime.setEnabled(False)
            self.doubleSpinBoxEndTime.setEnabled(False)
        self.doubleSpinBoxIntervalBounds.setValue(float(selectedEntry["bounds"][1]))
            
  

    def doubleSpinBoxStartTimeChanged(self):
        selectedEntry = self.listSelector.parameterList[self.selectedElement]
#        print(selectedEntry['time'][1])
        self.listSelector.setItemTime(self.selectedElement,
                                      [self.doubleSpinBoxStartTime.value(),
                                       selectedEntry['time'][1]])
#        self.doubleSpinBoxEndTime.setMinimum(
#                self.doubleSpinBoxStartTime.value()+25.)

    def doubleSpinBoxEndTimeChanged(self):
        selectedEntry = self.listSelector.parameterList[self.selectedElement]
#        print(selectedEntry['time'][1])
        self.listSelector.setItemTime(self.selectedElement,
                                      [selectedEntry['time'][0],
                                       self.doubleSpinBoxEndTime.value()])

    def doubleSpinBoxStartDirectionChanged(self):
        self.listSelector.setItemStartDirection(self.selectedElement,
                                       self.doubleSpinBoxStartDirection.value())
        # if (self.selectedElement['minimalAcceptedChange'] == [0, 0]):
        #     self.listSelector.setItemMinimalAcceptedChange(self.selectedElement,
        #                                                    self.doubleSpinBoxStartDirection.value()/25)

    def doubleSpinBoxMinimalAcceptedChangeChanged(self):
        self.listSelector.setItemMinimalAcceptedChange(self.selectedElement,
                                       self.doubleSpinBoxMinimalAcceptedChange.value())

    def doubleSpinBoxObservableStartTimeChanged(self):
        self.observable.time_interval[0] = self.doubleSpinBoxObservableStartTime.value()
        self.doubleSpinBoxObservableEndTime.\
        setMinimum(self.observable.time_interval[0] + 1)

    def doubleSpinBoxObservableEndTimeChanged(self):
        self.observable.time_interval[1] = self.doubleSpinBoxObservableEndTime.value()

    def doubleSpinBoxIntervalBoundsChanged(self):
        # self.interval_bound = self.doubleSpinBoxIntervalBounds.value()
        # print(self.listSelector)
        self.listSelector.setBoundaries(self.selectedElement, self.doubleSpinBoxIntervalBounds.value())


    def buttonGroupSelected(self, id):
        self.algorithmSelection = id.text()

    def buttonGroupObservableSelected(self, id):
        self.observableMethodSelection = id.text()
        if (self.observableMethodSelection == 'Area') |\
           (self.observableMethodSelection == 'Transmission'):
            self.doubleSpinBoxObservableEndTime.\
                 setMinimum(self.observable.time_interval[0] + 1)
            self.doubleSpinBoxObservableStartTime.setEnabled(True)
            self.doubleSpinBoxObservableEndTime.setEnabled(True)
        else:
            self.doubleSpinBoxObservableStartTime.setEnabled(False)
            self.doubleSpinBoxObservableEndTime.setEnabled(False)
        self.observable.method = id.text()

    def buttonRestoreOldValuesPressed(self):
        self.setValues(self.x0)

    def buttonSetMaximumPressed(self):
        self.setValues(self.max_value)

    def spinBoxXTolValueChanged(self):
        self.xTol = self.spinBoxXTolValue.value()

    def spinBoxFTolValueChanged(self):
        self.fTol = self.spinBoxFTolValue.value()

    def spinBoxAverageNrChanged(self):
        self.averageNrValue = self.spinBoxAverageNr.value()
        self.observable.dataLength = self.averageNrValue

    def onValueRecieved(self, parameterName, newValue):
        self.observable.setValue(newValue)

    def runOptimization(self):
        if self.runOptimizationButton.text() == "Start":
            self.listWidgetCycle.setEnabled(False)
            self.parameterClass.resetParameters()
            self.parameterClass.addParameters(
                    self.listSelector.getSelectedItemsDict())
            self.x0 = self.parameterClass.getStartVector()
            self.getOptimalValueThread = gOVThread.getOptimalMultiValueThread(
                    self.parameterClass, self.observable, self.algorithmSelection,
                    self.xTol, self.fTol, self.interval_bound)
            self.getOptimalValueThread.signals.setSubscribtion.connect(
                    self.setSubscribtion)
            self.getOptimalValueThread.signals.setValues.connect(
                    self.setValues)
            self.getOptimalValueThread.signals.drawNow.\
                connect(self.visualizeData)
            self.getOptimalValueThread.signals.setMaximum.connect(self.set_maximum)
            self.getOptimalValueThread.signals.jobFinished.connect(self.done)
            self.getOptimalValueThread.start()
            self.runOptimizationButton.setText('Cancel')

        elif self.getOptimalValueThread.isRunning():

            self.getOptimalValueThread.cancelFlag = True
            self.getOptimalValueThread.wait()
            self.getOptimalValueThread.quit()
            self.getOptimalValueThread.wait()
            self.listWidgetCycle.setEnabled(True)
            self.runOptimizationButton.setText('Start')

    def set_maximum(self, x):
        self.max_value = x

    def setValues(self, x):
        self.parameterClass.setNewValues(x)

    def done(self):
        name = self.cycle + '_' + self.observableMethodSelection + '_' +\
            datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
        self.getOptimalValueThread.save(name)
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
        self.set_axes_visible()
        plotFrame =\
            self.getOptimalValueThread.data_frame_graphics.iloc[:, 1:].T           
        init_val = plotFrame.iloc[0, -2]

        def set_label(x):
            return str(int(100*x/init_val))

        self.plotWidget.canvas.axs[1].clear()
#        self.plotWidget.canvas.axs[2].clear()
        self.plotWidget.canvas.axs[0].clear()

        ax_int = self.plotWidget.canvas.axs[1]
        ax_left = self.plotWidget.canvas.axs[2]

#        if plotFrame.shape[0] > 1:

        plotFrame.iloc[:, :-2].plot(ax=self.plotWidget.canvas.axs[0],
                                    colormap='jet')
        plotFrame.iloc[:, -2].plot(ax=ax_int)
        x = plotFrame.index.values
        y = plotFrame.iloc[:, -2].values
        yerr = plotFrame.iloc[:, -1].values
        ax_int.errorbar(x, y, yerr, marker='s',
                        mfc='blue', mec='lime',
                        ms=7, mew=4)
        limits = ax_int.get_ylim()
#        print('upper', limits)
        new_tick_locations = np.linspace(limits[0], limits[1], 10)
        ax_left.set_ylim(limits)
        ax_left.set_yticks(new_tick_locations)
        try:
            ax_left.set_yticklabels(map(set_label, new_tick_locations))
        except:
            pass
        limits = ax_left.get_ylim()
        ax_left.set_ylabel('rel. change (%)')

        self.plotWidget.canvas.axs[0].set_title('Parameter evolution')
        self.plotWidget.canvas.axs[1].set_title('Observable')

        self.plotWidget.canvas.axs[1].set_xlabel('Nr of changes')
        self.plotWidget.canvas.axs[0].set_ylabel('parameters (a.u.)')
        self.plotWidget.canvas.axs[1].set_ylabel(self.
                                                 observableMethodSelection)

        self.plotWidget.canvas.fig.tight_layout()
        limits = ax_int.get_ylim()

        self.plotWidget.canvas.draw()

    def plot_init(self):

        self.set_axes_visible(False)
#        img = mpimg.imread('smiley_rainbow_round.jpg')
#        self.plotWidget.canvas.axs[1].imshow(img)
        self.plotWidget.canvas.axs[1].text(self.plotWidget.canvas.axs[1]
                                           .get_xlim()[1]/3, .5,
                                           r'Stay tuned...',
                                           fontsize=30)
        self.plotWidget.canvas.axs[0].text(self.plotWidget.canvas.axs[1]
                                           .get_xlim()[1]/4, .5,
                                           zen.Zen().get_text(),
                                           fontsize=14)

    def set_axes_visible(self, setting=True):

        self.plotWidget.canvas.axs[0].axes.get_xaxis().set_visible(setting)
        self.plotWidget.canvas.axs[0].axes.get_yaxis().set_visible(setting)
        self.plotWidget.canvas.axs[1].axes.get_xaxis().set_visible(setting)
        self.plotWidget.canvas.axs[1].axes.get_yaxis().set_visible(setting)
        self.plotWidget.canvas.axs[2].axes.get_xaxis().set_visible(setting)   
        self.plotWidget.canvas.axs[2].axes.get_yaxis().set_visible(setting)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.setSubscribtion(False)
            event.accept()
        else:
            event.ignore()


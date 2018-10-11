#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:48:23 2018

@author: shirlaen
"""
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time
from scipy import optimize
import numpy as np
import pandas as pd


class CommuticatorSignals(QObject):

    drawNow = pyqtSignal()
    jobFinished = pyqtSignal()
    setValues = pyqtSignal(list)
    setSubscribtion = pyqtSignal(bool)


class getOptimalMultiValueThread(QThread):

    def __init__(self, parameterClass, observableParameter, algorithmSelection,
                 xTol, fTol):

        QThread.__init__(self)

        self.ob = observableParameter
        self.parameterClass = parameterClass
        self.index = self.parameterClass.getNames()
        self.index.extend(["intensity", "error"])
        self.parameterEvolution = pd.DataFrame(
                index=self.index)

        self.cancelFlag = False
        self.signals = CommuticatorSignals()
        self.nrCalls = 0
        self.startValues = np.array(self.parameterClass.getStartVector())
        self.data_storage_frame = pd.DataFrame()
        self.data_frame_graphics = pd.DataFrame()

        self.xTol = xTol
        self.fTol = fTol
        self.algorithmSelection = algorithmSelection
# Methods...
        self.updateData(self.startValues, np.nan, np.nan)

    def updateData(self, x, intensityValue, errorValue):
        print(x)
        self.parameterEvolution[self.nrCalls] = np.nan
        self.parameterEvolution.iloc[:-2,
                                     self.nrCalls] = np.array(x).flatten()
        self.parameterEvolution.iloc[-2:,
                                     self.nrCalls] = [intensityValue,
                                                      errorValue]
        print(self.parameterEvolution)
        observables_list = self.ob.valueList
        # TODO: add to storage
        self.data_storage_frame =\
            self.data_storage_frame.append(pd.DataFrame(observables_list,
                                           columns=[self.nrCalls]).T)

    def save_run(self, name):
        pd.concat([self.parameterEvolution.iloc[:-1, :].T,
                  self.data_storage_frame], axis=1,
                  keys=['parameters', 'observable']).to_csv(name)

    def __del__(self):
        self.wait()

    def run(self):
        self.signals.setSubscribtion.emit(True)
        x0 = self.startValues
#        print(self.parameterClass.getStartDirection())
        if self.algorithmSelection == 'Powell':
            res = optimize.fmin_powell(self._func_obj, x0, xtol=self.xTol,
                                       ftol=self.fTol,
                                       direc=self.parameterClass.
                                       getStartDirection())
            if (len(res.shape) < 0) | (type(res) == float):
                res = np.array([res])
#            returnValue = res
        else:
            res = optimize.minimize(self._func_obj, x0, method='Nelder-Mead',
                                    options={'xatol': self.xTol,
                                             'fatol': self.fTol})
#            returnValue = res.x
#        self.signals.setValues.emit(returnValue.tolist())
        self.signals.jobFinished.emit()
        self.signals.setSubscribtion.emit(False)

    def update_graphics(self, x):
        self.data_frame_graphics = self.parameterEvolution.copy()
        self.data_frame_graphics[self.nrCalls + 1] = np.nan
        print('update_graphics')
        self.data_frame_graphics.iloc[:-2, self.nrCalls + 1]\
            = np.array(x).flatten()
        intensityValues = self.ob.valueList
        values = [(-1)*np.mean(intensityValues),
                  np.sqrt(np.std(intensityValues) /
                  len(intensityValues))]
        print(values)
        self.data_frame_graphics.iloc[-2:, self.nrCalls + 1] =\
            np.array(values).flatten()
        print(self.data_frame_graphics)
        self.signals.drawNow.emit()

    def _func_obj(self, x):
        self.signals.setValues.emit(x.tolist())
        self.ob.reset()
        while(self.ob.dataWait):
            if self.cancelFlag:
                self.signals.setSubscribtion.emit(False)
                # TODO : check saving in this case
                self.terminate()
            self.update_graphics(x-self.parameterEvolution.iloc[:-2, 0])
            time.sleep(2)
        self.ob.dataWait = True
        dataFinal = self.ob.dataOut
        self.nrCalls += 1
        self.updateData(x-self.parameterEvolution.iloc[:-2, 0],
                        (-1) * self.ob.dataOut, self.ob.dataErrorOut)
        self.signals.drawNow.emit()
        return dataFinal

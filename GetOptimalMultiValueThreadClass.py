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


class CommuticatorSingals(QObject):

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
        index = self.parameterClass.getNames()
        index.append("intensity")
        self.parameterEvolution = pd.DataFrame(
                index=index)

        self.cancelFlag = False
        self.signals = CommuticatorSingals()
        self.nrCalls = 0
        self.startValues = np.array(self.parameterClass.getStartVector())
        self.updateData(self.startValues, np.nan)

        self.xTol = xTol
        self.fTol = fTol
        self.algorithmSelection = algorithmSelection

    def updateData(self, x, intensityValue):
        self.parameterEvolution[self.nrCalls] = np.nan
        self.parameterEvolution.iloc[:-1,
                                     self.nrCalls] = x
        self.parameterEvolution.iloc[-1,
                                     self.nrCalls] = intensityValue
        print(self.parameterEvolution)

    def __del__(self):
        self.wait()

    def run(self):
        print(self.xTol)
        print(self.fTol)
        self.signals.setSubscribtion.emit(True)
        x0 = self.startValues
        print(self.parameterClass.getStartDirection())
        if self.algorithmSelection == 'Powell':
            res = optimize.fmin_powell(self._func_obj, x0, xtol=self.xTol,
                                       ftol=self.fTol,
                                       direc=self.parameterClass.
                                       getStartDirection())
            if (len(res.shape) < 0) | (type(res) == float):
                res = np.array([res])
            returnValue = res
        else:
            res = optimize.minimize(self._func_obj, x0, method='Nelder-Mead',
                                    options={'xatol': self.xTol,
                                             'fatol': self.fTol})
            returnValue = res.x
        self.signals.setValues.emit(returnValue.tolist())
        self.signals.jobFinished.emit()
        self.signals.setSubscribtion.emit(False)

    def _func_obj(self, x):
        self.signals.setValues.emit(x.tolist())
        self.ob.reset()
        while(self.ob.dataWait):
            if self.cancelFlag:
                self.signals.setSubscribtion.emit(False)
                self.terminate()
            time.sleep(2)
        self.ob.dataWait = True
        dataFinal = self.ob.dataOut
        self.nrCalls += 1
        self.updateData(x-self.parameterEvolution.iloc[:-1, 0],
                        (-1) * self.ob.dataOut)
        self.signals.drawNow.emit()
        return dataFinal

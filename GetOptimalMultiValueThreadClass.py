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

        self.parameterEvolution = pd.DataFrame(
                index=['ei.v10', 'ei.v20', 'ei.h10', 'ei.h20-inj'])

        self.injIntensityEvolution = []
        self.ob = observableParameter
        self.parameterClass = parameterClass
        self.cancelFlag = False
        self.signals = CommuticatorSingals()
        self.nrCalls = 0
        self.startValues = np.array(self.parameterClass.getValues())
        self.parameterEvolution[0] = self.startValues

        self.xTol = xTol
        self.fTol = fTol
        self.algorithmSelection = algorithmSelection

    def __del__(self):
        self.wait()

    def run(self):
        self.signals.setSubscribtion.emit(True)
        x0 = self.startValues
        if self.algorithmSelection == 'Powell':
            res = optimize.fmin_powell(self._func_obj, x0, xtol=self.xTol,
                                   ftol=self.fTol,
                                   direc=np.array([[1e-4, 0., 0., 0.],
                                                  [0, 1e-4, 0., 0.],
                                                  [0, 0, 1e-4, 0.],
                                                  [0, 0, 0, 1e-4]]))
        else:
            res = optimize.minimize(self._func_obj, x0, method='Nelder-Mead',
                                      options={'xatol': self.xTol,
                                      'fatol': self.fTol})
        self.signals.setValues.emit(res.tolist())
        self.signals.jobFinished.emit()
        self.signals.setSubscribtion.emit(False)

    def _func_obj(self, x):
        self.signals.setValues.emit(x.tolist())
        while(self.ob.dataWait):
            if self.cancelFlag:
                self.signals.setSubscribtion.emit(False)
                self.terminate()
            time.sleep(2)
        self.ob.dataWait = True
        dataFinal = self.ob.dataOut
        self.nrCalls += 1
        self.parameterEvolution[self.nrCalls] = x-self.parameterEvolution[0]
        self.injIntensityEvolution.append((-1) * self.ob.dataOut)
        self.signals.drawNow.emit()

        return dataFinal

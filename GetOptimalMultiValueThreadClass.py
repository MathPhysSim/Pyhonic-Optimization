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
import os


class CommuticatorSignals(QObject):
    drawNow = pyqtSignal()
    jobFinished = pyqtSignal()
    setValues = pyqtSignal(list)
    setSubscribtion = pyqtSignal(bool)
    setMaximum = pyqtSignal(list)


class getOptimalMultiValueThread(QThread):

    def __init__(self, parameterClass, observableParameter, algorithmSelection,
                 xTol, fTol, interval_bound):

        QThread.__init__(self)

        self.ob = observableParameter
        self.parameterClass = parameterClass
        self.index = self.parameterClass.getNames()
        self.index.extend(["intensity", "error"])
        self.parameterEvolution = pd.DataFrame(index=self.index)
        self.cancelFlag = False
        self.signals = CommuticatorSignals()
        self.nrCalls = 0
        self.start_values = np.array(self.parameterClass.getStartVector())
        self.minimalAcceptedChangeVector = np.array(self.parameterClass.getMinimalAcceptedChangeVector())
        self.bounds = self.parameterClass.getBounds()
        self.data_storage_frame = pd.DataFrame()
        self.data_frame_graphics = pd.DataFrame()

        self.xTol = xTol
        self.fTol = fTol
        self.interval_bound = interval_bound
        #        print(self.fTol)
        self.algorithmSelection = algorithmSelection
        self.data_max = pd.DataFrame()
        # Methods...
        self.updateData(self.start_values, np.nan, np.nan)

    def updateData(self, x, intensityValue, errorValue):
        # print(x)
        self.parameterEvolution[self.nrCalls] = np.nan
        self.parameterEvolution.iloc[:-2,
        self.nrCalls] = np.array(x).flatten()
        self.parameterEvolution.iloc[-2:,
        self.nrCalls] = [intensityValue,
                         errorValue]
        print(self.parameterEvolution)
        observables_list = self.ob.valueListBuffer
        observables_list = np.array(observables_list) * (-1)
        self.data_storage_frame = \
            self.data_storage_frame.append(pd.DataFrame(observables_list,
                                                        columns=[self.nrCalls]).T)

    def save(self, name):
        save_path = 'saved_data/'
        name = save_path + name
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        pd.concat([self.parameterEvolution.iloc[:-2, :].T,
                   self.data_storage_frame], axis=1).to_csv(name)

    def __del__(self):
        self.wait()

    def update_graphics(self, x):
        "updates graphics and max value"
        self.data_frame_graphics = self.parameterEvolution.copy()
        self.data_frame_graphics[self.nrCalls + 1] = np.nan
        self.data_frame_graphics.iloc[:-2, self.nrCalls + 1] \
            = np.array(x).flatten()
        intensityValues = self.ob.valueList
        values = [(-1) * np.mean(intensityValues),
                  np.std(intensityValues) /
                  np.sqrt(len(intensityValues))]
        self.data_frame_graphics.iloc[-2:, self.nrCalls + 1] = \
            np.array(values).flatten()
        max_idx = self.data_frame_graphics.iloc[-2, :].idxmax()
        if not (np.isnan(max_idx)):
            self.data_max = self.data_frame_graphics.iloc[:, max_idx]
            self.signals.setMaximum.emit((self.data_max.iloc[:-2]
                                          + self.parameterEvolution.
                                          iloc[:-2, 0]).tolist())
        self.signals.drawNow.emit()

    def set_function(self, x):
        print(type(x))
        print(self.parameterEvolution)
        if self.nrCalls > 1:
            previous_change = self.parameterEvolution.iloc[:-2, self.nrCalls]
            current_change = x - self.parameterEvolution.iloc[:-2, 0]
            small_change = (abs(current_change - previous_change) < self.minimalAcceptedChangeVector).all()
        else:
            small_change = False
        # small_change = False
        if (small_change):
            print(10 * 'in case')
            dataFinal = (-1) * self.parameterEvolution.iloc[-2, self.nrCalls]
            intensity = self.parameterEvolution.iloc[-2, self.nrCalls]
            error = self.parameterEvolution.iloc[-1, self.nrCalls]
            self.update_graphics(x - self.parameterEvolution.iloc[:-2, 0])
            time.sleep(.1)
        else:
            self.signals.setValues.emit(x.tolist())
            self.ob.reset()
            while (self.ob.dataWait):
                if self.cancelFlag:
                    self.signals.setSubscribtion.emit(False)
                    # TODO : check saving in this case
                    self.terminate()
                self.update_graphics(x - self.parameterEvolution.iloc[:-2, 0])
                time.sleep(2)

            self.ob.dataWait = True
            dataFinal = self.ob.dataOut
            intensity = (-1) * self.ob.dataOut
            error = self.ob.dataErrorOut

        self.nrCalls += 1
        self.updateData(x - self.parameterEvolution.iloc[:-2, 0], intensity, error)
        self.signals.drawNow.emit()

        return dataFinal

    def wrapper_fun(self, x):
        x = np.asarray([x])
        return self.set_function(x)

    def taxi_cab(self, start_values):
        current_values = start_values

        def select_element_fun(x, nr_element):
            current_values[nr_element] = x
            return self.set_function(current_values)

        for nr in range(len(current_values)):
            bounds = np.array(self.bounds[nr])
            bounds = bounds + start_values[nr]
            print('bounds: ', bounds)
            res = optimize.fminbound(lambda trim_lambda: (select_element_fun(trim_lambda, nr)),
                                     bounds[0], bounds[1], xtol=self.xTol)


    def run(self):
        self.signals.setSubscribtion.emit(True)
        start_values = self.start_values
        print(start_values.shape[0])

        # print(self.parameterClass.getStartDirection())
        # DOTO: add linear search
        if self.algorithmSelection == 'Powell':
            bounds_delta = self.interval_bound
            bounds = [start_values[0] - bounds_delta, start_values[0] + bounds_delta]
            if start_values.shape[0] == 1:
                print('Use fminbound')
                res = optimize.fminbound(self.wrapper_fun, bounds[0], bounds[1], xtol=self.xTol)
            if True:
                self.taxi_cab(start_values)

            else:
                print('Use Powell')
                res = optimize.fmin_powell(self.set_function, start_values, xtol=self.xTol,
                                           ftol=self.fTol,
                                           direc=self.parameterClass.
                                           getStartDirection())
                if (len(res.shape) < 0) | (type(res) == float):
                    res = np.array([res])
        #            returnValue = res
        else:
            res = optimize.minimize(self.set_function, start_values, method='Nelder-Mead',
                                    options={'xatol': self.xTol,
                                             'fatol': self.fTol})
        #            returnValue = res.x
        #        self.signals.setValues.emit(returnValue.tolist())
        self.signals.jobFinished.emit()
        self.signals.setSubscribtion.emit(False)

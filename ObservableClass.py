#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:41:13 2018

@author: shirlaen
"""

import numpy as np
import pandas as pd

class ObservableClass():

    def __init__(self, japc, length=5):
        self.valueList = []
        self.valueListBuffer = []
        self.japc = japc
        self.dataOut = False
        self.dataErrorOut = False
        self.dataWait = True
        self.dataLength = length
        self.method = 'Maximum'
        self.time_interval = np.array([0, 0])
        # self.observableClass = ObservableClassSchottky(self.japc)

        self.observableClass = ObservableClassIntensity(self.time_interval, self.japc, self.method)

    def setValue(self, data_acquisiton_in):
        observable_value = self.observableClass.create_observable(data_acquisiton_in)
        self.valueList.append(observable_value)

        if len(self.valueList) >= self.dataLength:
            cleanData = self.valueList
            # if len(cleanData) > 2:
            #     cleanData = np.sort(np.array(cleanData))

            self.dataOut = np.median(cleanData)
            self.dataErrorOut = np.std(cleanData)/np.sqrt(len(cleanData))
            self.valueListBuffer = self.valueList
            self.valueList = []
            self.dataWait = False

    def reset(self):
        self.valueList = []


class ObservableClassSchottky():

    def __init__(self, japcIn):
        self.japc = japcIn
        self.dataFrame = np.array([])
        self.acquisition = self.japc.getParam("LEI.BQS.L/Acquisition")
        self.settings = self.japc.getParam("LEI.BQS.L/Setting")
        self.currentTimeVector = 0
        self.deltapoverp = 0


    def setData(self, value):
        value = np.flipud(np.reshape(value, (self.acquisition['nWindows'], -1)))
        timeVector = self.acquisition['windowMsStamp'][::-1]
        self.currentTimeVector = timeVector
        fVector = (np.arange(value.shape[-1]) * self.acquisition['df'] + \
                   self.acquisition['spectralZoomStartFreqHz'])
        f0 = 36.1e6
        eta = -0.867
        fact = -1 / eta
        self.deltapoverp = (fVector - f0) / f0 * fact * 1e3
        self.dataFrame = pd.DataFrame(value, index=timeVector, columns=self.deltapoverp)

    def getData(self):
        return self.dataFrame

    def getStatistics(self, sliceNr):
        outFrame = pd.DataFrame(index=['1.mom', '2.mom'])
        df = self.dataFrame.iloc[sliceNr, :]
        first_moment = (df / df.sum() * df.index.values).sum()
        second_moment = np.sqrt((df / df.sum() * (df.index.values - first_moment) ** 2).sum())
        outFrame[0] = [first_moment, second_moment]
        return outFrame.T

    def acquireData(self, value):
        self.acquisition = value #self.japc.getParam("LEI.BQS.L/Acquisition")
        self.setData(self.acquisition['spectralZoomDftPow'])

    def updateSettings(self):
        self.settings = self.japc.getParam("LEI.BQS.L/Setting")

    def setSettings(self, myFields):
        self.japc.setParam("LEI.BQS.L/Setting", myFields)
        self.updateSettings()

    def getSettings(self):
        x = self.japc.getParam("LEI.BQS.L/Setting")
        self.updateSettings()
        return x

    def get_observable(self):
        processe_observable = (self.getStatistics(2)['2.mom'])**2+(self.getStatistics(2)['1.mom']-0.15)**2
        return processe_observable

    def create_observable(self, in_data):
        self.acquireData(in_data)
        return (self.get_observable())

class ObservableClassIntensity:

    def __init__(self, time_interval, japc_in, method):

        self.timeInterval = time_interval
        self.japc = japc_in
        self.acquisition = None
        self.intensity_values = np.array([])
        self.observable_value = False
        self.method = method


    def acquire_data(self, value):
            self.acquisition = value

    def process_data(self):
        self.observable_value = False
        self.intensity_values = np.array(self.acquisition['intensities'][395:]) * (-1)
        if self.method == 'Maximum':
            observable_value = np.min(self.intensity_values)
        elif self.method == 'Area':
            observable_value = np.mean(self.intensity_values[self.timeInterval[0]:self.timeInterval[1]])
            # self.valueList.append(observable_value)
        elif self.method == 'Transmission':
            #            observable_value = (in_array[self.timeInterval[1]]/in_array[self.timeInterval[0]])
            observable_value = (self.intensity_values[self.timeInterval[0]])
            #            observable_value = (in_array[self.timeInterval[0]])
            norm_val = self.japc.getParam("EI.BCT10/Acquisition#chargesLinacSingle")
            if norm_val > 0.15:
                observable_value = (observable_value / norm_val)
        return observable_value

    def create_observable(self, in_data):
        self.acquire_data(in_data)
        return self.get_observable()

    def get_observable(self):
        return self.process_data()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:41:13 2018

@author: shirlaen
"""

import numpy as np


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
        self.timeInterval = np.array([0, 0])

    def setValue(self, inArray):
        inArray = np.array(inArray[395:])*(-1)
#        print('inArray')
#        print(inArray)
        if self.method == 'Maximum':
            x = np.min(inArray)
        elif self.method == 'Area':
#            x = np.mean(inArray[self.timeInterval[0]:self.timeInterval[1]])
#             print("Value xtime")
#             print(self.timeInterval)
             x = np.mean(inArray[self.timeInterval[0]:self.timeInterval[1]])
#             print("Value x")
#             print(x)
        elif self.method == 'Transmission':

            x = (-1)*(inArray[self.timeInterval[1]]/inArray[self.timeInterval[0]])
#        normVal = self.japc.getParam("EI.BCT10/Acquisition#chargesLinacSingle")
#        if normVal > 2:
#            self.valueList.append(x/normVal)
        self.valueList.append(x)
        if len(self.valueList) >= self.dataLength:
            cleanData = self.valueList
            if len(cleanData) > 2:
                cleanData = np.sort(np.array(cleanData))
            self.dataOut = np.median(cleanData)
            self.dataErrorOut = np.std(cleanData)/np.sqrt(len(cleanData))
            self.valueListBuffer = self.valueList
            self.valueList = []
            self.dataWait = False

    def reset(self):
        self.valueList = []

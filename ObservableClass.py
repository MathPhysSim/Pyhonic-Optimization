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
        self.japc = japc
        self.dataOut = False
        self.dataWait = True
        self.dataLength = length

    def setValue(self, x):
#        normVal = self.japc.getParam("ITL.BCT05/Acquisition")
        self.valueList.append(x)
        if len(self.valueList) >= self.dataLength:
            cleanData = self.valueList
            if len(cleanData) > 2:
                cleanData = np.sort(np.array(cleanData))[2:]
            self.dataOut = np.median(cleanData)
            self.valueList = []
            self.dataWait = False

    def reset(self):
        self.valueList = []

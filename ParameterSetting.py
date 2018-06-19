#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:27:52 2018

@author: shirlaen
"""

import numpy as np


class ParameterClass():

    def __init__(self, japcIn):
        self.japc = japcIn
        self.memberParameters = {}

    def addParameters(self, namesDict):
        for key in namesDict:
            print(key)
            self.memberParameters[key] = (parameterObject(self.japc,
                                          namesDict[key]))

    def resetParameters(self):
        self.memberParameters = {}

    def getStartVector(self):
        startVector = [self.memberParameters[key].x0 for key
                       in self.memberParameters]
        return startVector

    def getStartDirection(self):
        return np.diag([5e-4 for ii in range(len(self.memberParameters))])

    def setNewValues(self, x):
        x = np.array(x)
        xReal = []
        xSet = []
        for ii, key in enumerate(self.memberParameters):
            self.memberParameters[key].setValue(x[ii])
            xReal.append(self.memberParameters[key].getValue())
            xSet.append(x[ii])

    def getValues(self):
        xOut = []
        for key in (self.memberParameters):
            xOut.append(self.memberParameters[key].getValue())
        return np.array(xOut)

    def getNames(self):
        return [key for key in self.memberParameters]


class parameterObject():

    def __init__(self, japcIn, parameterNameDict):

        self.japc = japcIn
        self.parameterName = parameterNameDict['name']
        self.parameterType = parameterNameDict['type']

        if self.parameterType == 'function':
            self.object = constFunctionClass(japcIn, self.parameterName,
                                             parameterNameDict['time'])
        elif self.parameterType == 'functionSquare':
            self.object = squareFunctionClass(japcIn, self.parameterName,
                                             parameterNameDict['time'])
        else:
            self.object = scalarClass(japcIn, self.parameterName)
        self.x0 = self.getValue()

    def getValue(self):
        return self.object.getValue()

    def setValue(self, x):
        self.object.setValue(x)
        return None


class constFunctionClass():
#    t1 = 200
#    t2 = 1850

    def __init__(self, japcIn, elementName, t):

        self.japc = japcIn
        self.elementName = elementName
        self.t = t

    def getValue(self):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = np.array(app.getDiscreteFunction().xArray)
        Qtrim = np.array(app.getDiscreteFunction().yArray)
        ind_select = np.where(
                (np.array(time) >= self.t[0]) & (np.array(time) <= self.t[1]))

        return Qtrim[ind_select][0]

    def setValue(self, setValue):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = app.getDiscreteFunction().xArray
        Qtrim = np.array(app.getDiscreteFunction().yArray)
        Qtrim[np.where((np.array(time) >= self.t[0]) &
                       (np.array(time) <= self.t[1]))] = setValue
        app.getDiscreteFunction().yArray = Qtrim
        try:
            self.japc.setParam(self.elementName, app,
                               dimcheck=True)
        except Exception as e:
            print(e.stacktrace())


class scalarClass():

    def __init__(self, japcIn, parameterName):

        self.japc = japcIn
        self.parameterName = parameterName

    def getValue(self):
        knobParam = self.japc.getParam(self.parameterName,
                                       noPyConversion=True,
                                       timingSelectorOverride=
                                       self.japc.getSelector()).getValue()
        returnValue = knobParam.double
        return returnValue

    def setValue(self, x):
        knobParam = self.japc.getParam(self.parameterName,
                                       noPyConversion=True,
                                       timingSelectorOverride=
                                       self.japc.getSelector()).getValue()
        knobParam.double = x
        self.japc.setParam(self.parameterName, knobParam)
        return None

class squareFunctionClass():
#    t1 = 200
#    t2 = 1850

    def __init__(self, japcIn, elementName, t):

        self.japc = japcIn
        self.elementName = elementName
        self.t = t
        self.initiate = False

    def initiateValues(self):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = np.array(app.getDiscreteFunction().xArray, dtype=float)
        Qtrim = np.array(app.getDiscreteFunction().yArray, dtype=float)
        print('here......................................................')
        print(time)
        print(Qtrim)
        delta = 10.
        timeLim = self.t[0]
        if not(timeLim in time):
            time = np.insert(time, np.where(time > timeLim)[0][0], timeLim)
        timeLim = max([self.t[0] - delta, 0])
        if not(timeLim in time):
            time = np.insert(time, np.where(time > timeLim)[0][0], timeLim)

        timeLim = self.t[1]
        if not(timeLim in time):
            time = np.insert(time, np.where(time > timeLim)[0][0], timeLim)
        timeLim = self.t[1] + delta
        if not(timeLim in time):
            time = np.insert(time, np.where(time > timeLim)[0][0], timeLim)

        Qtrim = np.interp(time, np.array(app.getDiscreteFunction().xArray,
                                         dtype=float), Qtrim)
        print('here......................................................')
        print(time)
        print(Qtrim)
        
        app.getDiscreteFunction().yArray = Qtrim
        app.getDiscreteFunction().xArray = time

        try:
            self.japc.setParam(self.elementName, app,
                               dimcheck=True)
            self.initiate = True
        except Exception as e:
            print(e.stacktrace())

    def getValue(self):
        if not(self.initiate):
            self.initiateValues() 
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = np.array(app.getDiscreteFunction().xArray)
        Qtrim = np.array(app.getDiscreteFunction().yArray)
        ind_select = np.where(
                (np.array(time) >= self.t[0]) & (np.array(time) <= self.t[1]))

        return Qtrim[ind_select][0]

    def setValue(self, setValue):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = app.getDiscreteFunction().xArray
        Qtrim = np.array(app.getDiscreteFunction().yArray)
        Qtrim[np.where((np.array(time) >= self.t[0]) &
                       (np.array(time) <= self.t[1]))] = setValue
        app.getDiscreteFunction().yArray = Qtrim
        try:
            self.japc.setParam(self.elementName, app,
                               dimcheck=True)
        except Exception as e:
            print(e.stacktrace())

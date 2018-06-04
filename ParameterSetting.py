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
        return np.diag([1e-4 for ii in range(len(self.memberParameters))])

    def setNewValues(self, x):
        x = np.array(x)
        print("Set values in class")
        xReal = []
        xSet = []
        for ii, key in enumerate(self.memberParameters):
            print("Try...................................")
            print(key)
            print(self.memberParameters[key].getValue())
            print(x[ii])
            self.memberParameters[key].setValue(x[ii])
            xReal.append(self.memberParameters[key].getValue())
            xSet.append(x[ii])
            print("GetSet...................................")
            print(xSet)
            print(xReal)
            print("GetSet...................................")

    def getValues(self):
        xOut = []
        for key in (self.memberParameters):
            xOut.append(self.memberParameters[key].getValue())
        return np.array(xOut)

    def getNames(self):
        return [key for key in self.memberParameters]


class parameterObject():

    def __init__(self, japcIn, parameterNameDict):
        print("success para0")
        self.japc = japcIn
        self.parameterName = parameterNameDict['name']
        self.parameterType = parameterNameDict['type']
        print("success para1")
        if self.parameterType == 'function':
            self.object = constFunctionClass(japcIn, self.parameterName,
                                             parameterNameDict['time'])
        else:
            self.object = scalarClass(japcIn, self.parameterName)
        self.x0 = self.getValue()
        print("success para2")
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
        except:


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

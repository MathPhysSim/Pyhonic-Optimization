#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:27:52 2018

@author: shirlaen
"""

import numpy as np
import pandas as pd

class ParameterClass():

    def __init__(self, japcIn):
        self.japc = japcIn
        self.memberParameters = {}

    def addParameters(self, namesDict):
        for key in namesDict:
            self.memberParameters[key] = (parameterObject(self.japc,
                                          namesDict[key]))

    def resetParameters(self):
        self.memberParameters = {}

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
        self.parameterStartDirection = parameterNameDict['startDirection']
#        print("parameterObject")
        if self.parameterType == 'function':
            self.object = constFunctionClass(japcIn, self.parameterName,
                                             parameterNameDict['time'])
        elif self.parameterType == 'functionSquare':
#            print("parameterObject1")
            self.object = squareFunctionClass(japcIn, self.parameterName,
                                              parameterNameDict['time'],
                                              parameterNameDict['delta'],
                                              parameterNameDict['range'])
#            print("parameterObject2")
        elif self.parameterType == 'functionList':
            self.object = constFunctionListClass(japcIn, self.parameterName,
                                              parameterNameDict['time'])
        elif self.parameterType == 'scalarNonLSA':
            self.object = scalarClassNonLsa(japcIn, self.parameterName)    
        else:
            self.object = scalarClass(japcIn, self.parameterName)
#        print("parameterObject3")    
        self.x0 = self.getValue()
#        print("parameterObject4")

    def getValue(self):
        return self.object.getValue()

    
class constFunctionListClass():
#    t1 = 200
#    t2 = 1850
    
    def __init__(self, japcIn, elementName, t):
        self.japc = japcIn
        self.elementName = elementName
#        print(self.elementName)
        self.t = t

    def getValue(self):
        try:
            app = self.japc.getParam(self.elementName,
                                     noPyConversion=True).getValue()
#            print(app)
            time = np.array(app.getDiscreteFunctionList().getFunctions()[0].xArray)
            Qtrim = np.array(app.getDiscreteFunctionList().getFunctions()[0].yArray)
            ind_select = np.where(
                    (np.array(time) >= self.t[0]) & (np.array(time) <= self.t[1]))
#            print(Qtrim[ind_select][0])
            return Qtrim[ind_select][0]


        except Exception as e:
#            print("pos x1")
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


class scalarClassNonLsa():

    def __init__(self, japcIn, parameterName):

        self.japc = japcIn
        self.parameterName = parameterName

    def getValue(self):
        knobParam = self.japc.getParam(self.parameterName,
                                       timingSelectorOverride=
                                       self.japc.getSelector())
        return knobParam

    
    

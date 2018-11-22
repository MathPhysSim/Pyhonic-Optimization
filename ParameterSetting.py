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

    def getStartVector(self):
        startVector = [self.memberParameters[key].x0 for key
                       in self.memberParameters]
        return startVector

    def getMinimalAcceptedChangeVector(self):
        minimalAcceptedChangeVector = [self.memberParameters[key].minimalAcceptedChange for key
                       in self.memberParameters]
        return minimalAcceptedChangeVector

    def getStartDirection(self):
        startVec = []
        for key in self.memberParameters:
            startVec.append(self.memberParameters[key].parameterStartDirection)
        return np.diag(startVec)

    def getBounds(self):
        bounds = []
        for key in self.memberParameters:
            bounds.append(self.memberParameters[key].bounds)
        return bounds

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

    def __init__(self, japcIn, parameter_name_dict_entry):

        self.japc = japcIn
        self.parameterName = parameter_name_dict_entry['name']
        self.parameterType = parameter_name_dict_entry['type']
        self.parameterStartDirection = parameter_name_dict_entry['startDirection']
        self.bounds = parameter_name_dict_entry['bounds']

        if self.parameterType == 'function':
            self.object = delta_function(japcIn, self.parameterName,
                                         parameter_name_dict_entry['time'])
        elif self.parameterType == 'functionSquare':
            self.object = delta_function(japcIn, self.parameterName,
                                         parameter_name_dict_entry['time'])
        # elif self.parameterType == 'functionSquare':
        #     self.object = squareFunctionClass(japcIn, self.parameterName,
        #                                       parameterNameDict['time'],
        #                                       parameterNameDict['delta'],
        #                                       parameterNameDict['range'])
        elif self.parameterType == 'functionList':
            self.object = constFunctionListClass(japcIn, self.parameterName,
                                                 parameter_name_dict_entry['time'])
        elif self.parameterType == 'scalarNonLSA':
            self.object = scalarClassNonLsa(japcIn, self.parameterName)    
        else:
            self.object = scalarClass(japcIn, self.parameterName)
        self.x0 = self.getValue()
        self.minimalAcceptedChange = parameter_name_dict_entry["minimalAcceptedChange"]



    def getValue(self):
        return self.object.getValue()

    def setValue(self, x):
        self.object.setValue(x)
        return None
    
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

    
    def setValue(self, setValue):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = np.array(app.getDiscreteFunctionList().getFunctions()[0].xArray)
        Qtrim = np.array(app.getDiscreteFunctionList().getFunctions()[0].yArray)
        Qtrim[np.where((np.array(time) >= self.t[0]) &
                       (np.array(time) <= self.t[1]))] = setValue
        app.getDiscreteFunctionList().getFunctions()[0].yArray = Qtrim
        try:
            self.japc.setParam(self.elementName, app,
                               dimcheck=True)
        except Exception as e:
            print(e.stacktrace())

class constFunctionClass():
    
    def __init__(self, japcIn, elementName, t):
#        print("constantFunctionClassHIHI")
        self.japc = japcIn
        self.elementName = elementName
#        print(self.elementName)
        self.t = t

    def getValue(self):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        
        time = np.array(app.getDiscreteFunction().xArray)
#        print(time)
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

class delta_function():

    def __init__(self, japcIn, elementName, t):
        self.japc = japcIn
        self.elementName = elementName
        self.t = t
        self.initial_array = self.get_initial_array()
        self.current_off_set = 0

    def get_initial_array(self):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = np.array(app.getDiscreteFunction().xArray)
        Qtrim = np.array(app.getDiscreteFunction().yArray)
        Qtrim = Qtrim[np.where((np.array(time) >= self.t[0]) &
                       (np.array(time) <= self.t[1]))]
        return Qtrim


    def setValue(self, set_value):
        self.current_off_set = set_value
        self.setValues(self.initial_array + self.current_off_set)

    def getValue(self):
        return self.current_off_set

    def setValues(self, set_array):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
        time = app.getDiscreteFunction().xArray
        Qtrim = np.array(app.getDiscreteFunction().yArray)
        Qtrim[np.where((np.array(time) >= self.t[0]) &
                       (np.array(time) <= self.t[1]))] = set_array
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


class scalarClassNonLsa():

    def __init__(self, japcIn, parameterName):

        self.japc = japcIn
        self.parameterName = parameterName

    def getValue(self):
        knobParam = self.japc.getParam(self.parameterName,
                                       timingSelectorOverride=
                                       self.japc.getSelector())
        return knobParam

    def setValue(self, x):
        self.japc.setParam(self.parameterName, x)
        return None
    
    
class squareFunctionClass():
#    t1 = 200
#    t2 = 1850

    def __init__(self, japcIn, elementName, t, delta, dataRange):

        self.japc = japcIn
        self.elementName = elementName
        self.t = t
        self.delta = delta
        self.initiate = False
        self.dataRange = dataRange
#        print("squareFunctionClass")
        
    def initiateValues(self):
        app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()

        valueFrame = pd.DataFrame(np.array(app.getDiscreteFunction().yArray),
                                  index = np.array(app.getDiscreteFunction().xArray)).T
#        print(valueFrame.T)
                
        delta = self.delta
        timeLim = self.t[0]
        if not(timeLim in valueFrame.columns):
            valueFrame[timeLim] = np.nan             
        timeLim = max([timeLim - delta, self.dataRange[0]])
        if not(timeLim in valueFrame.columns):
            valueFrame[timeLim] = np.nan

        timeLim = self.t[1]
        if not(timeLim in valueFrame.columns):
            valueFrame[timeLim] = np.nan

        timeLim = min([timeLim + delta, self.dataRange[1]])
        if not(timeLim in valueFrame.columns):
            valueFrame[timeLim] = np.nan
        valueFrame.sort_index(inplace=True, axis=1)
#        print(valueFrame.T)
        valueFrame = valueFrame.interpolate(axis=1)
#        print("interpolate")
#        print(valueFrame.T)

        app.getDiscreteFunction().yArray = valueFrame.values[0]
        app.getDiscreteFunction().xArray = valueFrame.columns.values
#        print("allmost")
        try:
            self.japc.setParam(self.elementName, app)
            self.initiate = True
#            print("done")
        except Exception as e:
#            print("pos x1")
            print(e.stacktrace())

    def getValue(self):
#        print("getValue1")
        if not(self.initiate):
#            print("getValue2")
            self.initiateValues()
#        print("getValue3")    
        try:
            app = self.japc.getParam(self.elementName,
                                 noPyConversion=True).getValue()
            valueFrame = pd.DataFrame(np.array(app.getDiscreteFunction().yArray),
                                  index = np.array(app.getDiscreteFunction().xArray)).T
#            print(valueFrame)
#            print(self.t[0])                          
        except Exception as e:
            print(e.stacktrace())
        try:
            return valueFrame[self.t[0]].values
        except Exception as e:
            print(e.stacktrace())
        
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

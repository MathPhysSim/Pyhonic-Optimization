#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 22:37:51 2018

@author: shirlaen
"""

import numpy as np
import pyjapc
import ParameterSetting as pc

import ListSelectorClass as lsclass


japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=False)
japc.setSelector("LEI.USER.NOMINAL")

# japc.rbacLogin()

parameterClass = pc.ParameterClass(japc)


ls = lsclass.ListSelector()
ls.setSelection(["ETL.GSBHN10/KICK"])

parameterClass.addParameters(ls.getSelectedItemsDict())
print("Current Value")
print(parameterClass.getValues())
setValue = parameterClass.getValues()
print(setValue)
print("Set Value")
parameterClass.setNewValues([.1])
print(parameterClass.getValues())
print("Set Value back")
parameterClass.setNewValues([0])
print(parameterClass.getValues())
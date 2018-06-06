#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 22:37:51 2018

@author: shirlaen
"""

import numpy as np
import pyjapc
import ParameterSetting as pc




japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=False)
japc.setSelector("LEI.USER.EARLY")
parameterClass = pc.ParameterClass(japc)


ls = lsclass.ListSelector()
ls.setSelection(["LEIRBEAM/coolerBump_CTRS20_H_1mrad"])
# japc.rbacLogin(loginDialog=True)
parameterClass.addParameters(ls.getSelectedItemsDict())
print("Current Value")
print(parameterClass.getValues())
setValue = parameterClass.getValues()
parameterClass.setNewValues(setValue)
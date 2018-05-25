#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:47:49 2018

@author: shirlaen
"""

import numpy as np


class ParameterClass():


    def __init__(self, japcIn):

        self.japc = japcIn
        self.x0 = self.getValues()

    def getValues(self):
       knob_bvn10 = self.japc.getParam("rmi://virtual_sps/logical.EI.BVN10/K",
                                       noPyConversion=True,
                                       timingSelectorOverride=
                                       "LEI.USER.EARLY").getValue()
       knob_bvn20 = self.japc.getParam("rmi://virtual_sps/logical.EI.BVN20/K",
                                       noPyConversion=True,
                                       timingSelectorOverride=
                                       "LEI.USER.EARLY").getValue()
       knob_bhn10 = self.japc.getParam("rmi://virtual_sps/logical.EI.BHN10/K",
                                       noPyConversion=True,
                                       timingSelectorOverride=
                                       "LEI.USER.EARLY").getValue()
       knob_bhn20 = self.japc.getParam(
       "rmi://virtual_sps/logical.ETL.BHN20-INJ/K",
       noPyConversion=True,
       timingSelectorOverride="LEI.USER.EARLY").getValue()
       return np.array([ knob_bhn10.double, knob_bhn20.double,
                        knob_bvn10.double, knob_bvn20.double])
    
    def setValues(self,x):
       x = np.array(x) 
       knob_bvn10 = self.japc.getParam(
       "rmi://virtual_sps/logical.EI.BVN10/K",
       noPyConversion=True, timingSelectorOverride=
       "LEI.USER.EARLY").getValue()
       knob_bvn10.double = x[2]
       knob_bvn20 = self.japc.getParam(
       "rmi://virtual_sps/logical.EI.BVN20/K",
       noPyConversion=True, timingSelectorOverride=
       "LEI.USER.EARLY").getValue()
       knob_bvn20.double = x[3]
       knob_bhn10 = self.japc.getParam(
       "rmi://virtual_sps/logical.EI.BHN10/K",
       noPyConversion=True, timingSelectorOverride=
       "LEI.USER.EARLY").getValue()
       knob_bhn10.double = x[0]
       knob_bhn20 = self.japc.getParam(
       "rmi://virtual_sps/logical.ETL.BHN20-INJ/K",
       noPyConversion=True, timingSelectorOverride=
       "LEI.USER.EARLY").getValue()
       knob_bhn20.double = x[1]
       self.japc.setParam("rmi://virtual_sps/logical.EI.BVN10/K",knob_bvn10)
       self.japc.setParam("rmi://virtual_sps/logical.EI.BVN20/K",knob_bvn20)
       self.japc.setParam("rmi://virtual_sps/logical.EI.BHN10/K",knob_bhn10)
       self.japc.setParam("rmi://virtual_sps/logical.ETL.BHN20-INJ/K",knob_bhn20)

       return None
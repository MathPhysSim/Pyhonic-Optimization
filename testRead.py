#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:03:14 2018

@author: shirlaen
"""
import pyjapc

japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=False)
japc.setSelector("LEI.USER.EARLY")

normVal = japc.getParam("ITL.BCT05/Acquisition")
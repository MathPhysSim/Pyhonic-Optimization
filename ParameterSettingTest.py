#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 22:37:51 2018

@author: shirlaen
"""

import numpy as np
import pyjapc
import ParameterSetting as pc




class ListSelector():

    parameterList = {"EI.BVN10/K":
                     {"name": "rmi://virtual_sps/logical.EI.BVN10/K",
                      "type": "scalar"},
                     "EI.BVN20/K":
                         {"name": "rmi://virtual_sps/logical.EI.BVN20/K",
                          "type": "scalar"},
                     "EI.BHN10/K":
                         {"name": "rmi://virtual_sps/logical.EI.BHN10/K",
                          "type": "scalar"},
                     "ETL.BHN20-INJ/K":
                         {"name": "rmi://virtual_sps/logical.ETL.BHN20-INJ/K",
                          "type": "scalar"},
                         "ITH.DHZ10/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DHZ10/K",
                              "type": "scalar"},
                         "ITH.DHZ11/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DHZ11/K",
                              "type": "scalar"},
                         "ITH.DHZ21/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DHZ21/K",
                              "type": "scalar"},
                         "ITE.BHN10/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN10/K",
                              "type": "scalar"},
                         "ITE.BHN20/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN20/K",
                              "type": "scalar"},
                         "ITE.BHN30/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN30/K",
                              "type": "scalar"},
                         "ITE.BHN40-IN-LEI/K":
                             {"name": "rmi://virtual_sps/logical.ITE.BHN40-IN-LEI/K",
                              "type": "scalar"},
                         "ETL.DHN10-INJ/K":
                             {"name": "rmi://virtual_sps/logical.ETL.DHN10-INJ/K",
                              "type": "scalar"},
                         "ITH.DVT10/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DVT10/K",
                              "type": "scalar"},
                         "ITH.DVT11/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DVT11/K",
                              "type": "scalar"},
                         "ITH.DVT21/K":
                             {"name": "rmi://virtual_sps/logical.ITH.DVT21/K",
                              "type": "scalar"},
                         "ETL.BVN10-INJ/K":
                             {"name": "rmi://virtual_sps/logical.ETL.BVN10-INJ/K",
                              "type": "scalar"},
                         "ETL.BVN20-INJ/K":
                         {"name": "rmi://virtual_sps/logical.ETL.BVN20-INJ/K",
                          "type": "scalar"},
                         "ETL.GSBHN10/KICK":
                             {"name": "rmi://virtual_leir/ETL.GSBHN10/KICK",
                              "type": "function", "time": [110, 660]}
                             }
    markedItems = {"EI.BVN10/K", "EI.BVN20/K", "EI.BHN10/K"}

    def getItems(self):
        return self.parameterList.keys()

    def getSelectedItemsNames(self):
        return [self.parameterList[key] for key in self.selectionList]

    def getSelectedItemsDict(self):
        return {key: self.parameterList[key] for key in self.selectionList}

    def __init__(self):
        self.selectionList = []

    def setSelection(self, selectedItems):
        self.selectionList = selectedItems



japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=False)
japc.setSelector("LEI.USER.EARLY")
parameterClass = pc.ParameterClass(japc)


ls = ListSelector()
ls.setSelection(["ETL.GSBHN10/KICK", "ETL.BVN20-INJ/K"])

parameterClass.addParameters(ls.getSelectedItemsDict())

parameterClass.setNewValues(parameterClass.getValues())
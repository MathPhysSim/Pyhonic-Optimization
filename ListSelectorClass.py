#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 21:30:16 2018

@author: shirlaen
"""

class ListSelector():

    parameterList = {
                    "EI.BVN10/K":
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
#                         "ITH.DHZ10/K":
#                             {"name": "rmi://virtual_sps/logical.ITH.DHZ10/K",
#                              "type": "scalar"},
#                         "ITH.DHZ11/K":
#                             {"name": "rmi://virtual_sps/logical.ITH.DHZ11/K",
#                              "type": "scalar"},
#                         "ITH.DHZ21/K":
#                             {"name": "rmi://virtual_sps/logical.ITH.DHZ21/K",
#                              "type": "scalar"},
#                         "ITE.BHN10/K":
#                             {"name": "rmi://virtual_sps/logical.ITE.BHN10/K",
#                              "type": "scalar"},
#                         "ITE.BHN20/K":
#                             {"name": "rmi://virtual_sps/logical.ITE.BHN20/K",
#                              "type": "scalar"},
#                         "ITE.BHN30/K":
#                             {"name": "rmi://virtual_sps/logical.ITE.BHN30/K",
#                              "type": "scalar"},
#                         "ITE.BHN40-IN-LEI/K":
#                             {"name": "rmi://virtual_sps/logical.ITE.BHN40-IN-LEI/K",
#                              "type": "scalar"},
#                         "ETL.DHN10-INJ/K":
#                             {"name": "rmi://virtual_sps/logical.ETL.DHN10-INJ/K",
#                              "type": "scalar"},
#                         "ITH.DVT10/K":
#                             {"name": "rmi://virtual_sps/logical.ITH.DVT10/K",
#                              "type": "scalar"},
#                         "ITH.DVT11/K":
#                             {"name": "rmi://virtual_sps/logical.ITH.DVT11/K",
#                              "type": "scalar"},
#                         "ITH.DVT21/K":
#                             {"name": "rmi://virtual_sps/logical.ITH.DVT21/K",
#                              "type": "scalar"},
#                         "ETL.BVN10-INJ/K":
#                             {"name": "rmi://virtual_sps/logical.ETL.BVN10-INJ/K",
#                              "type": "scalar"},
#                         "ETL.BVN20-INJ/K":
#                         {"name": "rmi://virtual_sps/logical.ETL.BVN20-INJ/K",
#                          "type": "scalar"},
                         "ETL.GSBHN10/KICK":
                             {"name": "rmi://virtual_leir/ETL.GSBHN10/KICK",
                             "type": "function", "time": [110, 660]},
                          "LEIRBEAM/injectionBump_CTRS10_H_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_H_1mm",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                          "LEIRBEAM/injectionBump_CTRS10_H_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_H_1mrad",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                          "LEIRBEAM/injectionBump_CTRS10_V_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_V_1mm",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                           "LEIRBEAM/injectionBump_CTRS10_V_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/injectionBump_CTRS10_V_1mrad",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                           "LEIRBEAM/coolerBump_CTRS20_H_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/coolerBump_CTRS20_H_1mm",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                            "LEIRBEAM/coolerBump_CTRS20_H_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/coolerBump_CTRS20_H_1mrad",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                            "LEIRBEAM/coolerBump_CTRS20_V_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/coolerBump_CTRS20_V_1mm",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                             "LEIRBEAM/coolerBump_CTRS20_V_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/coolerBump_CTRS20_V_1mrad",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                             "LEIRBEAM/extractionRegionSteering_CTRS40_H_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/extractionRegionSteering_CTRS40_H_1mm",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                             "LEIRBEAM/extractionRegionSteering_CTRS40_H_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/extractionRegionSteering_CTRS40_H_1mrad",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                             "LEIRBEAM/extractionRegionSteering_CTRS40_V_1mm":
                             {"name": "rmi://virtual_leir/LEIRBEAM/extractionRegionSteering_CTRS40_V_1mm",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]},
                             "LEIRBEAM/extractionRegionSteering_CTRS40_V_1mrad":
                             {"name": "rmi://virtual_leir/LEIRBEAM/extractionRegionSteering_CTRS40_V_1mrad",
                              "type": "functionSquare", "time": [200, 1850], "delta": 100., "range": [100,1950]}#,
#                              "EA.FGFREVCOR/Settings#amplitudes":
#                             {"name": "rmi://inca_leir/EA.FGFREVCOR/Settings#amplitudes",
#                             "type": "function", "time": [0, 60]}
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
    
    def setItemTime(self, key, values):
        self.parameterList[key]["time"] = values
        
        

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 13:37:28 2018

@author: shirlaen
"""

from scipy import optimize

import numpy as np

def fun(x):
    return (x[0]+x[1])/np.sin(x[1])

res = optimize.minimize(fun, np.array([0,3]), method='Nelder-Mead', options={
        'xatol':.001})
print(res.x)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:44:53 2018

@author: shirlaen
"""

from scipy import optimize
import numpy as np
import pandas as pd

def func_obj(x):
    return (x[1]**2+x[1]**2-x[0]**2)**2

x0 = [1,1,1]
res = optimize.fmin_powell(func_obj, x0)


def func_obj(x):
    return (x[0])**2

x0 = [1]
res1 = optimize.fmin_powell(func_obj, x0)
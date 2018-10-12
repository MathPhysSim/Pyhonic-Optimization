#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 18:36:40 2018

@author: shirlaen
"""

import pandas as pd
import os

path = os.path.dirname(os.path.realpath(__file__))
files = os.listdir(path)

files = [i for i in files if i.endswith('.csv')]

data = pd.read_csv(files[1], index_col=[0] )
print(data)
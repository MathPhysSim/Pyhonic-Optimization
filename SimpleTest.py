#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 12:54:55 2018

@author: shirlaen
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:24:16 2018

@author: shirlaen
"""

import pyjapc
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import minimize_scalar
from scipy import optimize

inj_intensity=[]
       
def myCallback(parameterName, newValue):
    getVal = abs(newValue["intensities"][395]) *(-1.)
    print('subscribtion')
    inj_intensity.append(getVal)
    print(inj_intensity)

japc = pyjapc.PyJapc(incaAcceleratorName="LEIR", noSet=False)
japc.setSelector("LEI.USER.MDNOM")
japc.subscribeParam( "ER.BCTDC/Acquisition", myCallback)  
japc.startSubscriptions() 


def func_obj(x):
   inj_intensity.clear()
   while(len(inj_intensity)<1.):
       print(inj_intensity)
       time.sleep(2)   
   intFinal =  np.mean(np.sort(np.array(inj_intensity)))  
   print ("new value", intFinal)

   return intFinal


x0 = np.array([-0.34344])
rranges = slice(x0-1e-3, x0+1e-3, 2.5e-4)
print('raw tuning..................................')
resbrute = optimize.brute(func_obj, (rranges,), finish=None)

japc.stopSubscriptions() 


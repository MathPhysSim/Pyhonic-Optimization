#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:19:22 2018

@author: shirlaen
"""
import random

zen = \
"What is the use of a book,\n without pictures or conversations?.\
Oh my ears and whiskers,\n how late it's getting!.\
Curiouser and curiouser!.\
I can't explain myself,\n I'm afraid, Sir,\n because I'm not myself you see.\
We're all mad here.\
Tut, tut, child!\n Everything's got a moral,\n if only you can find it.\
Take care of the sense,\n and the sounds will take care of themselves.\
Reeling and Writhing,\n of course, to begin with,\n and then the different\
 branches of arithmetic\n -- Ambition, Distraction, Uglification, and Derision."
 

zen = zen.split('.')
class Zen():
    def __init__(self):
        self.zen = zen        
    def get_text(self):
        return zen[random.randint(0,len(zen)-1)]
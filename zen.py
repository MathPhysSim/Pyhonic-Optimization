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
 branches of arithmetic\n -- Ambition, Distraction, Uglification, and Derision.\
 Well,\n I never heard it before,\n but it sounds uncommon nonsense.\
 Begin at the beginning and go on till you come to the end: then stop.\
 Sentence first -- verdict afterwards.\
A cat may look at a king.\n I've read that in some book,\n\
 but I don't remember where.\
 It would be so nice if something\n made sense for a change.\
 LEIR rules!"
 

zen = zen.split('.')
class Zen():
    def __init__(self):
        self.zen = zen        
    def get_text(self):
        return zen[random.randint(0,len(zen)-1)]
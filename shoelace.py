# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 15:25:46 2021

@author: lim38963
"""


import numpy as np
import math as m

p = np.linspace(0,2*np.pi,9)
#x = 1.2*np.cos(p)
#y = 1.2*np.sin(p)

x = [2,0,-2,0,2,0,-2,0,2,0,-2,0,2,0,-2,0]
y = [2,2,-2,-2,2,2,-2,-2,2,2,-2,-2,2,2,-2,-2]


def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))#/0.0

if __name__ == '__main__':
    res = PolyArea(x,y)
    print(res)
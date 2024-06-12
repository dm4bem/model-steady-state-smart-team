# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:25:48 2024

@author: roman
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from modélisationV6 import *
import dm4bem

### Calcul  steady-state using DAE###
T0 = 20 #température extérieure
Tin = 20 #température intérieure au début
Ti_sp=20
Φo = 200 # W/m2 average solar irradiation on the exterior wall
Φi = 100 # W/m2 surfacic power inside the building due to wall temperature
Qa = 100 # W Human activity in the bulding that brings power to the building
Φa = Φo
bss=np.zeros(43)
bss[[0,1,7,35,37,40]]=T0
bss[39]=Ti_sp
fss=np.zeros(33)
theta = np.linalg.inv(A.T @ np.diag(G) @ A) @ (A.T @ np.diag(G) @ bss + fss)
q = np.diag(G) @ (-A @ theta + bss)
print('Temperature without flux \n''pièce 0 : ', theta[0], ', pièce 1 : ',theta[1],', pièce 2 : ', theta[2])
fss[[3,8,10,16,30,32]]=Φo
fss[[7,17,19,14,20,22,23,25,26]]=Φi
fss[0]=Φa
theta = np.linalg.inv(A.T @ np.diag(G) @ A) @ (A.T @ np.diag(G) @ bss + fss)
q = np.diag(G) @ (-A @ theta + bss)
print('Temperature with flux \n''pièce 0 : ', theta[0], ', pièce 1 : ',theta[1],', pièce 2 : ', theta[2])



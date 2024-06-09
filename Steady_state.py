# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:25:48 2024

@author: roman
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from modélisationV5 import *
import dm4bem



### Calcul  steady-state###
theta = np.linalg.inv(A.T @ np.diag(G) @ A) @ (A.T @ np.diag(G) @ bss + fss)
q = np.diag(G) @ (-A @ theta + bss)
print('pièce 0 : ', theta[0], ', pièce 1 : ',theta[1],', pièce 2 : ', theta[2])

y = np.zeros(A.shape[1])
y[0:2] = 1

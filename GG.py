# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:25:48 2024

@author: roman
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dm4bem
###Data###

H = 3               # m hauteur des murs
L1= 10              # m longueur premier côté
L2= 8               # m longueur deuxième  côté
L3= 6               # m longueur coté du fond
S1 = L1*H           # m² surface 1 intermédiaire
S2 = L2*H           # m² surface 2 intermédiaire
S3 = L3*H           # m² surface 3 intermédiaire
Smur1 = 2*S1+2*S3   # m² surface du mur du bas
Svitre = 4          # m² surface d'une vitre
Smur2= S1+S2 -Svitre        # m² surface d'un des murs du haut
Smur3= S1             # m² surface du mur intérieur horizontale
Smur4= S2             # m² surface du mur intérieur verticale

T0 = 20 #température extérieure
Tin = 0 #température intérieure au début
ntheta= 33  #nombre de points de température
nbranches= 43 #nombre de branches
Qout = 5 #heat flow rate outside#
Qin = 2 #heat flow rate inside#

####
air = {'Density': 1.2,                      # kg/m³
       'Specific heat': 1000}               # J/(kg·K)

concrete = {'Conductivity': 1.400,          # W/(m·K)
            'Density': 2300.0,              # kg/m³
            'Specific heat': 880,           # J/(kg⋅K)
            'Width': 0.2}            # m²

insulation = {'Conductivity': 0.027,        # W/(m·K)
              'Density': 55.0,              # kg/m³
              'Specific heat': 1210,        # J/(kg⋅K)
              'Width': 0.08}          # m²

glass = {'Conductivity': 1.4,               # W/(m·K)
         'Density': 2500,                   # kg/m³
         'Specific heat': 1210,             # J/(kg⋅K)
         'Width': 0.04}                   # m²

layer = pd.DataFrame.from_dict({'Layer_out': concrete,
                               'Layer_in': insulation,
                               'Glass': glass},
                              orient='index')
# radiative properties
ε_wLW = 0.85    # long wave emmisivity: wall surface (concrete)
ε_gLW = 0.90    # long wave emmisivity: glass pyrex
α_wSW = 0.25    # short wave absortivity: white smooth surface
α_gSW = 0.38    # short wave absortivity: reflective blue glass
τ_gSW = 0.30    # short wave transmitance: reflective blue glass

σ = 5.67e-8     # W/(m²⋅K⁴) Stefan-Bolzmann constant
h = pd.DataFrame([{'in': 8., 'out': 25}], index=['h'])  # W/(m²⋅K)
wall_width_interior=insulation['Width']
wall_width_exterior=insulation['Width']+concrete['Width']

### Incidence matrix###

A = np.zeros([nbranches, ntheta])

A[6,0] = 1
A[13,0] = 1
A[18,0]=1
A[20,0] = -1
A[24,0] = -1
A[41,0] = 1

A[12,1] = 1
A[16,1] = -1
A[42,1]=1
A[27,1] = -1
A[21,1] = -1
A[18,1] = -1

A[28,2] = 1
A[24,2] = 1
A[29,2]=1
A[27,2] = 1
A[39,2] = -1
A[38,2] = 1
A[30,2] = 1

A[1,3] = 1
A[2,3] = -1

A[2,4] = 1
A[3,4] = -1

A[3,5] = 1
A[4,5] = -1

A[4,6] = 1
A[5,6] = -1

A[5,7] = 1
A[6,7] = -1

A[40,8] = 1
A[17,8] = -1

A[17,9] = 1
A[41,9] = -1

A[7,10] = 1
A[8,10] = -1

A[8,11] = 1
A[9,11] = -1

A[9,12] = 1
A[10,12] = -1

A[10,13] = 1
A[11,13] = -1

A[11,14] = 1
A[12,14] = -1

A[42,15] = -1
A[19,15] = 1

A[0,16] = 1
A[19,16] = -1

A[13,17] = -1
A[14,17] = 1

A[14,18] = -1
A[15,18] = 1

A[15,19] = -1
A[16,19] = 1

A[20,20] = 1
A[22,20] = -1

A[22,21] = 1
A[25,21] = -1

A[25,22] = 1
A[28,22] = -1

A[21,23] = 1
A[23,23] = -1

A[23,24] = 1
A[26,24] = -1

A[26,25] = 1
A[29,25] = -1

A[30,26] = -1
A[31,26] = 1

A[31,27] = -1
A[32,27] = 1

A[32,28] = -1
A[33,28] = 1

A[33,29] = -1
A[34,29] = 1

A[34,30] = -1
A[35,30] = 1

A[38,31] = -1
A[36,31] = 1

A[36,32] = -1
A[37,32] = 1
### Conductance matrix###

G_layer = layer['Conductivity'] / layer['Width'] #conductance par m²
pd.DataFrame(G_layer, columns=['Conductance'])
G_cd={'vitre':G_layer[2]*Svitre,
        'mur bas béton':Smur1*G_layer[0],
        'mur bas isolant':Smur1*G_layer[1],
        'mur haut isolant':Smur2*G_layer[1],
        'mur haut béton':Smur2*G_layer[0],
        'mur intérieur horizontal':Smur3*G_layer[0],
        'mur intérieur vertical':Smur4*G_layer[0]
}
pd.DataFrame.from_dict({'Conduction':G_cd})

G_conv={'vitre interieur':h['in']*Svitre,
        'vitre exterieur':h['out']*Svitre,
        'mur bas intérieur':Smur1*h['in'],
        'mur bas exterieur':Smur1*h['out'],
        'mur haut interieur':Smur2*h['out'],
        'mur haut exterieur':Smur2*h['in'],
        'mur intérieur horizontal':Smur3*h['in'],
        'mur intérieur vertical':Smur4*h['in']
}
pd.DataFrame.from_dict({'Conduction':G_conv})

C_layer = layer['Density'] * layer['Specific heat']  * layer['Width']
pd.DataFrame(C_layer, columns=['Capacity'])
C_thermal = {'vitre':C_layer[2]*Svitre,
        'mur bas béton':Smur1*C_layer[0],
        'mur bas isolant':Smur1*C_layer[1],
        'mur haut isolant':Smur2*C_layer[1],
        'mur haut béton':Smur2*C_layer[0],
        'mur intérieur horizontal':Smur3*C_layer[0],
        'mur intérieur vertical':Smur4*C_layer[0]
}

Va1 = (L1-wall_width_exterior)*(L2-wall_width_exterior)*H    # m³, volume d'air de la pièce du haut
Va2 = (2*L1-wall_width_exterior)*(L2-wall_width_exterior)*H           # m³, volume d'air de la pièce du haut
ACH1 = 1        # 1/h, changement d'air pièce du bas
ACH2 = 0.5      # 1/h, changement d'air pièce du haut
G_adv = {   'Advection bas': air['Density']*air['Specific heat']*ACH1*Va1/3600,
            'Advection haut': air['Density']*air['Specific heat']*ACH2*Va2/3600,
            'Advection entre haut':10
}
pd.DataFrame.from_dict({'Conduction':G_adv})

G = np.zeros(A.shape[0])

G[0]=G_conv['vitre exterieur']
G[1]=G_conv['mur haut exterieur']
G[2]=G_cd['mur haut béton']
G[3]=G_cd['mur haut béton']
G[4]=G_cd['mur haut isolant']
G[5]=G_cd['mur haut isolant']
G[6]=G_conv['mur haut interieur']
G[7]=G_conv['mur haut exterieur']
G[8]=G_cd['mur haut béton']
G[9]=G_cd['mur haut béton']
G[10]=G_cd['mur haut isolant']
G[11]=G_cd['mur haut isolant']
G[12]=G_conv['mur haut interieur']
G[13]=G_conv['mur intérieur vertical']
G[14]=G_cd['mur intérieur vertical']
G[15]=G_cd['mur intérieur vertical']
G[16]=G_conv['mur intérieur vertical']
G[17]=G_cd['vitre']
G[18]=G_conv['mur intérieur vertical']
G[19]=G_cd['vitre']
G[20]=G_conv['mur intérieur horizontal']
G[21]=G_conv['mur intérieur horizontal']
G[22]=G_cd['mur intérieur horizontal']
G[23]=G_cd['mur intérieur horizontal']
G[24]=G_adv['Advection haut']
G[25]=G_cd['mur intérieur horizontal']
G[26]=G_cd['mur intérieur horizontal']
G[27]=G_adv['Advection haut']
G[28]=G_conv['mur intérieur horizontal']
G[29]=G_conv['mur intérieur horizontal']
G[30]=G_conv['mur bas intérieur']
G[31]=G_cd['mur bas isolant']
G[32]=G_cd['mur bas isolant']
G[33]=G_cd['mur bas béton']
G[34]=G_cd['mur bas béton']
G[35]=G_conv['mur bas exterieur']
G[36]=G_adv['Advection bas']
G[37]=1 #Conv ext porte
G[38]=1 #Conv int porte
G[39]=1 #Ventilation
G[40]=G_conv['vitre exterieur']
G[41]=G_conv['vitre interieur']
G[42]=G_conv['vitre interieur']

### Vector of temperature sources ###

b = np.zeros(A.shape[0])

b[40]=T0
b[1]=T0
b[7]=T0
b[37]=T0
b[39]=T0

### Vector of heat flow rate sources (for steady-state) ###

f = np.zeros(A.shape[1])

f[8]= Qout
f[26]= Qin
f[30]= Qout
f[7]= Qin
f[3]= Qout
f[10]= Qout
f[14]= Qin
f[16]= Qout
f[32]= Qout
f[22]= Qin
f[20]= Qin
f[25]= Qin
f[23]= Qin
f[17]= Qin
f[19]= Qin

### Calcul  steady-state###
theta = np.linalg.inv(A.T @ np.diag(G) @ A) @ (A.T @ np.diag(G) @ b + f)
q = np.diag(G) @ (-A @ theta + b)
print('pièce 0 : ', theta[0], ', pièce 1 : ',theta[1],', pièce 2 : ', theta[2])

y = np.zeros(A.shape[1])
y[0:2] = 1


# ### Calcul step response ###
# # State-space
# C = np.zeros(A.shape[1])
# TC = {'A':A, 'C':C, 'G':G, 'b':b, 'f':f, 'y':y}
# [As, Bs, Cs, Ds, us] = dm4bem.tc2ss(A,G,b,f)

# λ = np.linalg.eig(As)[0]
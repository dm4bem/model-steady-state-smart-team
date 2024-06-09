import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


H = 3               # m hauteur des murs
hporte = 2.04       # m hauteur de la porte d entree
L1= 10              # m longueur horizontale
L2= 8               # m largeur  du haut
L3= 6               # m largeur du bas
Lporte = 0.73       # m largeur porte
S1 = L1*H          # m² surface 1 intermédiaire
S2 = L2*H           # m² surface 2 intermédiaire
S3 = L3*H           # m² surface 3 intermédiaire
Smur1 = 2*S1+2*S3   # m² surface du mur du bas
Svitre = 4          # m² surface d'une vitre
Sporte= hporte * Lporte    # m² surface de la porte d'entrée
Smur2= S1+S2 -Svitre        # m² surface d'un des murs du haut ou on enlèvre la surface des vitres
Smur3= S1             # m² surface du mur intérieur horizontale
Smur4= S2             # m² surface du mur intérieur verticale

T0 = 20 #température extérieure
Tin = 0 #température intérieure au début
Ti_sp=10
ntheta= 33  #nombre de points de température
nbranches= 43 #nombre de branches
Φo = 800 # W/m2 average solar irradiation on the exterior wall
Φi = 100 # W/m2 surfacic power inside the building due to wall temperature
Qa = 2*83 + 50 + 110 + 10 # W Human activity in the bulding that brings power to the building
Φa = Φo

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

wood = {'Conductivity': 0.15,               # W/(m·K)
         'Density': 2500,                   # kg/m³
         'Specific heat': 1210,             # J/(kg⋅K)
         'Width': 0.035}                   # m²

layer = pd.DataFrame.from_dict({'Layer_out': concrete,
                               'Layer_in': insulation,
                               'Glass': glass,
                               'Wood':wood},
                                orient='index')


# radiative properties
ε_wLW = 0.85    # long wave emmisivity: wall surface (concrete)
ε_gLW = 0.90    # long wave emmisivity: glass pyrex
α_wSW = 0.25    # short wave absortivity: white smooth surface
α_gSW = 0.38    # short wave absortivity: reflective blue glass
τ_gSW = 0.30    # short wave transmitance: reflective blue glass

σ = 5.67e-8     # W/(m²⋅K⁴) Stefan-Bolzmann constant
h=[8,25]

wall_width_interior=insulation['Width']
wall_width_exterior=insulation['Width']+concrete['Width']
pd.DataFrame([{'in': 8., 'out': 25}], index=['h'])  # W/(m²⋅K)
G_layer = layer['Conductivity'] / layer['Width'] #conductance par m²
pd.DataFrame(G_layer, columns=['Conductance'])



G_cd={'vitre':G_layer.iloc[2]*Svitre,
        'mur bas béton':Smur1*G_layer.iloc[0],
        'mur bas isolant':Smur1*G_layer.iloc[1],
        'mur haut isolant':Smur2*G_layer.iloc[1],
        'mur haut béton':Smur2*G_layer.iloc[0],
        'mur intérieur horizontal':Smur3*G_layer.iloc[0],
        'mur intérieur vertical':Smur4*G_layer.iloc[0],
        'porte':G_layer.iloc[3]*Sporte
}

pd.DataFrame.from_dict({'Conduction':G_cd})

### Conductance matrix###

G_layer = layer['Conductivity'] / layer['Width'] #conductance par m²
pd.DataFrame(G_layer, columns=['Conductance'])
G_cd={'vitre':G_layer.iloc[2]*Svitre,
        'mur bas béton':Smur1*G_layer.iloc[0],
        'mur bas isolant':Smur1*G_layer.iloc[1],
        'mur haut isolant':Smur2*G_layer.iloc[1],
        'mur haut béton':Smur2*G_layer.iloc[0],
        'mur intérieur horizontal':Smur3*G_layer.iloc[0],
        'mur intérieur vertical':Smur4*G_layer.iloc[0]
}
pd.DataFrame.from_dict({'Conduction':G_cd})


G_conv={'vitre interieur':h[0]*Svitre,
        'vitre exterieur':h[1]*Svitre,
        'mur bas intérieur':Smur1*h[0],
        'mur bas exterieur':Smur1*h[1],
        'mur haut interieur':Smur2*h[0],
        'mur haut exterieur':Smur2*h[1],
        'mur intérieur horizontal':Smur3*h[0],
        'mur intérieur vertical':Smur4*h[0],
        'porte intérieur' : Sporte * h[0],
        'porte exterieur' : Sporte * h[1],
}
pd.DataFrame.from_dict({'Conduction':G_conv})

C_layer = layer['Density'] * layer['Specific heat']  * layer['Width']
pd.DataFrame(C_layer, columns=['Capacity'])


C_layer = layer['Density'] * layer['Specific heat']  * layer['Width']
pd.DataFrame(C_layer, columns=['Capacity'])
C_thermal = {'vitre':C_layer.iloc[2]*Svitre,
        'mur bas béton':Smur1*C_layer.iloc[0],
        'mur bas isolant':Smur1*C_layer.iloc[1],
        'mur haut isolant':Smur2*C_layer.iloc[1],
        'mur haut béton':Smur2*C_layer.iloc[0],
        'mur intérieur horizontal':Smur3*C_layer.iloc[0],
        'mur intérieur vertical':Smur4*C_layer.iloc[0],
}
pd.DataFrame.from_dict({'Thermal capacity':C_thermal})

Va1 = (L1-wall_width_exterior)*(L2-wall_width_exterior)*H    # m³, volume d'air de la pièce du haut
Va2 = (2*L1-wall_width_exterior)*(L2-wall_width_exterior)*H           # m³, volume d'air de la pièce du haut
ACH1 = 1        # 1/h, changement d'air pièce du bas
ACH2 = 0.5      # 1/h, changement d'air pièce du haut
G_adv = {   'Advection bas': air['Density']*air['Specific heat']*ACH1*Va1/3600,
            'Advection haut': air['Density']*air['Specific heat']*ACH2*Va2/3600,
            'Advection entre haut':10
}
pd.DataFrame.from_dict({'Conduction':G_adv})


# temperature nodes
θ = ['θ0', 'θ1', 'θ2', 'θ3', 'θ4', 'θ5', 'θ6', 'θ7','θ8', 'θ9', 'θ10', 'θ11', 'θ12', 'θ13', 'θ14', 'θ15','θ16', 'θ17', 'θ18'
     ,'θ19', 'θ20', 'θ21', 'θ22', 'θ23', 'θ24', 'θ25', 'θ26','θ27', 'θ28', 'θ29', 'θ30', 'θ31', 'θ32']

# flow-rate branches
q = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11','q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18',
      'q19', 'q20', 'q21', 'q22', 'q23','q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30', 'q31', 'q32', 'q33', 'q34', 'q35','q36',
       'q37','q38', 'q39','q40' ,'q41', 'q42']


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
A[39,2] = 1
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

G = np.zeros(A.shape[0])

G[0]=G_conv['vitre exterieur']
G[1]=G_conv['mur haut exterieur']
G[2]=G_cd['mur haut béton']/2
G[3]=G_cd['mur haut béton']/2
G[4]=G_cd['mur haut isolant']/2
G[5]=G_cd['mur haut isolant']/2
G[6]=G_conv['mur haut interieur']
G[7]=G_conv['mur haut exterieur']
G[8]=G_cd['mur haut béton']/2
G[9]=G_cd['mur haut béton']/2
G[10]=G_cd['mur haut isolant']/2
G[11]=G_cd['mur haut isolant']/2
G[12]=G_conv['mur haut interieur']
G[13]=G_conv['mur intérieur vertical']
G[14]=G_cd['mur intérieur vertical']/2
G[15]=G_cd['mur intérieur vertical']/2
G[16]=G_conv['mur intérieur vertical']
G[17]=G_cd['vitre']
G[18]=G_conv['mur intérieur vertical']
G[19]=G_cd['vitre']
G[20]=G_conv['mur intérieur horizontal']
G[21]=G_conv['mur intérieur horizontal']
G[22]=G_cd['mur intérieur horizontal']/2
G[23]=G_cd['mur intérieur horizontal']/2
G[24]=G_adv['Advection haut']
G[25]=G_cd['mur intérieur horizontal']/2
G[26]=G_cd['mur intérieur horizontal']/2
G[27]=G_adv['Advection haut']
G[28]=G_conv['mur intérieur horizontal']
G[29]=G_conv['mur intérieur horizontal']
G[30]=G_conv['mur bas intérieur']
G[31]=G_cd['mur bas isolant']/2
G[32]=G_cd['mur bas isolant']/2
G[33]=G_cd['mur bas béton']/2
G[34]=G_cd['mur bas béton']/2
G[35]=G_conv['mur bas exterieur']
G[36]=G_adv['Advection bas']
G[37]=50 #Conv ext porte
G[38]=50 #Conv int porte
G[39]=1 #Ventilation
G[40]=G_conv['vitre exterieur']
G[41]=G_conv['vitre interieur']
G[42]=G_conv['vitre interieur']

### Vector of temperature sources ###




b = pd.Series(['T0','T0',0,0,0,0,0,'T0',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'T0',0,'T0',0,'Ti_sp','T0',0,0 ],
              index=q)

f = pd.Series([0, 0, 0, 'Φo', 0, 0,0,'Φi','Φo',0,'Φo',0,0,0,'Φi',0,'Φo','Φi',0,'Φi','Φi',0,'Φi','Φi',0,'Φi','Φi',0,0,0,'Φo',0,'Φo'],
              index=θ)

C = np.zeros(A.shape[1])
C[4]=C_thermal['mur haut béton']
C[6]=C_thermal['mur haut isolant']
C[11]=C_thermal['mur haut béton']
C[13]=C_thermal['mur haut isolant']
C[18]=C_thermal['mur intérieur vertical']
C[24]=C_thermal['mur intérieur horizontal']
C[21]=C_thermal['mur intérieur horizontal']
C[29]=C_thermal['mur bas béton']
C[27]=C_thermal['mur bas isolant']

# node of interest
y = np.zeros(A.shape[1])
y[0:2] = 1

bss=pd.Series([T0,T0,0,0,0,0,0,T0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,T0,0,T0,0,Ti_sp,T0,0,0 ])

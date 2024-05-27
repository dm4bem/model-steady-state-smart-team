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

G_cd={'vitre':G_layer[2]*Svitre,
        'mur bas béton':Smur1*G_layer[0],
        'mur bas isolant':Smur1*G_layer[1],
        'mur haut isolant':Smur2*G_layer[1],
        'mur haut béton':Smur2*G_layer[0],
        'mur intérieur horizontal':Smur3*G_layer[0],
        'mur intérieur vertical':Smur4*G_layer[0],
        'porte':G_layer[3]*Sporte
}

pd.DataFrame.from_dict({'Conduction':G_cd})

G_conv={'vitre interieur':h[0]*Svitre,
        'vitre exterieur':h[1]*Svitre,
        'mur bas intérieur':Smur1*h[0],
        'mur bas exterieur':Smur1*h[1],
        'mur haut interieur':Smur2*h[1],
        'mur haut exterieur':Smur2*h[0],
        'mur intérieur horizontal':Smur3*h[0],
        'mur intérieur vertical':Smur4*h[0],
        'porte intérieur' : Sporte * h[0],
        'porte exterieur' : Sporte * h[1]
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

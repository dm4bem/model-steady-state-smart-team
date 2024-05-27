import numpy as np
import dm4bem
import pandas as pd
import matplotlib as plt
from modélisationV5 import*
from GG import*
#%%
#INPUTS

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


# # State-space
# temperature nodes
theta_list=[f"theta_{i}" for i in range(ntheta)]
q_list=[f"q_{i}" for i in range(nbranches)]
# flow-rate branches

#print(help(dm4bem.tc2ss))
Adf = pd.DataFrame(A, index=q_list, columns=theta_list)
Cdf= pd.Series(C, index=theta_list)
Gdf = pd.Series(G, index=q_list)
bdf = pd.Series(b, index=q_list)
fdf = pd.Series(f, index=theta_list)
ydf= pd.Series(y, index=theta_list)

TC = {'A':Adf, 'C':Cdf, 'G':Gdf, 'b':bdf, 'f':fdf, 'y':ydf}
[As, Bs, Cs, Ds, us] = dm4bem.tc2ss(TC)


Qa=0 # verif si c'est pas nul
Qin = 50
Qout = 50


         # vector of nonzero elements of vector f : [f0, f3, f7, f8, f10, f14, f16, f17, f19, f20, f22, f23, f25, f26, f30, f32]
#%%
lamda = np.linalg.eig(As)[0] # eigenvalues
dtmax = 2*min(-1/lamda)
dt = dm4bem.round_time(dtmax)

t_settle=4*max(-1/lamda)
duration=np.ceil(t_settle/3600)*3600
n = int(np.floor(duration / dt))    # number of time steps
To = 15 * np.ones(n)        # outdoor temperature
Ti_sp = 19 * np.ones(n)
bT = np.array([To, To, To, To, To, To, Ti_sp]) # vector of the nonzero elements of vector b : temperatures for the conductances 0, 1, 7, 35, 37, 39 and 40.

fQ = np.array([Qa, Qout, Qin, Qout, Qout, Qin, Qout, Qin, Qin, Qin, Qin, Qin, Qin, Qin, Qout, Qout])




uss = np.hstack([bT, fQ])           # input vector for state space
print(f'us = {us}')



# DateTimeIndex starting at "00:00:00" with a time step of dt
time = pd.date_range(start="2000-01-01 00:00:00",
                           periods=n, freq=f"{int(dt)}S")


phi0=0





f0 = Qa * np.ones(n)       # auxiliary heat gains
f3 = Qout * np.ones(n)      # solar radiation absorbed by the outdoor part of the glasses and the walls
f7 = Qin * np.ones(n)       # solar radiation absorbed by the outdoor part of the glasses and the walls
Φa=Qa=Φi=Φo=0*np.ones(n)


data = {'To': To, 'Ti_sp': Ti_sp, 'Φo': Φo, 'Φi': Φi, 'Qa': Qa, 'Φa': Φa}
input_data_set = pd.DataFrame(data, index=time)

# inputs in time from input_data_set
u = dm4bem.inputs_in_time(us, input_data_set)

# Initial conditions
θ_exp = pd.DataFrame(index=u.index)     # empty df with index for explicit Euler
θ_imp = pd.DataFrame(index=u.index)     # empty df with index for implicit Euler

θ0 = 0.0                    # initial temperatures
θ_exp[As.columns] = θ0      # fill θ for Euler explicit with initial values θ0
θ_imp[As.columns] = θ0      # fill θ for Euler implicit with initial values θ0

I = np.eye(As.shape[0])     # identity matrix
for k in range(u.shape[0] - 1):
    θ_exp.iloc[k + 1] = (I + dt * As) \
        @ θ_exp.iloc[k] + dt * Bs @ u.iloc[k]
    θ_imp.iloc[k + 1] = np.linalg.inv(I - dt * As) \
        @ (θ_imp.iloc[k] + dt * Bs @ u.iloc[k])

# outputs
y_exp = (Cs @ θ_exp.T + Ds @  u.T).T
y_imp = (Cs @ θ_imp.T + Ds @  u.T).T

# plot results
y = pd.concat([y_exp, y_imp], axis=1, keys=['Explicit', 'Implicit'])
# Flatten the two-level column labels into a single level
y.columns = y.columns.get_level_values(0)

ax = y.plot()
ax.set_xlabel('Time')
ax.set_ylabel('Indoor temperature, $\\theta_i$ / °C')
ax.set_title(f'Time step: $dt$ = {dt:.0f} s; $dt_{{max}}$ = {dtmax:.0f} s')
plt.show()
#%% Imports 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dm4bem import read_epw, sol_rad_tilt_surf

#%% Read weather data

# Modify the following path before running according to where the file has been downloaded.
filename = 'FRA_AR_Grenoble.Alpes.Isere.AP.074860_TMYx.2007-2021.epw' 
[data, meta] = read_epw(filename, coerce_year=None)
#data  #print the table with all the entries

# Extract the month and year from the DataFrame index with the format 'MM-YYYY'
month_year = data.index.strftime('%m-%Y')

# Create a set of unique month-year combinations
unique_month_years = sorted(set(month_year))

# Create a DataFrame from the unique month-year combinations
pd.DataFrame(unique_month_years, columns=['Month-Year'])

# select columns of interest
weather_data = data[["temp_air", "dir_n_rad", "dif_h_rad"]]

# replace year with 2000 in the index 
weather_data.index = weather_data.index.map(
    lambda t: t.replace(year=2020))

#%% Calculation of solar radiation on a tilted surface

# Parameters
# =============================================================================
# β slope between 0 and 180° (0 Horiz,upward / 90 Verti / 180 Horiz,downward)
# γ azimuth between -180 and 180° (0 South / Westward >0 / Eastward <0)
# ϕ latitude between -90 and 90 (northward >0 / Southward <0)
# =============================================================================

albedo=0.2
#Walls
WallN={'slope': 90, 'azimuth': 180, 'latitude': 45}
WallE={'slope': 90, 'azimuth': -90, 'latitude': 45}
WallW={'slope': 90, 'azimuth': 90, 'latitude': 45}
WallS={'slope': 90, 'azimuth': 0, 'latitude': 45}


β = 90 # 90° is vertical; > 90° downward
γ = 0 # 0° South, positive westward
ϕ = 45 # °, North Pole 90° positive

# Transform degrees in radians
β = β * np.pi / 180
γ = γ * np.pi / 180
ϕ = ϕ * np.pi / 180

n = weather_data.index.dayofyear

# Direct radiation
declination_angle = 23.45 * np.sin(360 * (284 + n) / 365 * np.pi / 180)
δ = declination_angle * np.pi / 180

hour = weather_data.index.hour
minute = weather_data.index.minute + 60
hour_angle = 15 * ((hour + minute / 60) - 12)   # deg
ω = hour_angle * np.pi / 180    # rad

theta = np.sin(δ) * np.sin(ϕ) * np.cos(β) - np.sin(δ) * np.cos(ϕ) * np.sin(β) * np.cos(γ) + np.cos(δ) * np.cos(ϕ) * np.cos(β) * np.cos(ω) + np.cos(δ) * np.sin(ϕ) * np.sin(β) * np.cos(γ) * np.cos(ω) + np.cos(δ) * np.sin(β) * np.sin(γ) * np.sin(ω)
theta = np.array(np.arccos(theta))
theta = np.minimum(theta, np.pi / 2)

dir_rad = weather_data["dir_n_rad"] * np.cos(theta)
dir_rad[dir_rad < 0] = 0

# Diffuse radiation
dif_rad = weather_data["dif_h_rad"] * (1 + np.cos(β)) / 2

#Reflected radiation
gamma = np.cos(δ) * np.cos(ϕ) * np.cos(ω) + np.sin(δ) * np.sin(ϕ)

gamma = np.array(np.arcsin(gamma))
gamma[gamma < 1e-5] = 1e-5

dir_h_rad = weather_data["dir_n_rad"] * np.sin(gamma)

ref_rad = (dir_h_rad + weather_data["dif_h_rad"]) * albedo * (1 - np.cos(β) / 2)
#%%

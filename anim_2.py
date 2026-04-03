import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as anm
import pandas as pd 

fig,ax = plt.subplots(figsize=(6,6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
df_U = pd.read_csv("Uranus_s1.csv", sep = ';')
df_T = pd.read_csv("Terre.csv",sep = ';')

print(df_U['phi* (deg)'])

phi = df_U['phi* (deg)'][0]

print(phi)
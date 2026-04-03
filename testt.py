import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as anm
import pandas as pd 

# Initialisation des angles
theta_U = 0 
theta_T = 0
theta_S = 0

# Figure et axes
fig, ax = plt.subplots(figsize=(6,6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Lecture des fichiers CSV
df_U = pd.read_csv("Mars_s1.csv", sep=';')
df_T = pd.read_csv("Terre.csv", sep=';')

# Conversion des colonnes en numériques
df_U['X mars'] = pd.to_numeric(df_U['X mars'], errors='coerce')
df_U['Y mars'] = pd.to_numeric(df_U['Y mars'], errors='coerce')
df_U['X trans mars'] = pd.to_numeric(df_U['X trans mars'], errors='coerce')[:180]
df_U['Y trans mars'] = pd.to_numeric(df_U['Y trans mars'], errors='coerce')[:180]

df_T['X terre'] = pd.to_numeric(df_T['X terre'], errors='coerce')
df_T['Y terre'] = pd.to_numeric(df_T['Y terre'], errors='coerce')

# Paramètres angulaires
phi = int(df_U['phi* (deg)'][0])
omega = 1.05825E-07 *(180/np.pi) *3600*24        # Mars (deg/jour)
omega_terre  = 1.99098E-07 *(180/np.pi) *3600*24 # Terre (deg/jour)

# Trajectoire satellite
n_points_sat = len(df_U['X trans mars'])
n_frames = 258
theta_S_max = np.pi                 # angle final à atteindre
omega_S = theta_S_max / n_frames    # incrément par frame

# Limites des axes
ax.set_xlim(df_U['X mars'].min()+df_U['X mars'].min()/8, df_U['X mars'].max()+df_U['X mars'].max()/8)
ax.set_ylim(df_U['Y mars'].min()+df_U['X mars'].min()/8, df_U['Y mars'].max()+df_U['X mars'].max()/8)
ax.set_aspect('equal')
plt.tight_layout()

# Tracés des orbites
ax.plot(df_T['X terre'], df_T['Y terre'], '-', linewidth=1, c='lightseagreen')
ax.plot(df_U['X mars'], df_U['Y mars'], '-', linewidth=1, c='orange')
ax.scatter(0,0,c='y')  # Soleil

# Points animés
point, = ax.plot([], [], 'o', label="position Mars", c='orange')
point_T, = ax.plot([], [], 'o', label="position Terre", c='lightseagreen')
point_S, = ax.plot([], [], 'o', label="position satellite", c='gold')
line, = ax.plot([], [], '--', linewidth=1, c='gold')

# Initialisation de l'angle de Mars
theta_U += phi

# Fonction d'animation
def animate(i):
    global theta_S, theta_T, theta_U
    
    # Mise à jour des angles des planètes
    theta_U += omega
    theta_T += omega_terre
    
    # Mise à jour de l'angle du satellite, limité à θ_max
    theta_S = min(theta_S + omega_S, theta_S_max)
    
    # Calcul de l'index correspondant sur la trajectoire du satellite
    idx = int((theta_S / theta_S_max) * (n_points_sat - 1))
    
    # Mise à jour des positions
    point_T.set_data([df_T['X terre'][int(theta_T%360)]], [df_T['Y terre'][int(theta_T%360)]])
    point.set_data([df_U['X mars'][int(theta_U%360)]], [df_U['Y mars'][int(theta_U%360)]])
    point_S.set_data([df_U['X trans mars'][idx]], [df_U['Y trans mars'][idx]])
    line.set_data([df_U['X trans mars'][:idx]], [df_U['Y trans mars'][:idx]])
    
    return point, point_T, point_S, line

# Animation
ani = anm.FuncAnimation(fig, animate, repeat=False, frames=n_frames, interval=10)
ax.grid(c='w')
ax.legend()
plt.show()

# Sauvegarde en GIF
writer = anm.PillowWriter(fps=50, metadata=dict(artist='Me'), bitrate=1800)
ani.save('scatter.gif', writer=writer)
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as anm
import pandas as pd 

# Lecture des données
df_U = pd.read_csv("Uranus_s1.csv", sep=';')

# Conversion en numérique
df_U['X Uranus'] = pd.to_numeric(df_U['X Uranus'], errors='coerce')
df_U['Y Uranus'] = pd.to_numeric(df_U['Y Uranus'], errors='coerce')

# Supprimer les lignes avec NaN (important pour que la ligne de l'orbite ne soit pas coupée)
df_U = df_U.dropna(subset=['X Uranus','Y Uranus'])

# Figure
fig, ax = plt.subplots(figsize=(6,6))

# Calcul du centre et des marges pour que tout soit visible
cx = (df_U['X Uranus'].max() + df_U['X Uranus'].min()) / 2
cy = (df_U['Y Uranus'].max() + df_U['Y Uranus'].min()) / 2
width = df_U['X Uranus'].max() - df_U['X Uranus'].min()
height = df_U['Y Uranus'].max() - df_U['Y Uranus'].min()
margin = 0.05 * max(width, height)

ax.set_xlim(cx - width/2 - margin, cx + width/2 + margin)
ax.set_ylim(cy - height/2 - margin, cy + height/2 + margin)

# Aspect égal pour que le cercle ne soit pas déformé
ax.set_aspect('equal')

# Orbite
ax.plot(df_U['X Uranus'], df_U['Y Uranus'], '-', linewidth=2, color='blue', label="orbite Uranus")

# Point animé
point, = ax.plot([], [], 'o', markersize=6, color='red', label="position Uranus")

# Animation
def animate(i):
    point.set_data(df_U['X Uranus'].iloc[i], df_U['Y Uranus'].iloc[i])
    return point,

ani = anm.FuncAnimation(fig, animate, repeat=True, frames=len(df_U), interval=50)

ax.legend()
plt.tight_layout()
plt.show()
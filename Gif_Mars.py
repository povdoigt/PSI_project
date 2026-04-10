import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as anm
import pandas as pd 


theta_U = 0 
theta_T = 0
theta_S = 0
fig,ax = plt.subplots(figsize=(6,6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
df_U = pd.read_csv("Mars_s1.csv", sep = ';')
df_T = pd.read_csv("Terre.csv",sep = ';')

df_U['X mars'] = pd.to_numeric(df_U['X mars'], errors='coerce')
df_U['Y mars'] = pd.to_numeric(df_U['Y mars'], errors='coerce')

df_T['X terre'] = pd.to_numeric(df_T['X terre'], errors='coerce')
df_T['Y terre'] = pd.to_numeric(df_T['Y terre'], errors='coerce')

df_U['X trans mars'] = pd.to_numeric(df_U['X trans mars'], errors='coerce')[:180]
df_U['Y trans mars'] = pd.to_numeric(df_U['Y trans mars'], errors='coerce')[:180]

phi = int(df_U['phi* (deg)'][0])
omega = 1.05825E-07 *(180/np.pi) *3600*24 #omega en degrés par jours 
omega_terre  = 1.99098E-07 *(180/np.pi) *3600*24  #omega_terre en degrés par jours 
omega_S = 180/258.9151484 # omega du satélite en degrés par jours 




print(df_U['X mars'])
print(df_U['Y mars'])

print(df_U['X mars'].min(), df_U['X mars'].max())
print(df_U['Y mars'].min(), df_U['Y mars'].max())

ax.set_xlim(df_U['X mars'].min()+df_U['X mars'].min()/8, df_U['X mars'].max()+df_U['X mars'].max()/8)
ax.set_ylim(df_U['Y mars'].min()+df_U['X mars'].min()/8, df_U['Y mars'].max()+df_U['X mars'].max()/8)



ax.set_aspect('equal')
plt.tight_layout()

ax.plot(df_T['X terre'],df_T['Y terre'],'-',linewidth = 1, c='lightseagreen')
ax.plot(df_U['X mars'],df_U['Y mars'],'-',linewidth = 1,c='orange')
ax.scatter(0,0,c='y')


# Point

point, = ax.plot([],[],'o', label = "position mars",c = 'orange')
point_T, = ax.plot([],[],'o', label = "position Terre",c = 'lightseagreen')
line, = ax.plot([],[],'--',linewidth = 1, c='gold')
point_S, = ax.plot([],[],'o', label = "position satellite",c = 'gold')

theta_U += phi
max_idx = df_U['X trans mars'].dropna().shape[0]

def animate(i):
    global theta_S, theta_T, theta_U
    theta_U += omega
    theta_T += omega_terre
    theta_S += omega_S

    idx = int(theta_S / 180 * max_idx)
    idx = min(idx, max_idx - 1)

    point_T.set_data([df_T['X terre'][int(theta_T % 360)]], [df_T['Y terre'][int(theta_T % 360)]])
    point.set_data([df_U['X mars'][int(theta_U % 360)]], [df_U['Y mars'][int(theta_U % 360)]])
    point_S.set_data([df_U['X trans mars'][idx]], [df_U['Y trans mars'][idx]])
    line.set_data(df_U['X trans mars'][:idx + 1], df_U['Y trans mars'][:idx + 1])

    return point, point_T, point_S, line

ani = anm.FuncAnimation(fig, animate, repeat=False, frames=258, interval=10)
ax.legend()
plt.show()

# Réinitialisation des angles avant sauvegarde
theta_U = phi
theta_T = 0
theta_S = 0

writer = anm.PillowWriter(fps=50, metadata=dict(artist='Me'), bitrate=1800)
ani.save('scatter.gif', writer=writer)


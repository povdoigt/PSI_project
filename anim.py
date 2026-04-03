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
df_U = pd.read_csv("Uranus_s1.csv", sep = ';')
df_T = pd.read_csv("Terre.csv",sep = ';')

df_U['X Uranus'] = pd.to_numeric(df_U['X Uranus'], errors='coerce')
df_U['Y Uranus'] = pd.to_numeric(df_U['Y Uranus'], errors='coerce')

df_T['X terre'] = pd.to_numeric(df_T['X terre'], errors='coerce')
df_T['Y terre'] = pd.to_numeric(df_T['Y terre'], errors='coerce')

df_U['X trans Uranus'] = pd.to_numeric(df_U['X trans Uranus'], errors='coerce')[:180]
df_U['Y trans Uranus'] = pd.to_numeric(df_U['Y trans Uranus'], errors='coerce')[:180]

phi = int(df_U['phi* (deg)'][0])
omega = 2.36323E-09 *(180/np.pi) *3600*24 #omega en degrés par jours 
omega_terre  = 1.99098E-07 *(180/np.pi) *3600*24  #omega_terre en degrés par jours 
omega_S = 180/5869.900276 # omega du satélite en degrés par jours 




print(df_U['X Uranus'])
print(df_U['Y Uranus'])

print(df_U['X Uranus'].min(), df_U['X Uranus'].max())
print(df_U['Y Uranus'].min(), df_U['Y Uranus'].max())

ax.set_xlim(df_U['X Uranus'].min()+df_U['X Uranus'].min()/8, df_U['X Uranus'].max()+df_U['X Uranus'].max()/8)
ax.set_ylim(df_U['Y Uranus'].min()+df_U['X Uranus'].min()/8, df_U['Y Uranus'].max()+df_U['X Uranus'].max()/8)



ax.set_aspect('equal')
plt.tight_layout()

ax.plot(df_T['X terre'],df_T['Y terre'],'-',linewidth = 1, c='lightseagreen')
ax.plot(df_U['X Uranus'],df_U['Y Uranus'],'-',linewidth = 1,c='orange')
ax.scatter(0,0,c='y')


# Point

point, = ax.plot([],[],'o', label = "position Uranus",c = 'orange')
point_T, = ax.plot([],[],'o', label = "position Terre",c = 'lightseagreen')
line, = ax.plot([],[],'--',linewidth = 1, c='gold')
point_S, = ax.plot([],[],'o', label = "position satélite",c = 'gold')

theta_U += phi
def animate(i):
    global theta_S,theta_T,theta_U
    theta_U += omega
    theta_T += omega_terre
    theta_S += omega_S 



    point_T.set_data([df_T['X terre'][int(theta_T)% 360]],[df_T['Y terre'][int(theta_T)% 360]])

    point.set_data([df_U['X Uranus'][int(theta_U)]],[df_U['Y Uranus'][int(theta_U)w])

    point_S.set_data([df_U['X trans Uranus'][theta_S% 360]],[df_U['Y trans Uranus'][theta_S% 360]])
    line.set_data([df_U['X trans Uranus'][:theta_S% 360]],[df_U['Y trans Uranus'][:theta_S% 360]])
    
    return point,point_T,point_S,line

ani = anm.FuncAnimation(fig, animate, repeat=True, frames=5869, interval=1)
ax.grid(c = 'w')
ax.legend()
plt.show()

writer = anm.PillowWriter(fps=30, metadata=dict(artist='Me'),bitrate=1800)
ani.save('scatter.gif', writer=writer)


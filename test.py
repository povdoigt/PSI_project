import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as anm
import pandas as pd 

fig,ax = plt.subplots(figsize=(6,6))
df_U = pd.read_csv("Uranus_s1.csv", sep = ';')

print(df_U['X Uranus'].min(), df_U['X Uranus'].max())
print(df_U['Y Uranus'].min(), df_U['Y Uranus'].max())
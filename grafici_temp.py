import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from converti import converti

file = "misure/Temperatura/1_1.txt"
df = converti(file)

df.plot(x="Tempo(s)", y="Temperatura(C)", linestyle="None", marker=".")
plt.show() 

# Ripulisco i dati 
dfmod = df.drop(df[(df["Tempo(s)"] < 5)].index)
dfmod.plot(x="Tempo(s)", y="Temperatura(C)", linestyle="None", marker=".")
plt.show() 


t0 = dfmod["Tempo(s)"].to_numpy()[0]
T0 = dfmod["Temperatura(C)"] .to_numpy()[0]
print(T0)

time = dfmod["Tempo(s)"].to_numpy()-t0
temp = dfmod["Temperatura(C)"] .to_numpy()

#incertezze sulle temperature
fluttuazione = converti("misure/fluttuazione_temp.txt").std(ddof=1)['Temperatura(C)']
print(fluttuazione)

dtemp = np.sqrt(0.05**2 + fluttuazione**2)
t_error = np.repeat(dtemp, len(temp)) 
print(dtemp)

plt.errorbar(time, temp, yerr=t_error, linestyle="None", marker=".", ecolor="r")
plt.xlabel("Time [s]")
plt.ylabel("Temperature [C]")
plt.show()
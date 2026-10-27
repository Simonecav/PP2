import matplotlib.pyplot as plt
import numpy as np
from converti import df

df.plot(x="Tempo(s)", y="Temperatura(C)", linestyle="None", marker=".")
plt.show() 

# Ripulisco i dati 
dfmod = df.drop( df[ (df["Tempo(s)"] <10) | (df["Temperatura(C)"] > 30) ].index )
dfmod.plot(x="Tempo(s)", y="Temperatura(C)", linestyle="None", marker=".")
plt.show() 


t0 = dfmod["Tempo(s)"].to_numpy()[0]
T0 = dfmod["Temperatura(C)"] .to_numpy()[0]
print(T0)

time = dfmod["Tempo(s)"].to_numpy()-t0
temp = dfmod["Temperatura(C)"] .to_numpy()

dtemp = np.repeat(0.2, len(temp)) #incertezze sulle temperature

plt.errorbar(time, temp, yerr=dtemp, linestyle="None", marker=".", ecolor="r")
plt.xlabel("Time [s]")
plt.ylabel("Temperature [C]")
plt.show()
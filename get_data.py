import numpy as np
from converti import converti

df = converti("misure/Temperatura/1_2.txt")

# Ripulisco i dati 
dfmod = df.drop(df[(df["Tempo(s)"] < 15) | (df["Tempo(s)"] > 55)].index)

t0 = dfmod["Tempo(s)"].to_numpy()[0]
T0 = dfmod["Temperatura(C)"] .to_numpy()[0]

time = dfmod["Tempo(s)"].to_numpy()-t0
temp = dfmod["Temperatura(C)"].to_numpy()

#incertezze sulle temperature
fluttuazione = converti("misure/fluttuazione_temp.txt").std(ddof=1)['Temperatura(C)']
print(fluttuazione)

dtemp = np.sqrt(0.05**2 + fluttuazione**2)
temp_error = np.repeat(dtemp, len(temp)) 
print(dtemp)

T_bar = df[-30:]["Temperatura(C)"].mean() # Prendo la media degli ultimi 30 valori come valore asintotico
T_0 = 54.4
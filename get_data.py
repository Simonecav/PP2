import numpy as np
from matplotlib.pyplot import show
from converti import converti

df = converti("misure/Temperatura/4_3.txt")
df.plot(x="Tempo(s)", y="Temperatura(C)")
show()

# inf_lim = 12.5
# inf_lim = 5.5
# inf_lim = 5
inf_lim = 4.25


# Ripulisco i dati 
dfmod = df.drop(df[(df["Tempo(s)"] < inf_lim)].index) # tolgo i primi 15 secondi (monnezza)

t0 = dfmod["Tempo(s)"].to_numpy()[0]
T0 = dfmod["Temperatura(C)"] .to_numpy()[0]

dfmod_exp = dfmod.drop(dfmod[(dfmod["Tempo(s)"] > inf_lim+40)].index) # 40 secondi
time_exp = dfmod_exp["Tempo(s)"].to_numpy()-t0
temp_exp = dfmod_exp["Temperatura(C)"].to_numpy()

fluttuazione = converti("misure/fluttuazione_temp.txt").std(ddof=1)['Temperatura(C)']
dtemp = np.sqrt(0.05**2 + fluttuazione**2)

#incertezze sulle temperature per il fit esponenziale
temp_error_exp = np.repeat(dtemp, len(temp_exp)) 

# seleziono i dati per il fit lineare
dfmod_linear = dfmod.drop(dfmod[(dfmod["Tempo(s)"] > inf_lim+5)].index) # 5 secondi (pochi)
time_linear = dfmod_linear["Tempo(s)"].to_numpy()-t0
temp_linear = dfmod_linear["Temperatura(C)"].to_numpy()
temp_error_linear = np.repeat(dtemp, len(temp_linear)) 


# Prendo la media degli ultimi 30 valori come valore asintotico T barra
T_bar = df[-30:]["Temperatura(C)"].mean()
T_0 = 54.4
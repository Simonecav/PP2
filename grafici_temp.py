import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from converti import converti
from mylib import LinearFit, ExpFit

file = "misure/Temperatura/1_2.txt"
df = converti(file)

# Ripulisco i dati 
dfmod = df.drop(df[(df["Tempo(s)"] < 15) | (df["Tempo(s)"] > 20)].index)


t0 = dfmod["Tempo(s)"].to_numpy()[0]
T0 = dfmod["Temperatura(C)"] .to_numpy()[0]
print(T0)

time = dfmod["Tempo(s)"].to_numpy()-t0
temp = dfmod["Temperatura(C)"] .to_numpy()

#incertezze sulle temperature
fluttuazione = converti("misure/fluttuazione_temp.txt").std(ddof=1)['Temperatura(C)']
print(fluttuazione)

dtemp = np.sqrt(0.05**2 + fluttuazione**2)
temp_error = np.repeat(dtemp, len(temp)) 
print(dtemp)

T_bar = df.iloc[-1]["Temperatura(C)"] # Prendo l'ultimo elemento della temperatura come valore di asintoto
print(T_bar)
T_0 = 54.4

# linearizzo dati e incertezze (err_ln(T) = (1/T)*err_T)
df = pd.DataFrame({
    "t": time,
    # "T - T_bar": temp - T_bar,
    # "dT": temp_error,
    "ln(T - T_bar)": np.log(temp - T_bar - 0.10035342),
    "dT": (1/(temp - T_bar))*temp_error,
})

# fit = ExpFit(df, "t", "T - T_bar", "dT")

fit = LinearFit(df, "t", "ln(T - T_bar)", "dT")
fig, ax = plt.subplots(1)
fit.graph(ax, markersize=2, labels=("$t$ [s]", r"$T - \bar{T}$ [°C]"))
ax.legend()
plt.show()

print(fit.get_chi2().pvalue)

# p = fit.p
# print(p)

# def f(x, a, b, c, d):   
#     return [a*np.exp(b-c*xi)+d for xi in x]

# temp_mod = f(time, p[0], p[1], p[2], p[3])
# plt.plot(time, np.emath.log(temp_mod - p[3]))
# plt.show()
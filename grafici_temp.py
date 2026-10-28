import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from converti import converti
from linearfit import LinearFit

file = "misure/Temperatura/1_2.txt"
df = converti(file)

df.plot(x="Tempo(s)", y="Temperatura(C)", linestyle="None", marker=".")
plt.show() 

# Ripulisco i dati 
dfmod = df.drop(df[(df["Tempo(s)"] < 15)].index)


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

T_bar = 25
T_0 = 54.4

# linearizzo dati e incertezze (err_ln(T) = (1/T)*err_T)
df = pd.DataFrame({
    "t": time,
    "ln(T - T_bar)": temp - T_bar,
    "dT": temp_error,
    # "ln(T - T_bar)": np.emath.log(temp - T_bar),
    # "dT": (1/(temp - T_bar))*temp_error,
})

fit = LinearFit(df, "t", "ln(T - T_bar)", "dT")

fig, ax = plt.subplots(1)
fit.graph(ax, markersize=2, labels=("$t$ [s]", r"$T - \bar{T}$ [°C]"))
ax.legend()
plt.show()

print(fit.get_chi2().pvalue)

# plt.errorbar(time, np.log(temp - T_bar), yerr=(1/temp)*temp_error, linestyle="None", marker=".", ecolor="r")
# plt.xlabel("Time [s]")
# plt.ylabel("Temperature [C]")
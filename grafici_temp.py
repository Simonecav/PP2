import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mylib import LinearFit

from get_data import time, temp, temp_error, T_bar, df, dtemp
from fit_posterior import E_a, E_b

# linearizzo dati e incertezze (err_ln(T) = (1/T)*err_T)
# dati_fit = pd.DataFrame({
#     "t": time,
#     # "T - T_bar": temp - T_bar,
#     # "dT": temp_error,
#     "ln(T - T_bar)": np.log(temp - T_bar), #- 0.10035342
#     "dT": (1/(temp - T_bar))*temp_error,
# })

# fit = ExpFit(df, "t", "T - T_bar", "dT")

# fit = LinearFit(dati_fit, "t", "ln(T - T_bar)", "dT")
# fig, ax = plt.subplots(1)
# fit.graph(ax, markersize=2, labels=("$t$ [s]", r"$T - \bar{T}$ [°C]"))
# ax.legend()
# plt.show()

# print(fit.get_chi2().pvalue)


def f(x, a, b):   
    return [a*np.exp(b*xi) for xi in x]

# t = df.drop(df[(df["Tempo(s)"] < 15) | (df["Tempo(s)"] > 25)].index)['Tempo(s)']
# T = df.drop(df[(df["Tempo(s)"] < 15) | (df["Tempo(s)"] > 25)].index)['Temperatura(C)']

plt.plot(time, f(time, E_a, E_b), '--', linewidth=1)
plt.errorbar(time, temp - T_bar, temp_error, ecolor='r', elinewidth=1, markersize=2, color='black', fmt='o')
plt.show()
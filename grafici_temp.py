import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mylib import LinearFit
plt.style.use("ggplot")

from get_data import time_linear, temp_linear, temp_error_linear, time_exp, temp_exp, temp_error_exp, T_bar 
from fit_posterior import E_a, E_b

# FIT LINEARE
# linearizzo dati e incertezze (err_ln(T) = (1/T)*err_T)
dati_fit = pd.DataFrame({
    "t": time_linear,
    "ln(T - T_bar)": np.log(temp_linear - T_bar), # - 0.10035342
    "dT": (1/(temp_linear - T_bar))*temp_error_linear,
})

fit = LinearFit(dati_fit, "t", "ln(T - T_bar)", "dT")
fig, ax = plt.subplots(1)
fit.graph(ax, markersize=2, labels=("$t$ [s]", r"$T - \bar{T}$ [°C]"))
ax.legend()
plt.savefig("./immagini/temperatura/4/lineare.png")
plt.show()

print(f"chi quadro e chi2 ridotto per il fit lineare: {fit.get_chi2().chi2}, {fit.get_chi2().rid}")
print(f"P value per il fit lineare: {fit.get_chi2().pvalue}")

# Sovrappongo ai dati l'esponenziale restituito dal fit per integrazione della posterior
def f(x, a, b):   
    return [a*np.exp(b*xi) for xi in x]

plt.plot(time_exp, f(time_exp, E_a, E_b), '--', linewidth=1, label='fit')
plt.errorbar(time_exp, temp_exp - T_bar, temp_error_exp, ecolor='r', elinewidth=1, markersize=2,
              color='black', fmt='o', label="dati")
plt.xlabel("$t$ [s]")
plt.ylabel("$T - \\bar{T}$ [°C]")
plt.legend()
plt.savefig("./immagini/temperatura/4/esponenziale.png")
plt.show()
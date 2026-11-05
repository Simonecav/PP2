import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from converti import converti
from mylib import LinearFit

plt.style.use("ggplot")

G = 9.81

M = [0, 31.5, 63.0, 101.3, 139.9] # g
P = [] # kPa
#S = [] # mm^2

P_0 = 101.11 # kPa

DP = []
beta = []

for i in range(1, 6):
    data_vol = converti(f"./misure/Tenuta_cilindro/posizione_senza_termometro/{i}.txt")*1.e2 # cm
    # if (i == 5):
    #     data_vol = data_vol.drop(data_vol[(data_vol['Tempo(s)'] > 80)].index)
    dh = 0.0022 # cm

    df = pd.DataFrame({
        "t": data_vol["Tempo(s)"],
        "h": data_vol["Posizione(m)"],
        "dh": np.repeat(dh, data_vol.__len__())
    })

    fit = LinearFit(df, "t", "h", "dh")

    alpha = fit.get_fit_params()[0][0] # cm/s

    print("alpha: ", alpha)
    print("p_value: ", fit.get_chi2().pvalue)

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 5)
    fit.graph(ax, ("$t$ [s]", "$h(t)$ [m]"), 2, 15)
    ax.set_title(f"$m$ = {M[i-1]} g", fontsize=18)
    plt.savefig(f"./immagini/tenuta_cilindro/senza_termometro/posizione_{i}.png")
    plt.show()

    # Ricava la superficie
    data_p = converti(f"./misure/Tenuta_cilindro/pressione_senza_termometro/{i}.txt")
    p_mean = data_p["Pressione(kPa)"].mean()

    S = ((M[i-1]*G)/p_mean)*1.e-2 # mm^2 -> cm^2

    alpha = alpha*60 # cm/min

    beta.append(alpha * S) # cm^3/min
    DP.append(p_mean)

fig, ax = plt.subplots()
fig.set_size_inches(8, 5)
ax.plot(DP, beta, "o")
ax.set_xlabel("$\\Delta P$ [kPa]", fontsize=15)
ax.set_ylabel("$\\beta$ [cm$^3$/min]", fontsize=15)
plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from converti import converti
from mylib import LinearFit

plt.style.use("ggplot")

G = 9.81

M = [0, 31.5, 63.0, 101.3, 139.9] # g
P = [] # kPa
P_0 = 101.11 # kPa

dm = 0.1 # g

df_beta = pd.DataFrame({
    "P": [],
    "beta": [],
    "d_beta": [],
})

for i in range(1, 5):
    data_vol = converti(f"./misure/Tenuta_cilindro/posizione_senza_termometro/{i+1}.txt")
    data_vol["Posizione(m)"] = -data_vol["Posizione(m)"]*1.e2 # converto in cm ed inverto
    if (i == 4):
        data_vol = data_vol.drop(data_vol[(data_vol['Tempo(s)'] > 80)].index)
    dh = 0.0022 # cm

    df = pd.DataFrame({
        "t": data_vol["Tempo(s)"],
        "h": data_vol["Posizione(m)"],
        "dh": np.repeat(dh, data_vol.__len__())
    })

    fit = LinearFit(df, "t", "h", "dh", True)

    alpha = fit.get_fit_params()[0][0] # cm/s

    print("alpha: ", alpha)
    print("p_value: ", fit.get_chi2().pvalue)

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 5)
    fit.graph(ax, ("$t$ [s]", "$h(t)$ [m]"), 2, 15)
    ax.set_title(f"$m$ = {M[i]} g", fontsize=18)
    plt.savefig(f"./immagini/tenuta_cilindro/senza_termometro/posizione_{i+1}.png")
    plt.show()

    # Ricava la superficie
    data_p = converti(f"./misure/Tenuta_cilindro/pressione_senza_termometro/{i+1}.txt")
    P = data_p["Pressione(kPa)"].mean() # media
    dP = np.sqrt(0.005**2 + (data_p["Pressione(kPa)"].std(ddof=1)**2)/data_p.__len__()) #kPa

    S = ((M[i]*G)/P)*1.e-2 # mm^2 -> cm^2

    dS = G * (M[i]/P)*np.sqrt((dm/M[i])**2 + (dP/P)**2) * 1.e-2

    alpha = alpha*60 # cm/s -> cm/min
    d_alpha = np.sqrt(fit.get_fit_params()[1][0][0]) * 60
    beta = alpha * S # cm^3/min
    # if i==0:
    #     d_beta = beta * np.sqrt((dP/P)**2 + (d_alpha/alpha)**2) 
    # else:
    d_beta = beta * np.sqrt((dS/S)**2 + (d_alpha/alpha)**2)

    df_beta.loc[i] = [P, beta, d_beta]

print(df_beta)

fit_beta = LinearFit(df_beta, "P", "beta", "d_beta")

fig, ax = plt.subplots()
fit_beta.graph(ax, ("$\\Delta P$ [kPa]", "$\\beta$ [cm$^3$/min]"), 5, 15)
plt.savefig("./immagini/tenuta_cilindro/senza_termometro/beta.png")
plt.show()

print(fit_beta.get_chi2().chi2)


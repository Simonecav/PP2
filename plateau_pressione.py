"""Legge il file di pressione, lo grafica e individua i tratti a pressione costante (plateau)."""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Parametri ----------------
FILE = sys.argv[1] if len(sys.argv) > 1 else "C:\\Users\\cacci\\Desktop\\workspace\\PP2\\misure\\Siringone\\2.csv"

FINESTRA = 10      # punti per la finestra mobile (10 punti = 1 s a 0.1 s di campionamento)
TOL = 0.01         # kPa: max - min nella finestra per considerarla "costante"
MIN_PUNTI = 30   # un plateau deve durare almeno questi punti per essere tenuto


INTERVALLI_MANUALI = []    
# -------------------------------------------
#(0,8), (38, 45), ( 74, 82), (115, 125), (160, 170)

#
df = pd.read_csv(FILE)
t = df.iloc[:, 0].to_numpy()
p = df.iloc[:, 1].to_numpy()


if INTERVALLI_MANUALI:
    maschera = np.zeros(len(t), dtype=bool)
    for t0, t1 in INTERVALLI_MANUALI:
        maschera |= (t >= t0) & (t <= t1)
else:
    s = pd.Series(p)
    escursione = s.rolling(FINESTRA, center=True).max() - s.rolling(FINESTRA, center=True).min() # finestra mobile che ogni 10 punti calcola l'escursione
    maschera = (escursione <= TOL).fillna(False).to_numpy() #se escursione <= TOL allora è costante

# Raggruppo i punti consecutivi in tratti e scarto quelli troppo corti
tratti = []
i = 0
while i < len(maschera): #finché è vero che vale sono nella tollerenza
    if maschera[i]:
        j = i
        while j + 1 < len(maschera) and maschera[j + 1]:
            j += 1
        if j - i + 1 >= MIN_PUNTI: #scarto tratti troppo corti
            tratti.append((i, j)) #unisco i tratti che superano lunghezza minima
        i = j + 1
    else:
        i += 1

# Risultati per ogni plateau
#print(f"{'#':>2} {'t_ini [s]':>10} {'t_fin [s]':>10} {'N':>5} {'media [kPa]':>12} {'std [kPa]':>10} {'sem [kPa]':>10}")
print(f" {'media [kPa]':>12} {'sem [kPa]':>10}")

for k, (i, j) in enumerate(tratti, 1):
    seg = p[i:j + 1]
    N = len(seg)
    std = seg.std(ddof=1)
    #print(f"{k:>2} {t[i]:>10.2f} {t[j]:>10.2f} {N:>5} {seg.mean():>12.6f} {std:>10.6f} {std/np.sqrt(N):>10.6f}")
    print(f"{seg.mean():>12.6f} {std/np.sqrt(N):>10.6f}")
   
    # Grafico dei dati grezzi, così come sono
plt.figure(figsize=(10, 4))
plt.plot(t, p, ".", color='r', markersize=4, linewidth=0.8)
plt.xlabel("Tempo [s]")
plt.ylabel("Pressione [kPa]")
plt.title("Dati")
plt.grid()
plt.tight_layout()

# Grafico
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, p, ".", color='r', markersize=4, linewidth=0.8, label="dati")
for k, (i, j) in enumerate(tratti):
    ax.axvspan(t[i], t[j], color="violet", alpha=0.4, label="plateau" if k == 0 else None)
ax.set_xlabel("Tempo [s]")
ax.set_ylabel("Pressione [kPa]")
ax.set_title(" Intervalli Costanti")
ax.grid()
ax.legend()
plt.tight_layout()
plt.show()


# Dati dei soli plateau, pronti per altri usi (es. il fit)
t_plateau = t[maschera]
p_plateau = p[maschera]

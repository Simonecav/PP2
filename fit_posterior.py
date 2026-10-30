import numpy as np
from scipy import stats
from matplotlib import cm, pyplot as plt
import my_lib_santanastasio as my
from scipy import integrate

from get_data import df, fluttuazione, T_bar, time, temp, dtemp

# dfmod = df.drop(df[(df["Tempo(s)"] < 15) | (df["Tempo(s)"] > 25)].index)

# t0 = dfmod["Tempo(s)"].to_numpy()[0]
# T0 = dfmod["Temperatura(C)"].to_numpy()[0]
# print(T0)

# time = dfmod["Tempo(s)"].to_numpy()-t0
# temp = dfmod["Temperatura(C)"].to_numpy()
# dtemp = np.sqrt(0.05**2 + fluttuazione**2)

x = time
y = temp - T_bar
uy = dtemp

def posterior(A,B,Y,X,SigmaY):    
    Yexp = A*np.exp(B*X) # modello di fit
    #print (Yexp)
    return np.prod( stats.norm.pdf(Y, Yexp, SigmaY) )

print (x)
print (y.round(2))
print (uy)

# m0, sm0, c0, sc0, cov0, rho0 = my.lin_fit(x, y, uy, "x [ux]", "y [uy]", 0, 3, 0, 15, plot=True, setrange=True)

# uy_new = np.sqrt(uy**2+(m0*ux)**2)

a_values = np.linspace(7.85, 8.05, 100)
b_values = np.linspace(-0.21, -0.22, 100)
a_mesh, b_mesh = np.meshgrid(a_values, b_values)

posterior_values = np.zeros(len(a_values)*len(b_values))
idx = 0
for aval, bval in np.nditer([a_mesh, b_mesh]):
    posterior_values[idx]=posterior(aval,bval,y,x,uy) 
    idx = idx + 1
posterior_mesh = posterior_values.reshape((len(a_values), len(b_values)))

fig = plt.figure()
ax1 = plt.contourf(a_mesh, b_mesh, posterior_mesh, cmap=cm.jet, levels=100)
cbar = plt.colorbar(ax1)
cbar.set_label('f(a,b)', rotation=270, labelpad=20)
plt.xlabel("a")
plt.ylabel("b")
plt.grid()
plt.title("Posterior probability density function")
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(a_mesh, b_mesh, posterior_mesh, cmap=cm.jet,
                       linewidth=0, antialiased=False)

ax.set_xlabel('a')
ax.set_ylabel('b')
ax.set_zlabel('f(a,b)')
plt.title("Posterior probability density function")
plt.show()

# Range delle variabili su cui fare inferenza

#it works with uy=0.1, ux=0
range_a = (7.85, 8.05)
range_b = (-0.21, -0.22)

#range_m = (0,10)
#range_c = (0,10)

# Integrale di normalizzazione della posterior
normalization, integral_error_norm = integrate.nquad(posterior, 
                                                    [range_a, #m
                                                     range_b  #c
                                                    ],
                                                    args=(y,x,uy)
                                                    )
print (normalization, integral_error_norm)

# Posterior normalizzata (PDF)
def posterior_norm(A,B,Y,X,SigmaY):    
    return posterior(A,B,Y,X,SigmaY) / normalization

# L'argomento dell'integrale del valore atteso di c^k 
def arg_E_a_k(A,B,k,Y,X,SigmaY):
    return np.power(A,k) * posterior_norm(A,B,Y,X,SigmaY)

# L'argomento dell'integrale del valore atteso di m^k 
def arg_E_b_k(A,B,k,Y,X,SigmaY):
    return np.power(B,k) * posterior_norm(A,B,Y,X,SigmaY)

# L'argomento dell'integrale del valore atteso di m*c
def arg_E_ab(A,B,Y,X,SigmaY):
    return A * B * posterior_norm(A,B,Y,X,SigmaY)

E_a, error_int_E_a = integrate.nquad(arg_E_a_k, 
                                    [range_a, #m
                                    range_b  #c
                                    ],
                                    args=(1,y,x,uy)#k=1
                                    )
E_a2, error_int_E_a2 = integrate.nquad(arg_E_a_k, 
                                        [range_a, #m
                                        range_b  #c
                                        ],
                                        args=(2,y,x,uy)#k=2
                                        )
Var_a = E_a2 - E_a**2
Sigma_a = np.sqrt(Var_a)

E_b, error_int_E_b = integrate.nquad(arg_E_b_k, 
                                    [range_a, #m
                                    range_b  #c
                                    ],
                                    args=(1,y,x,uy)#k=1
                                    )
E_b2, error_int_E_b2 = integrate.nquad(arg_E_b_k, 
                                        [range_a, #m
                                        range_b  #c
                                        ],
                                        args=(2,y,x,uy)#k=2
                                        )
Var_b = E_b2 - E_b**2
Sigma_b = np.sqrt(Var_b)

E_ab, error_int_E_ab = integrate.nquad(arg_E_ab, 
                                       [range_a, #m
                                        range_b  #c
                                        ],
                                        args=(y,x,uy)
                                        )
Cov_ab = E_ab - E_a*E_b
Rho_ab = Cov_ab / (Sigma_a*Sigma_b)

my.PrintResult("a_fit",E_a,Sigma_a,20,"[y/x]")
my.PrintResult("b_fit",E_b,Sigma_b,20,"[y]")
print("Cov[a,b] fit", Cov_ab)
print("Rho[a,b] fit", Rho_ab)


posterior_norm_b = lambda B: np.fabs(integrate.nquad(posterior_norm, [range_a], args=(B,y,x,uy))[0]) # Marginale
posterior_norm_b_vfunc = np.vectorize(posterior_norm_b)

posterior_norm_b_values = posterior_norm_b_vfunc(b_values)

plt.plot(b_values,posterior_norm_b_values,label='Posterior',linewidth=4)
plt.xlabel("b")
plt.ylabel("f(b)")
plt.axvline(x = E_b, color = 'r', linestyle='-',label='E[b]')
plt.axvline(x = E_b+Sigma_b, color = 'orange', linestyle='--', label=r'$E[b] \pm 1\sigma$')
plt.axvline(x = E_b-Sigma_b, color = 'orange', linestyle='--')
plt.plot(b_values, stats.norm.pdf(b_values,E_b,Sigma_b), linewidth=1, color='black',linestyle='--',label='Gaussian')
plt.legend()
plt.grid()
plt.show()


def posterior_a(B,A,Y,X,SigmaY):    
    Yexp = A*np.exp(B*X) # modello di fit
    return np.prod( stats.norm.pdf(Y, Yexp, SigmaY) )

def posterior_a_norm(B,A,Y,X,SigmaY):    
    return posterior_a(B,A,Y,X,SigmaY) / normalization

posterior_norm_a = lambda A: integrate.nquad(posterior_a_norm, [range_b], args=(A,y,x,uy))[0] # Marginale
posterior_norm_a_vfunc = np.vectorize(posterior_norm_a)

posterior_norm_a_values = posterior_norm_a_vfunc(a_values)

plt.plot(a_values,posterior_norm_a_values,label='Posterior',linewidth=4)
plt.xlabel("a")
plt.ylabel("f(a)")
plt.axvline(x = E_a, color = 'r', linestyle='-',label='E[a]')
plt.axvline(x = E_a+Sigma_a, color = 'orange', linestyle='--', label=r'$E[a] \pm 1\sigma$')
plt.axvline(x = E_a-Sigma_a, color = 'orange', linestyle='--')
plt.plot(a_values, stats.norm.pdf(a_values,E_a,Sigma_a), linewidth=1, color='black',linestyle='--',label='Gaussian')
plt.legend()
plt.grid()
plt.show()

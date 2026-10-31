import numpy as np
from scipy import stats
from matplotlib import cm, pyplot as plt
import my_lib_santanastasio as my
from scipy import integrate

plt.style.use("ggplot")

from get_data import T_bar, time_exp, temp_exp, dtemp

x = time_exp
y = temp_exp - T_bar
uy = dtemp

def posterior(A,B,Y,X,SigmaY):    
    Yexp = A*np.exp(B*X) # modello di fit
    #print (Yexp)
    return np.prod( stats.norm.pdf(Y, Yexp, SigmaY) )

#1
# alim = (16.3, 16.6)
# blim = (-0.2475, -0.2550)

#2
# alim = (15.7, 16)
# blim = (-0.226, -0.22)

#3
# alim = (12.6, 12.9)
# blim = (-0.212, -0.218)

#4
alim = (13.5, 14)
blim = (-0.226, -0.22)
# alim = (11, 11.5)
# blim = (-0.2, -0.22)

N = 250
a_values = np.linspace(alim[0], alim[1], N)
b_values = np.linspace(blim[0], blim[1], N)
a_mesh, b_mesh = np.meshgrid(a_values, b_values)

# posterior_values = np.zeros(len(a_values)*len(b_values))
# idx = 0
# for aval, bval in np.nditer([a_mesh, b_mesh]):
#     posterior_values[idx]=posterior(aval,bval,y,x,uy) 
#     idx = idx + 1
# posterior_mesh = posterior_values.reshape((len(a_values), len(b_values)))

# # selezione del picco 
# soglia = 1e-3 * posterior_mesh.max()
# mask = posterior_mesh > soglia
# a_sel = a_values[mask.any(axis=0)]
# b_sel = b_values[mask.any(axis=1)]

# # griglia stretta sul picco, poi rifai meshgrid, ciclo e reshape
# a_values = np.linspace(a_sel.min(), a_sel.max(), 100)
# b_values = np.linspace(b_sel.min(), b_sel.max(), 100)
# a_mesh, b_mesh = np.meshgrid(a_values, b_values)

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
plt.title("Posterior probability density function")
plt.savefig("immagini/temperatura/4/posterior2d.png")
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(a_mesh, b_mesh, posterior_mesh, cmap=cm.jet,
                       linewidth=0, antialiased=False)

ax.set_xlabel('a')
ax.set_ylabel('b')
ax.set_zlabel('f(a,b)')
plt.title("Posterior probability density function")
plt.savefig("immagini/temperatura/4/posterior3d.png")
plt.show()

# Range delle variabili su cui fare inferenza
range_a = alim
range_b = blim

# Integrale di normalizzazione della posterior
normalization, integral_error_norm = integrate.nquad(posterior, 
                                                    [range_a, #m
                                                     range_b  #c
                                                    ],
                                                    args=(y,x,uy)
                                                    )
#print (normalization, integral_error_norm)

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
print("Cov[a,b] fit: ", Cov_ab)
print("Rho[a,b] fit: ", Rho_ab)


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
plt.savefig("immagini/temperatura/4/dist_b.png")
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
plt.savefig("immagini/temperatura/4/dist_a.png")
plt.show()

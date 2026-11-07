from numpy import mean, std, sqrt

b = [-0.2516810254748465 , -0.22256111461456685, -0.21424012032021023, -0.22377013303476923]
tau = [(-(1/bi)) for bi in b]
print(tau)
print(f"{mean(tau)} +- {std(tau, ddof=1)/sqrt(len(tau))}")

# aria
b = [-0.011567207686187922, -0.009518416552539814]
tau = [(-(1/bi)) for bi in b]
print(tau)
print(f"{mean(tau)} +- {std(tau, ddof=1)/sqrt(len(tau))}")
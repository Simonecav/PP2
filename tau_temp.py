from numpy import mean, std

b = [-0.2516838066913005, -0.22256897858257801, -0.21425801792709875, -0.22377625490464467]
tau = [(-(1/bi)) for bi in b]
print(tau, mean(tau))
print(std(tau, ddof=1))
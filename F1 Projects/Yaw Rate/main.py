import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parámetros vehículo
m = 300       # kg
Iz = 150      # kg m^2
a = 0.8       # m
b = 0.8       # m
Cf = 40000    # N/rad
Cr = 35000    # N/rad
V = 20        # m/s

def bicycle_model(t, x):
    beta, r = x
    delta = 0.05  # steering input rad
    
    Fyf = Cf * (delta - beta - a*r/V)
    Fyr = Cr * (-beta + b*r/V)
    
    dbeta_dt = (Fyf + Fyr)/(m*V) - r
    dr_dt = (a*Fyf - b*Fyr)/Iz
    
    return [dbeta_dt, dr_dt]

sol = solve_ivp(bicycle_model, [0,2], [0,0], t_eval=np.linspace(0,2,500))

plt.plot(sol.t, sol.y[1])
plt.xlabel("Time (s)")
plt.ylabel("Yaw rate (rad/s)")
plt.title("Yaw response to steering input")
plt.show()
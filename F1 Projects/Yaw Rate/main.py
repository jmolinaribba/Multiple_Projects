import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Vehicle parameters
m = 300       # kg
Iz = 150      # kg m^2
a = 0.8       # m
b = 0.8       # m
Cf = 40000    # N/rad
Cr = 35000    # N/rad
V = 20        # m/s
L = a + b     # Wheelbase (m)

# 1. Dynamic Steering Input (Step Steer)
def steering_input(t):
    # Apply a 0.05 rad steer angle after 0.2 seconds
    return 0.05 if t >= 0.2 else 0.0

def bicycle_model(t, x):
    beta, r = x
    delta = steering_input(t) 
    
    # Tire slip angles (linear assumption)
    alpha_f = delta - beta - (a * r) / V
    alpha_r = -beta + (b * r) / V
    
    # Lateral tire forces
    Fyf = Cf * alpha_f
    Fyr = Cr * alpha_r
    
    # Equations of motion
    dbeta_dt = (Fyf + Fyr) / (m * V) - r
    dr_dt = (a * Fyf - b * Fyr) / Iz
    
    return [dbeta_dt, dr_dt]

# 2. Calculate Theoretical Steady-State Yaw Rate
# Understeer gradient (Ku) calculation
Ku = (m * (b * Cr - a * Cf)) / (2 * L * Cf * Cr) 
steady_state_yaw = V / (L + Ku * V**2) * 0.05 # For delta = 0.05

# Solve ODE
sol = solve_ivp(bicycle_model, [0, 2], [0, 0], t_eval=np.linspace(0, 2, 500))
beta_deg = np.degrees(sol.y[0])
yaw_rate_deg = np.degrees(sol.y[1])
t = sol.t

# 3. Enhanced Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Yaw Rate Plot
ax1.plot(t, yaw_rate_deg, label='Simulated Yaw Rate', color='blue', linewidth=2)
ax1.axhline(np.degrees(steady_state_yaw), color='red', linestyle='--', label=f'Steady State: {np.degrees(steady_state_yaw):.1f} deg/s')
ax1.set_ylabel("Yaw rate (deg/s)")
ax1.set_title(f"Yaw Response (V = {V} m/s) | Understeer Gradient: {Ku:.4f}")
ax1.legend()
ax1.grid(True)

# Sideslip Plot
ax2.plot(t, beta_deg, label='Sideslip Angle (Beta)', color='orange', linewidth=2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Sideslip Angle (deg)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
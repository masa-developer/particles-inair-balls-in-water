# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 08:48:58 2025

@author: VK
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81   # m/s²
rho_p = 7800   # ball density (kg/m³)
rho_f = 1000   # water density (kg/m³)
mu = 1.0e-3    # water viscosity (Pa·s)

# Ball diameters to simulate (m)
diameters = [0.01, 0.1, 0.3]

# Drag coefficient correlation (Schiller-Naumann)
def C_d(Re):
    if Re <= 0:
        return 1e6
    if Re < 1000:
        return 24/Re * (1 + 0.15 * Re**0.687)
    else:
        return 0.44

def simulate(d, t_max=5.0, dt=0.001):
    """ Simulate sinking of a ball of diameter d (m). """
    # Geometry
    V = np.pi/6 * d**3      # volume (m³)
    A = np.pi/4 * d**2      # projected area (m²)
    m = rho_p * V           # mass (kg)

    # Initial conditions
    z, v, t = 0.0, 0.0, 0.0
    depth, velocities, time = [z], [v], [t]

    while t < t_max:
        # Reynolds number
        Re = rho_f * abs(v) * d / mu

        # Drag force
        Fd = 0.5 * C_d(Re) * rho_f * A * v * abs(v)  # sign with v

        # Net force (downward positive)
        Fg = rho_p * V * g
        Fb = rho_f * V * g
        Fnet = Fg - Fb - Fd

        # Acceleration
        a = Fnet / m

        # Update velocity and position
        v = v + a * dt
        z = z + v * dt

        # Store results
        t += dt
        time.append(t)
        depth.append(z)
        velocities.append(v)

    return np.array(time), np.array(depth), np.array(velocities)

# --- Run simulations ---
results = {}
for d in diameters:
    time, depth, vel = simulate(d)
    results[d] = (time, depth, vel)

# --- Plot velocity vs depth ---
plt.figure(figsize=(7,5))
for d in diameters:
    time, depth, vel = results[d]
    plt.plot(depth, vel, lw=2, label=f"d = {d} m")
plt.xlabel("Depth below surface (m)")
plt.ylabel("Velocity (m/s)")
plt.title("Sinking velocity vs depth for different ball diameters")
plt.grid(True)
plt.legend()
plt.show()

# --- Plot depth vs time (with depth increasing downward) ---
plt.figure(figsize=(7,5))
for d in diameters:
    time, depth, vel = results[d]
    plt.plot(time, depth, lw=2, label=f"d = {d} m")
plt.xlabel("Time (s)")
plt.ylabel("Depth below surface (m)")
plt.title("Sinking trajectory of balls in water")
plt.grid(True)
plt.legend()
plt.gca().invert_yaxis()  # depth increases downward
plt.show()

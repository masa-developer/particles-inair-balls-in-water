# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 12:29:11 2025

@author: VK
"""



import math
import pandas as pd
import matplotlib.pyplot as plt

# Constants
g = 9.81   # gravity (m/s^2)
rho_f = 1.2   # air density (kg/m^3)
mu = 1.8e-5   # air dynamic viscosity (Pa·s)

# Particle densities to study
particle_densities = [2500, 1500, 600, 100]

# Define velocity range (0.0 to 10.0 m/s, step 0.5)
velocities = [round(v, 1) for v in [i * 0.5 for i in range(1, 21)]]

# Collect results
all_results = []

for rho_p in particle_densities:
    for v_air in velocities:
        d_max = math.sqrt((18 * mu * v_air) / (g * (rho_p - rho_f)))  # meters
        all_results.append([rho_p, v_air, d_max * 1e6])  # micrometers

# Create DataFrame
df = pd.DataFrame(all_results, columns=["Particle density (kg/m³)", "Air velocity (m/s)", "Max particle diameter (µm)"])

# Print first rows for quick check
print(df.head(12))  # just a preview

# Pivot table for better readability
table = df.pivot(index="Air velocity (m/s)", columns="Particle density (kg/m³)", values="Max particle diameter (µm)")
print("\nTable of maximum particle diameter (µm):")
print(table.round(2))

# Plotting
plt.figure(figsize=(8, 6))
for rho_p in particle_densities:
    subset = df[df["Particle density (kg/m³)"] == rho_p]
    plt.plot(subset["Air velocity (m/s)"], subset["Max particle diameter (µm)"],
             marker="o", linestyle="-", label=f"{rho_p} kg/m³")

plt.title("Maximum Particle Diameter vs. Air Velocity", fontsize=14)
plt.xlabel("Air velocity (m/s)", fontsize=12)
plt.ylabel("Max particle diameter (µm)", fontsize=12)
plt.legend(title="Particle density")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

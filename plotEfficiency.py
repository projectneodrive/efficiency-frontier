import numpy as np
import matplotlib.pyplot as plt

# Constants
rho = 1.225   # air density kg/m^3
g = 9.81      # earth gravity

# Speed range
v = np.linspace(1, 25, 400)  # m/s (avoid 0 to prevent division by zero)

# Vehicle parameters
vehicles = {
    "cityEL": {
        "Cd": 0.30, "A": 1.0, "Crr": 0.015, "m": 300, "eta": 0.7
    },
    "tesla_model3": {
        "Cd": 0.23, "A": 2.22, "Crr": 0.010, "m": 1760, "eta": 0.85
    },
    "citroen_2CV": {
        "Cd": 0.51, "A": 1.8, "Crr": 0.015, "m": 600, "eta": 0.25
    },
    "small_petrol_car": {  # e.g., Toyota Yaris or VW Polo
        "Cd": 0.32, "A": 2.0, "Crr": 0.012, "m": 1100, "eta": 0.25
    },
    "toyota_prius": {
        "Cd": 0.24, "A": 2.16, "Crr": 0.010, "m": 1375, "eta": 0.35
    },
    "toyota_prius_battery_only": {
        "Cd": 0.24, "A": 2.16, "Crr": 0.010, "m": 1375, "eta": 0.85
    },
    "velomobile_quest": {
        "Cd": 0.20, "A": 0.55, "Crr": 0.005, "m": 125, "eta": 0.98
    },
    "bmw_X1_SUV": {
        "Cd": 0.33, "A": 2.6, "Crr": 0.012, "m": 1650, "eta": 0.25
    },
    "smart_fortwo": {
        "Cd": 0.35, "A": 2.0, "Crr": 0.012, "m": 900, "eta": 0.25
    },
    "bike_upright": {
        "Cd": 1.00, "A": 0.6, "Crr": 0.005, "m": 80+20, "eta": 0.98
    },
    "neodrive": {
        "Cd": 0.2, "A": 1, "Crr": 0.005, "m": 80 + 50, "eta": 0.75
    }
}

# Compute consumption in kWh/100km
consumption = {}

for name, params in vehicles.items():
    F_roll = params["Crr"] * params["m"] * g
    F_aero = 0.5 * rho * params["Cd"] * params["A"] * v**2
    F_total = F_roll + F_aero
    P_wheel = F_total * v  # W
    P_batt = P_wheel / params["eta"]
    E_per_m = P_batt / v
    kWh_per_100km = E_per_m * 100000 / 3.6e6
    consumption[name] = kWh_per_100km

# Plot with logarithmic y-axis
plt.figure(figsize=(9,6))
for name, cons in consumption.items():
    plt.plot(v*3.6, cons, label=name)

plt.xlabel("Speed (km/h)")
plt.ylabel("Consumption (kWh/100 km) [log scale]")
plt.title("Vehicle Consumption vs Speed (log scale)")
plt.yscale("log")
plt.grid(True, which="both", linestyle="--")
plt.legend()
plt.show()
plt.savefig("Efficiency.png")
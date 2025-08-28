import numpy as np
import matplotlib.pyplot as plt

# Constants
rho = 1.225   # air density kg/m^3
g = 9.81      # earth gravity

# Speed range
v = np.linspace(1, 35, 400)  # m/s (avoid 0 to prevent division by zero)

# Vehicle parameters
vehicles = {
    "cityEL": {"Cd": 0.30, "A": 1.0, "Crr": 0.015, "m": 300, "eta": 0.7},
    "tesla_model3": {"Cd": 0.23, "A": 2.22, "Crr": 0.010, "m": 1760, "eta": 0.85},
    "citroen_2CV": {"Cd": 0.51, "A": 1.8, "Crr": 0.015, "m": 600, "eta": 0.25},
    "small_petrol_car": {"Cd": 0.32, "A": 2.0, "Crr": 0.012, "m": 1100, "eta": 0.25},
    "toyota_prius": {"Cd": 0.24, "A": 2.16, "Crr": 0.010, "m": 1375, "eta": 0.35},
    "toyota_prius_battery_only": {"Cd": 0.24, "A": 2.16, "Crr": 0.010, "m": 1375, "eta": 0.85},
    "velomobile_quest": {"Cd": 0.20, "A": 0.55, "Crr": 0.005, "m": 125, "eta": 0.98},
    "bmw_X1_SUV": {"Cd": 0.33, "A": 2.6, "Crr": 0.012, "m": 1650, "eta": 0.25},
    "smart_fortwo": {"Cd": 0.35, "A": 2.0, "Crr": 0.012, "m": 900, "eta": 0.25},
    "bike_upright": {"Cd": 1.00, "A": 0.6, "Crr": 0.005, "m": 100, "eta": 0.98},
    "neodrive": {"Cd": 0.2, "A": 1, "Crr": 0.005, "m": 130, "eta": 0.75},
    "train": {"Cd": 1, "A": 0.4, "Crr": 0.0003, "m": 7500, "eta": 0.95}
}


def plot_consumption_vs_speed(vehicles, v):
    """Plot consumption (kWh/100km) vs speed"""
    plt.figure(figsize=(9,6))
    for name, params in vehicles.items():
        F_roll = params["Crr"] * params["m"] * g
        F_aero = 0.5 * rho * params["Cd"] * params["A"] * v**2
        F_total = F_roll + F_aero
        P_wheel = F_total * v  # W
        P_batt = P_wheel / params["eta"]
        E_per_m = P_batt / v
        kWh_per_100km = E_per_m * 100000 / 3.6e6
        plt.plot(v*3.6, kWh_per_100km, label=name)

    plt.xlabel("Speed (km/h)")
    plt.ylabel("Consumption (kWh/100 km) [log scale]")
    plt.title("Vehicle Consumption vs Speed (log scale)")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.savefig("Efficiency.png")
    plt.show()


def plot_power_vs_speed(vehicles, v):
    """Plot required battery power vs speed (flat road)"""
    plt.figure(figsize=(9,6))
    for name, params in vehicles.items():
        F_roll = params["Crr"] * params["m"] * g
        F_aero = 0.5 * rho * params["Cd"] * params["A"] * v**2
        F_total = F_roll + F_aero
        P_wheel = F_total * v  # W
        P_batt = P_wheel / params["eta"]
        plt.plot(v*3.6, P_batt/1000, label=name)  # kW

    plt.xlabel("Speed (km/h)")
    plt.ylabel("Power demand (kW) [log scale]")
    plt.title("Vehicle Power vs Speed (flat road, log scale)")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.savefig("Power.png")
    plt.show()


def plot_power_vs_speed_slope(vehicles, v, slope_fraction, filename):
    """Plot power vs speed for a given road slope"""
    plt.figure(figsize=(9,6))
    for name, params in vehicles.items():
        F_roll = params["Crr"] * params["m"] * g
        F_aero = 0.5 * rho * params["Cd"] * params["A"] * v**2
        F_slope = params["m"] * g * slope_fraction
        F_total = F_roll + F_aero + F_slope
        P_wheel = F_total * v  # W
        P_batt = P_wheel / params["eta"]
        plt.plot(v*3.6, P_batt/1000, label=name)  # kW

    plt.xlabel("Speed (km/h)")
    plt.ylabel("Power demand (kW) [log scale]")
    plt.title(f"Vehicle Power vs Speed ({int(slope_fraction*100)}% slope, log scale)")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.savefig(filename)
    plt.show()


def plot_power_vs_acceleration(vehicles, v, acc, filename):
    """Plot power vs speed for different accelerations at a given speed"""
    plt.figure(figsize=(9,6))

    for name, params in vehicles.items():
        F_roll = params["Crr"] * params["m"] * g
        F_aero = 0.5 * rho * params["Cd"] * params["A"] * v**2
        F_acc = params["m"] * acc * g
        F_total = F_roll + F_aero + F_acc
        P_wheel = F_total * v  # W
        P_batt = P_wheel / params["eta"]
        plt.plot(v*3.6, P_batt/1000,
                 label=f"{name}, {acc:.1f} g")

    plt.xlabel("Speed (km/h)")
    plt.ylabel("Power demand (kW) [log scale]")
    plt.title(f"Vehicle Power vs Speed for Accelerations of {acc} g")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.savefig(filename)
    plt.show()


def main():
    plot_consumption_vs_speed(vehicles, v)
    plot_power_vs_speed(vehicles, v)
    plot_power_vs_speed_slope(vehicles, v, 0.05, "Power_5percent_slope.png")
    plot_power_vs_speed_slope(vehicles, v, 0.10, "Power_10percent_slope.png")
    plot_power_vs_acceleration(vehicles, v, 1.0, "Power_acceleration10.png")
    plot_power_vs_acceleration(vehicles, v, 0.5, "Power_acceleration05.png")
    plot_power_vs_acceleration(vehicles, v, 0.3, "Power_acceleration03.png")
    plot_power_vs_acceleration(vehicles, v, 0.2, "Power_acceleration02.png")
    plot_power_vs_acceleration(vehicles, v, 0.1, "Power_acceleration01.png")
if __name__ == "__main__":
    main()

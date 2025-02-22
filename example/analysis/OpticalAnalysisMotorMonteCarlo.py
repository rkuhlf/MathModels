import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lib.data import hist_box_count, plot_all_sims, read_sims
from lib.visualization import make_matplotlib_big



# Analysis functions to operate on a folder generated by the monte carlo simulation of a motor

def plot_exit_pressures(sims):
    plot_all_sims(sims, y="nozzle.exit_pressure")

    plt.ylabel("Pressure (Pa)")
    plt.xlabel("Time (s)")
    plt.title("Exit Pressures")

def display_exit_pressures(sims):
    plot_exit_pressures(sims)
    
    plt.show()


def plot_with_size(x, y, s):
    for i in range(len(x) - 1):
        plt.plot(x[i:i+2], y[i:i+2], 'k', linewidth=s[i])


def display_CG_components(sim):
    x = sim["time"]
    # plt.plot(x, sim["ox_tank.oxidizer_center_of_mass"], alpha=[0.5])
    # plt.plot(x, sim["fuel_grain.total_CG"])
    mass_scaler = 0.3
    offset = 1.613
    dry_mass = 49.989
    dry_CG = 3.454

    # plt.plot(x, sim["ox_tank.oxidizer_center_of_mass"], color="b")
    plot_with_size(x, sim["ox_tank.oxidizer_center_of_mass"] + offset, sim["ox_tank.ox_mass"] * mass_scaler)
    
    # plt.plot(x, sim["fuel_grain.total_CG"], color="b")
    plot_with_size(x, sim["fuel_grain.total_CG"] + offset, sim["fuel_grain.fuel_mass"] * mass_scaler)

    plt.plot(x, sim["propellant_CG"] + offset)
    plt.plot([min(x), max(x)], [dry_CG] * 2)

    plt.plot(x, (dry_mass * dry_CG + sim["propellant_mass"] * (sim["propellant_CG"] + offset)) / (dry_mass + sim["propellant_mass"]))

    plt.axis([min(x), max(x), 6, 0])

    plt.show()


def display_overview(characteristic_figures):
    plt.scatter(characteristic_figures["Burn Time"], characteristic_figures["Total Impulse"])

    plt.title("Motor Comprehensive Monte Carlo")
    plt.xlabel("Burn Time (s)")
    plt.ylabel("Total Impulse (Ns)")

    plt.show()

def display_efficiency(characteristic_figures):
    # I think that this does not work right when it is passed the characteristic figures in one transposition, and it does work in the other
    # Might need a .transpose()
    plt.hist(characteristic_figures[["Total Specific Impulse", "Used Specific Impulse"]], hist_box_count(len(characteristic_figures)), histtype='bar', label=["Total Specific Impulse", "Used Specific Impulse"])
    plt.legend()

    plt.title("Monte Carlo Motor Efficiencies")
    plt.xlabel("Efficiency [s]")
    plt.ylabel("Frequency")

    plt.show()

def display_average_thrust(characteristic_figures):
    plt.scatter(characteristic_figures["Total Impulse"], characteristic_figures["Average Thrust"])

    plt.title("Monte Carlo Motor Average Thrust")
    # We should be aiming for all of the average thrust values to be above a certain threshold, which will give us a good liftoff, and we want everything to be as far to the right as possible
    plt.ylabel("Average Thrust (N)")
    plt.xlabel("Total Impulse (Ns)")

    plt.show()

def display_cstar_importance(characteristic_figures):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.scatter(characteristic_figures["Combustion Efficiency"], characteristic_figures["Total Impulse"])
    ax1.set(title="Monte Carlo C* Efficiency Importance", xlabel="C* Efficiency ()", ylabel="Total Impulse (Ns)")

    ax2.scatter(characteristic_figures["Combustion Efficiency"], characteristic_figures["Burn Time"])
    ax2.set(title="Monte Carlo C* Efficiency Importance", xlabel="C* Efficiency ()", ylabel="Burn Time (s)")

    fig.tight_layout()

    plt.show()

def display_OF_correlation(characteristic_figures):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.scatter(characteristic_figures["Average OF"], characteristic_figures["Total Impulse"])
    ax1.set(title="Monte Carlo OF Importance", xlabel="O/F ()", ylabel="Total Impulse (Ns)")

    ax2.scatter(characteristic_figures["Average Regression"] * 1000, characteristic_figures["Total Impulse"])
    ax2.set(title="Monte Carlo Regression Rate Importance", xlabel="Regression Rate (mm/s)", ylabel="Total Impulse (Ns)")

    fig.tight_layout()

    plt.show()

def display_end_temperature_distribution(sims):
    start_temps = []
    end_temps = []

    for sim in sims:
        try:
            start_temps.append((sim.iloc[0]["ox_tank.temperature"] - 273.15) * 9/5 + 32)
            end_temps.append((sim.iloc[-1]["ox_tank.temperature"] - 273) * 9/5 + 32)
        except Exception:
            print("Skipping because of error; probable non-simulation included in folder")
    
    plt.scatter(end_temps, start_temps)
    plt.xlabel("Final Temperature (F)")
    plt.ylabel("Initial Temperature (F)")
    plt.title("Range of Final Temperatures")

    plt.show()

def display_starting_fuel_mass_distribution(sims):
    fuel_mass = []

    for sim in sims:
        try:
            fuel_mass.append((sim.iloc[0]["fuel_grain.fuel_mass"]))
        except Exception:
            print("Skipping because of error; probable non-simulation included in folder")
    
    plt.hist(fuel_mass, bins=13)
    plt.xlabel("Fuel Mass (kg)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Launch Masses")

    print(np.average(fuel_mass))

    plt.show()

def display_final_mass_distribution(sims, dry_weight=0):
    propellant_mass = []

    for sim in sims:
        try:
            propellant_mass.append((sim.iloc[-1]["propellant_mass"]) + dry_weight)
        except Exception:
            print("Skipping because of error; probable non-simulation included in folder")
    

    print(np.average(propellant_mass))
    print(np.std(propellant_mass))
    
    plt.hist(propellant_mass, bins=13)
    plt.xlabel("Final Mass (kg)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Deployment Masses")

    plt.show()


#region Many curves
thin_lines = {
    "linewidth": 1.5,
    "alpha": 0.3
}

dark_green = {
    "color": (31/255, 145/255, 38/255)
}

black = {
    "color": (0/255, 0/255, 0/255)
}

def display_curves(sims):
    # Once again, this is not working for the monte carlo class. Skips all of the sims
    plot_all_sims(sims, x="time", y="thrust", **thin_lines, **black)
    plt.title("Thrust Curves")
    plt.xlabel("Time (s)")
    plt.ylabel("Thrust (N)")

    plt.show()

def display_CG_movement(sims):
    plot_all_sims(sims, x="time", y="propellant_CG", **thin_lines, **black)
    plt.title("CG Curves")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")

    plt.show()

def display_regression(characteristic_figures, sims):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    # Convert from m to mm
    ax1.hist(characteristic_figures["Length Regressed"] * 1000, hist_box_count(len(characteristic_figures)))
    ax1.set(title="Distribution of Ending Regression", xlabel="Length Regressed (mm)")

    plt.sca(ax2)
    plot_all_sims(sims, "time", "combustion_chamber.fuel_grain.geometry.length_regressed", **thin_lines, **black)
    ax2.set(title="Regression Lines", xlabel="Time (s)", ylabel="Length Regressed (m)")

    fig.tight_layout()

    plt.show()

#endregion

def display_general(characteristic_figures, sims):
    display_overview(characteristic_figures)
    display_efficiency(characteristic_figures)
    display_average_thrust(characteristic_figures)
    display_cstar_importance(characteristic_figures)
    display_OF_correlation(characteristic_figures)
    display_regression(characteristic_figures, sims)
    


if __name__ == "__main__":
    folder = "Analysis/MotorMonteCarloUpdatedDimensions2"
    sims = read_sims(folder)
    characteristic_figures = pd.read_csv(f"{folder}/output.csv")

    # display_starting_fuel_mass_distribution(sims)
    # display_end_temperature_distribution(sims)
    display_final_mass_distribution(sims)
    # make_matplotlib_big()
    # display_general(characteristic_figures, sims)
    # display_efficiency(characteristic_figures)
    # display_curves(sims)
    # display_regression(characteristic_figures, sims)

    # print(sims)
    
    # sims = read_sims("./Analysis/MontecarloMotorData/MotorMonteCarloAccurateLoadDistribution-Temporary")
    # display_exit_pressures(sims)


    df = pd.read_csv("./Analysis/MotorMonteCarloAccurateLoadDistribution/1.csv")
    # print(df.keys())
    # display_CG_components(df)

    pass
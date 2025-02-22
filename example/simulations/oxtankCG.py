# Display the center of mass of the ox tank over a linear drain (because it doesn't matter how quickly you drain atm)


import matplotlib.pyplot as plt
import numpy as np



from src.rocketparts.motorparts.oxtank import OxTank

# 
def run_simulation(ox: OxTank=OxTank(ox_mass=52.43, length=3.2, radius=0.17145 / 2, temperature=293.15)):
# Higher than 36 Celsius is super critical. Please don't do that
    masses = []
    ullages = []
    centers = []
    temperatures = []
    pressures = []

    for _ in range(55):
        masses.append(ox.ox_mass)
        ullages.append(ox.ullage)
        centers.append(ox.oxidizer_center_of_mass / ox.length)
        temperatures.append(ox.temperature)
        pressures.append(ox.pressure)
        # Drain 1 kg out of the tank.
        ox.update_mass(-1)
    print(centers)
    return masses, ullages, centers, temperatures, pressures


def display_important_conditions(temperatures, pressures):
    important_temperatures = temperatures[:int(len(temperatures) * 0.75)]
    print(f"The average of the first 3/4 of temperatures is {np.average(important_temperatures)} Kelvin")

    important_pressures = pressures[:int(len(pressures) * 0.75)]
    print(f"The average of the first 3/4 of pressures is {np.average(important_pressures) / 10**5} bar")


def display_CG_shift(masses, ullages, centers, temperatures, pressures):

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    ax1.plot(masses, ullages, label="Ullage")
    ax1.plot(masses, centers, label="Center of Mass")

    ax1.set_title("Ullage over Mass Drain")

    ax1.set_xlim(1, 60)
    ax1.set_xlabel("Ox Mass [kg]")
    ax1.invert_xaxis()

    ax1.set_ylim(0, 1)
    ax1.set_ylabel("Fraction")
    ax1.invert_yaxis()


    ax1.legend(loc="upper right")


    ax2.plot(masses, temperatures)
    ax2.set_title("Temperature over Mass Drain")
    ax2.set_xlabel("Ox Mass [kg]")
    ax2.set_ylabel("Temperature [K]")
    ax2.invert_xaxis()

    ax3.plot(masses, pressures)
    ax3.set_title("Pressure over Mass Drain")
    ax3.set_xlabel("Ox Mass [kg]")
    ax3.set_ylabel("Pressure [Pa]")
    ax3.invert_xaxis()

    fig.tight_layout()

    plt.show()



if __name__ == "__main__":
    # outputs = run_simulation()

    # display_CG_shift(*outputs)

    # Calculated 109 in for ox length (a little fudged)
    # This diameter should give us the correct total volume
    # ox = OxTank(temperature=293.15, length=2.69, diameter=0.1716, ox_mass=45, front=0)
    ox = OxTank(temperature=293.15, length=2.69, diameter=0.1716, ox_mass=45*0.5, front=0)

    print(ox.oxidizer_center_of_mass)
    # 1.45 m * 45 + 46.3 * 3.28 + 11.9 * 4.82 
    # 45 + 46.3 + 11.9

    pass
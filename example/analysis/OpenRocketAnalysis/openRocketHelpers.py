

from random import gauss
from matplotlib import pyplot as plt
import numpy as np
import orhelper
from orhelper import FlightDataType


# from net.sf.openrocket import document # type: ignore


from lib.data import load_environment_variable


OR_JAR_PATH = load_environment_variable('OR_JAR_PATH')
CURRENT_SIMULATION = load_environment_variable('CURRENT_OR_SIMULATION')


def new_or_instance():
    import javaInitialization
    return orhelper.OpenRocketInstance(jar_path=OR_JAR_PATH)

def most_updated_sim(orhelper):
    doc = orhelper.load_doc(CURRENT_SIMULATION)
    sim = getSimulationByName(doc, 'Custom CG; Regular Wind')

    return sim

def get_randomized_sim(orhelper):
    doc = orhelper.load_doc(CURRENT_SIMULATION)
    sim = getSimulationByName(doc, 'Custom CG; Regular Wind')
    opts = sim.getOptions()

    # TODO: make a better wind speed override that varies with altitude
    # This is a single data point from a wind table at ~30,000 ft in the air
    opts.setWindSpeedAverage(gauss(12.2, 6.1))
    opts.setISAAtmosphere(gauss(0, 1) < 0)
    opts.setWindTurbulenceIntensity(gauss(0.1, 0.05))

    # Kelvin
    opts.setLaunchTemperature(gauss(297, 7))
    opts.setLaunchAltitude(gauss(1300, 10))
    opts.setLaunchRodLength(gauss(12.5, 0.5))
    opts.setLaunchRodAngle(gauss(0, 0.05))
    opts.setLaunchPressure(gauss(101325, 100))


    return sim


def getSimulationNames(document):
    print([sim.getName() for sim in document.getSimulations()])

def getSimulationByName(document, name: str):
    """Accepts openrocket document; returns simulation with the given name"""

    for sim in document.getSimulations():
        sim.getName()
        if sim.getName() == name:
            return sim

    return None

def apogee(sim):
    return sim.getSimulatedData().getMaxAltitude()



# FIXME: this should really be a part of the Logger rewrite
def graph_vertical(orh: orhelper.Helper, sim):
    data = orh.get_timeseries(sim, [FlightDataType.TYPE_TIME, FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_VELOCITY_Z])

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(data[FlightDataType.TYPE_TIME], data[FlightDataType.TYPE_ALTITUDE], 'b-')
    ax2.plot(data[FlightDataType.TYPE_TIME], data[FlightDataType.TYPE_VELOCITY_Z], 'r-')
    # ax2.plot(data[FlightDataType.TYPE_TIME], data[FlightDataType.TYPE_ACCELERATION_Z], 'r-')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Altitude (m)', color='b')
    ax2.set_ylabel('Vertical Velocity (m/s)', color='r')
    change_color = lambda ax, col: [x.set_color(col) for x in ax.get_yticklabels()]
    change_color(ax1, 'b')
    change_color(ax2, 'r')


    ax1.grid(True)
    plt.show()

def graph_stability(orh: orhelper.Helper, sim):
    cp = FlightDataType.TYPE_CP_LOCATION
    cg = FlightDataType.TYPE_CG_LOCATION
    stability = FlightDataType.TYPE_STABILITY
    t = FlightDataType.TYPE_TIME
    data = orh.get_timeseries(sim, [t, cp, cg, stability])

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.plot(data[t], data[cp], 'b-', label="CP")
    ax1.plot(data[t], data[cg], 'r-', label="CG")

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Distance from Tip (m)')

    ax2.plot(data[t], data[stability])
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Stability (cal)')


    ax1.grid(True)
    ax2.grid(True)

    ax1.legend()

    plt.tight_layout()
    plt.show()

def graph_angles(orh: orhelper.Helper, sim):
    phi = FlightDataType.TYPE_ORIENTATION_PHI
    theta = FlightDataType.TYPE_ORIENTATION_THETA
    aoa = FlightDataType.TYPE_AOA
    t = FlightDataType.TYPE_TIME
    data = orh.get_timeseries(sim, [t, phi, theta, aoa])

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.plot(data[t], data[phi], 'b-', label="phi")
    ax1.plot(data[t], data[theta], 'r-', label="theta")

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Orientation (rad)')

    ax2.plot(data[t], data[aoa])
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Angle of Attack (rad)')


    ax1.grid(True)
    ax2.grid(True)

    ax1.legend()

    plt.tight_layout()

    plt.show()



def graph_destabilization(orh: orhelper.Helper, sim):
    phi = FlightDataType.TYPE_ORIENTATION_PHI
    theta = FlightDataType.TYPE_ORIENTATION_THETA
    aoa = FlightDataType.TYPE_AOA
    wind = FlightDataType.TYPE_WIND_VELOCITY
    vertical = FlightDataType.TYPE_VELOCITY_Z
    lateral = FlightDataType.TYPE_VELOCITY_XY
    cp = FlightDataType.TYPE_CP_LOCATION
    cg = FlightDataType.TYPE_CG_LOCATION

    t = FlightDataType.TYPE_TIME
    data = orh.get_timeseries(sim, [t, phi, theta, aoa, wind, lateral, vertical, cp, cg])

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    ax1.plot(data[t], data[phi], 'b-', label="phi")
    ax1.plot(data[t], data[theta], 'r-', label="theta")

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Orientation (rad)')

    ax2.plot(data[t], data[aoa])
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Angle of Attack (rad)')


    ax3.plot(data[t], data[wind], 'b-', label="wind")
    ax3.plot(data[t], data[vertical], 'r-', label="vertical")
    ax3.plot(data[t], data[lateral], 'g-', label="lateral")

    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Velocity (m/s)')


    ax4.plot(data[t], data[cp], 'b-', label="CP")
    ax4.plot(data[t], data[cg], 'r-', label="CG")

    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Distance from Tip (m)')


    for ax in fig.axes:
        ax.grid(True)

    ax1.legend()
    ax3.legend()
    ax4.legend()

    plt.tight_layout()
    plt.show()

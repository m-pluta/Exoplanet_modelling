import math
import os

import matplotlib.pyplot as plt
import numpy as np

import c


# This function is used to make the plot look more professional by adding a Title to the figure
# as well as labels for the x and y axes.
# It also adds minor ticks to each of the axes to make reading values of the plots easier
# It also modifies the thickness of all the grid lines
def beautifyPlot(fig, Title, x_axis, y_axis):
    # Adding labels for title and axes
    fig.suptitle(Title, fontsize=14)
    plt.xlabel(x_axis, fontsize=10)
    plt.ylabel(y_axis, fontsize=10)
    plt.minorticks_on()  # minor ticks

    # Drawing major & minor gridlines
    plt.grid(b=True, which='major', color='black', linestyle='-', linewidth=0.5)
    plt.grid(b=True, which='minor', color='grey', linestyle=':', linewidth=0.2)
    return fig


# This function plot the horizontal line for 0°C so it is easier to gauge if a temperature
# would be habitable for humans
# It does this by plotting a horizontal line at 273.15°K between two x co-ordinates
# It also adds a legend to plot so it is possible to identify the 0°C line
def plotCelciusLine(fig, t1, t2):
    plt.plot([t1, t2], [273.15, 273.15], c='c', label='0°C', lw='1.25', linestyle='dashed')
    fig = addLegend(fig, 'lower right', 'Extra lines:')
    return fig


# This function adds a legend to the figure at a specified position and with a given title
# The legend is also given an alpha value of 1.0 to make sure it not transparent as it is
# harder to read from a transparent legend.
def addLegend(fig, pos='lower right', title='Extra Lines: '):
    plt.legend(loc=pos, title=title, framealpha=1.0)
    return fig


# This method saves the figure with a given file name at a specific filepath.
# The dpi (dots-per-inch) determines how detailed the final saved image will be.
# The method also ensures that a plot is not saved with a name that already exists,
# If this were to happen then the first image would be overwritten
def savePlot(fig, filePath, fileName, dpi=1000):
    if input("Would you like to save this figure? (YES/NO): ").upper() == "YES":

        # Checking which fileName is available next in the directory in order to not overwrite existing plots
        i = 0
        while os.path.exists(f"{fileName}_{i}.png"):
            i += 1

        # Saving plot locally
        print("Saving to " + f"{fileName}_{i}.png")
        fig.savefig(filePath + f"{fileName}_{i}.png", dpi=dpi)
        print("Plot saved to " + f"{fileName}_{i}.png")


# This function converts between Astronomical Units and meters
def au_to_meters(x):
    return 149597870700 * x


# This function converts between meters and Astronomical Units
def meters_to_au(x):
    return x / 149597870700


# This function calculates the black-body radiant emittance
# This is how much energy per square metre (J/m^2) is radiated of a given body with a
# certain temperature
# More information: https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law
def PowerOut(T_body):
    return c.sigma * T_body ** 4


# This function calculates the planet's surface insolation by calculating the total energy radiated
# from the sun's surface and dividing it by the surface area the given planet
# More information: https://scied.ucar.edu/earth-system/planetary-energy-balance-temperature-calculate
def planetInsolation(Power_Output, R_star, d_planet):
    insolation = (4 * math.pi * R_star ** 2 * Power_Output) / (4 * math.pi * d_planet)
    return insolation


# This function does the same thing as planetInsolation() but instead takes the Temperature of the star as a parameter
def solarConstant(T_star, R_star, d_planet):
    insolation = (4 * math.pi * R_star ** 2 * PowerOut(T_star)) / (4 * math.pi * d_planet ** 2)
    return insolation


# This function calculates the incoming heat flux that passes through the atmosphere successfully
# By this I mean, all the energy that is not reflected by the atmosphere.
# This function splits the period into equally sized sections (periodFractions) which will act as timesteps.
# It calculates the the insolation accurately by using the provided Keplerian Ellipse.
def generate_heat_in(ke, periodFractions, d_planet, planetInsolation, albedo):
    heat_in = []
    period = d_planet ** (3 / 2)

    # Generating Heat_in coefficients
    for i in range(0, periodFractions):
        r = ke.radius(i / periodFractions * period)  # Applying Kepler's First Law to find r
        L = planetInsolation / (r / d_planet) ** 2  # Calculating insolation based on distance from star relative to semi major axis
        heat_in.append((L * (1 - albedo)) / 4)

    return heat_in


# This method uses NumPy to create a list from a starting number (inclusive) to the ending number
# (exclusive) by stepping through all the numbers in between
def generateList(start, end, step):
    e = np.arange(start, end, step).tolist()
    return e


# Obsolete method
def distance_of_planet_to_star(angle, semi_major_axis, e):
    return (semi_major_axis * (1 - e ** 2)) / (1 + e * math.cos(angle))


# This function smoothens out the transition between min and max albedo when the planet is hot/cold enough for water to change physical state
# Variables
# {Temp} is the Global Mean Temperature
# {T_i} is the threshold temperature below which the model assumes the planet is completely ice covered
# {T_o} is the threshold temperature above which our model assumes the planet is ice-free
# {alpha_o} is the albedo of a warm, ice-free planet
# {alpha_i} is the albedo of a very cold, completely ice-covered planet
# Source: https://brian-rose.github.io/ClimateLaboratoryBook/courseware/advanced-sensitivity-feedback.html
def smoothAlbedo_quadratic(Temp, T_i=260, T_o=293, alpha_o=0.289, alpha_i=0.7):
    if Temp <= T_i:
        return alpha_i
    elif T_i < Temp < T_o:
        return alpha_o + (alpha_i - alpha_o) * ((Temp - T_o) ** 2) / ((T_i - T_o) ** 2)
    else:
        return alpha_o


# This function performs linear interpolation to transition between min and max albedo
# This is an okay approximation however the approximation in smoothAlbedo_quadratic is better.
# Since the other function has been made, this function has become partly obsolete
# Variables
# {Temp} is the Global Mean Temperature
# {T_i} is the threshold temperature below which the model assumes the planet is completely ice covered
# {T_o} is the threshold temperature above which our model assumes the planet is ice-free
# {alpha_o} is the albedo of a warm, ice-free planet
# {alpha_i} is the albedo of a very cold, completely ice-covered planet
def smoothAlbedo_linear(Temp, T_i=260, T_o=293, alpha_o=0.289, alpha_i=0.7):
    if Temp < T_i:
        return alpha_i
    elif T_i <= Temp <= T_o:
        # ensures albedo transitions smoothly between min and max Albedo varying with temperature - This is linear interpolation
        return alpha_i - (alpha_i - alpha_o) * (Temp - T_i) / (T_o - T_i)
    else:
        return alpha_o


# Ratio of the area of the 'shadow' cast by the latitude band to the surface of revolution of the arc length of the latitude band
# Add more documentation here
def InOutRatio(latitude1, latitude2):
    theta1, theta2 = math.radians(latitude1), math.radians(latitude2)
    Surface_in = abs(theta1 - theta2 + 0.5 * (math.sin(2 * theta1) - math.sin(2 * theta2)))
    Surface_out = abs(2 * math.pi * (math.sin(theta1) - math.sin(theta2)))
    return Surface_in / Surface_out

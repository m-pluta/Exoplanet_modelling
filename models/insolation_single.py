from PyAstronomy import pyasl

from Utility import *


#  Sources: Kepler's First Law: https://www.vanderbilt.edu/AnS/physics/astrocourses/ast201/keplerslaws_1.html
#                               http://astronomy.nmsu.edu/nicole/teaching/ASTR505/lectures/lecture08/slide13.html#:~:text=The%20squares%20of%20the%20sidereal,square%20of%20its%20sidereal%20period.

def insolation_single(plotTitle, iterated, parsedE):
    if not iterated:
        e = float(input("Eccentricity: "))
    else:
        e = parsedE

    # Independent Variables
    R_star = c.R_Sun  # Radius of star (AU)
    d_planet = c.d_Earth  # Distance of planet from body it is orbiting  (AU)
    T_star = c.T_Sun  # (K)
    periodFractions = 1000  # fraction of period acts as timeStep

    # Initialisation
    period = math.pow(d_planet, 1.5)
    solar_Constant = solarConstant(T_star, R_star, d_planet)

    t = []
    L = []
    ke = pyasl.KeplerEllipse(d_planet, period, e, Omega=0., i=0.0, w=0.0)

    # Generating Data
    for i in range(periodFractions):
        t.append(((i / periodFractions) * period) * 365.25)
        r = ke.radius((i / periodFractions) * period)  # Applying Kepler's First Law to find r
        newL = solar_Constant / (r / d_planet) ** 2  # Calculating insolation based on position in orbit relative to the starting point
        L.append(newL)

    if not iterated:
        # Plotting data
        fig = plt.figure(plotTitle)
        plt.plot(t, L, c='r', linewidth=1.75)

        # Modifying Visual aspect of plot
        fig = beautifyPlot(fig, plotTitle + ' (e=' + str(e) + ')', 'time (days)', 'Light Insolation (W/m^2)')

        return fig
    else:
        return t, L

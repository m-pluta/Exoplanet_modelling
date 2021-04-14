import matplotlib.pyplot as plt

import c
from Utility import beautifyPlot
from Utility import plotCelciusLine


def zeroD_EBM():
    # Independent variables
    timeStep = 0.2  # (y)
    waterDepth = 4000  # (m)
    L = 1361  # (W / m^2)
    albedo = 0.3  # how much light gets reflected by atmosphere
    epsilon = 0.77  # how good of a blackbody the body is

    # Init
    heat_capacity = waterDepth * 1000 * 4200  # (J / K m^2)
    heat_in = (L * (1 - albedo)) / 4  # Watts/m^2
    t = [0]
    T = [0]

    # Generating Data
    heat_content = heat_capacity * T[0]  # (J / m^2)
    years = int(input('Number of years (1500): '))
    for i in range(int(years / timeStep)):
        heat_out = epsilon * c.sigma * pow(T[-1], 4)
        t.append(t[-1] + timeStep)
        heat_content += (heat_in - heat_out) * timeStep * c.SiY
        T.append(heat_content / heat_capacity)  # (K)

    # Plotting data
    plotTitle = '0D EBM without Greenhouse effect'
    fig = plt.figure(plotTitle)
    plt.plot(t, T, c='r', linewidth=1.75)

    # Modifying Visual aspect of plot
    fig = beautifyPlot(fig, plotTitle, 'time (years)', 'Surface temperature (K)')
    fig = plotCelciusLine(fig, t[0], t[-1])

    return fig

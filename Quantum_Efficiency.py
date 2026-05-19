from CXRO_Tools import Filter_Transmission
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

cxro = Filter_Transmission()

def QE_Interpolated_Function(x, min : float, max : float, Si_thickness : float, C_thickness : float, SiO2_thickness : float, Fe_thickness : float, step : float = 100):
    #Conversion from float to int to work between lmfit and cxro. lmfit sends floats.
    min=int(min)
    max=int(max)
    step=int(step)
    Si_cxro_data = cxro.get_transmission("Si", thickness = Si_thickness, energy_min=min, energy_max=max, steps=step)
    C_cxro_data = cxro.get_transmission("C", thickness= C_thickness, energy_min=min, energy_max=max, steps=step)
    SiO2_cxro_data = cxro.get_transmission("SiO2", thickness= SiO2_thickness, energy_min=min, energy_max=max, steps=step)
    Fe_cxro_data = cxro.get_transmission("Fe", thickness= Fe_thickness, energy_min=min, energy_max=max, steps=step)

    energies = np.array([i[0] for i in Si_cxro_data])
    Si_transmission = np.array([i[1] for i in Si_cxro_data])
    C_transmission = np.array([i[1] for i in C_cxro_data])
    SiO2_transmission = np.array([i[1] for i in SiO2_cxro_data])
    Fe_transmission = np.array([i[1] for i in Fe_cxro_data])

    QE = (1-Si_transmission) * C_transmission * SiO2_transmission * Fe_transmission
    interpolated_QE = interpolate.PchipInterpolator(energies, QE)

    return interpolated_QE(x)

if __name__ == "__main__":
    y = QE_Interpolated_Function(range(30, 2000, 50), 30, 2000, 5, 0.1, 0.1, 0.05, 100)
    test_range = range(30, 2000, 50)
    plt.plot(test_range, y)
    plt.show()
    
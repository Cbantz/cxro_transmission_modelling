from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from database_tools import add_database_item, get_formatted_filepath

def QE_Interpolated_Function(x, min : float, max : float, composition : list[dict], step : float = 100):
    #Conversion from float to int to work between lmfit and cxro. lmfit sends floats.
    min=int(min)
    max=int(max)
    step=int(step)


    detector_transmission_arrays = []
    other_transmission_arrays = []

    for i in composition:
        add_database_item(chemical_formula=i["Chemical Formula"], thickness=i["Thickness"], energy_min=min, energy_max=max, steps=step)
        i["cxro_data"] = np.load(get_formatted_filepath(chemical_formula=i["Chemical Formula"], thickness=i["Thickness"], energy_min=min, energy_max=max, steps=step))
        if i["is_detector"] == True:
            detector_transmission_arrays.append(i["cxro_data"][:,1])
        else:
            other_transmission_arrays.append(i["cxro_data"][:,1])






    energies = composition[0]["cxro_data"][:,0]


    detector_transmission = np.prod(detector_transmission_arrays, 0)
    other_transmission = np.prod(other_transmission_arrays, 0)
    QE = (1-detector_transmission) * other_transmission
    interpolated_QE = interpolate.PchipInterpolator(energies, QE)

    return interpolated_QE(x)

if __name__ == "__main__":
    min = 30
    max = 2000
    x = np.arange(80, 1200, 50)
    composition = [
        {"Chemical Formula" : "Si",
         "Thickness" : 1,
         "is_detector": True
        },
        {
         "Chemical Formula" : "SiO2",
         "Thickness" : 0.1,
         "is_detector": False
        }
    ]
    transmission = QE_Interpolated_Function(x, min, max, composition)
    plt.scatter(x, transmission)
    plt.show()


    
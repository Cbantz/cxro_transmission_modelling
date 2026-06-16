from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from collections.abc import Sequence
from database_tools import add_database_item, get_formatted_filepath
from Element_Layer import Element_Layer
from CXRO_Tools import get_transmission

def QE_Interpolated_Function(x, energy_min : float, energy_max : float, composition : Sequence[Element_Layer], steps : float = 100, use_database : bool = True):
    #Conversion from float to int to work between lmfit and cxro. lmfit sends floats.
    energy_min=int(energy_min)
    energy_max=int(energy_max)
    steps=int(steps)


    detector_transmission_arrays = []
    other_transmission_arrays = []

    for element in composition:
        if element.thickness == 0:
            continue # Don't do the rest of the for loop if no thickness
        if(use_database):
            add_database_item(chemical_formula=element.chemical_formula, thickness=element.thickness, energy_min=energy_min, energy_max=energy_max, steps=steps)
            element.cxro_data = np.load(get_formatted_filepath(chemical_formula=element.chemical_formula, thickness=element.thickness, energy_min=energy_min, energy_max=energy_max, steps=steps))
        else:
            element.cxro_data = np.array(get_transmission(chemical_formula=element.chemical_formula, thickness=element.thickness, energy_max=energy_max, energy_min=energy_min, steps=steps))
        if element.is_detector == True:
            detector_transmission_arrays.append(element.cxro_data[:,1])
        else:
            other_transmission_arrays.append(element.cxro_data[:,1])






    energies = composition[0].cxro_data[:,0]


    detector_transmission = np.prod(detector_transmission_arrays, 0)
    other_transmission = np.prod(other_transmission_arrays, 0)
    QE = (1-detector_transmission) * other_transmission
    interpolated_QE = interpolate.PchipInterpolator(energies, QE)

    return interpolated_QE(x)

if __name__ == "__main__":
    from time import process_time
    min = 30
    max = 2000
    x = np.arange(80, 1200, 50)
    composition = [
        Element_Layer(
            chemical_formula="Si",
            thickness=1,
            is_detector=True
        ),
        Element_Layer(
            chemical_formula="SiO2",
            thickness=0.1
        )
    ]
    start_time = process_time()
    transmission = QE_Interpolated_Function(x, min, max, composition)
    end_time = process_time()
    print(end_time-start_time)
    plt.scatter(x, transmission)
    plt.show()


    
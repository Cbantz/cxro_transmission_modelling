import numpy as np
import matplotlib.pyplot as plt
from Quantum_Efficiency_Local import QE_Interpolated_Function
from Element_Layer import Initial_Guess
import lmfit


def _build_function_(x, y, energy_min : int, energy_max : int, initial_guesses : list[Initial_Guess], should_round : bool, eff_pixel_size : float):
    """
    Generates an lmfit Model for the QE given your initial guesses.
    """
    def generated_QE_model(x, **kwargs):
        for guess in initial_guesses:
            if should_round:
                guess.thickness = np.round(kwargs[f"{guess.chemical_formula}_thickness"], guess.decimals) # this will always be able to pull an arg.
            else:
                guess.thickness = kwargs[f"{guess.chemical_formula}_thickness"]
        #eff_pixel_size = kwargs[f"eff_pixel_size"]
        return QE_Interpolated_Function(x, energy_min, energy_max, composition=initial_guesses, use_database=should_round, eff_pixel_size=eff_pixel_size)
    return generated_QE_model

def _make_params_(initial_guesses : list[Initial_Guess], eff_pixel_size : float):
    """
    This generates lmfit model parameters based on whatever intial guesses were added.
    """
    params = lmfit.Parameters()
    for element in initial_guesses:
        param_name = f"{element.chemical_formula}_thickness"
        parameter = lmfit.Parameter(name=param_name, value=element.thickness, vary=True, min=element.min_thickness, max=element.max_thickness)
        params.add(parameter)

    #params.add(lmfit.Parameter("eff_pixel_size", value=eff_pixel_size, vary=True, min=0, max=1))
    return params

def do_QE_fit(x, y, yerr, energy_min : int, energy_max : int, initial_guesses : list[Initial_Guess], fitting_method : str, eff_pixel_size : float = 1):
    # If using leastsq or another gradient-based method, turn off rounding. Can also use "differential_evolution" for gradient-less or "brute" for force-checking every combination. These two should have rounding turned on.
    rounding_needed_methods = ["differential_evolution", "brute"]
    no_rounding_methods = ["leastsq", "least_squares"]
    if fitting_method in rounding_needed_methods:
        should_round = True 
    elif fitting_method in no_rounding_methods:
        should_round = False
    model = lmfit.Model(_build_function_(x, y, energy_min, energy_max, initial_guesses, should_round, eff_pixel_size=eff_pixel_size))
    params = _make_params_(initial_guesses, eff_pixel_size)
    result = model.fit(data = y, params = params, x=x, weights = 1./yerr, method=fitting_method)
    return result

if __name__ == "__main__":
    """
    Running this script is how we have been fitting. in the initial_guesses_list list, you list whatever initial guesses you want,
    Each is an Initial_Guess object (see Element_Layer.py).
    """
    from time import process_time
    initial_guesses_list = [
    Initial_Guess(
        chemical_formula="Si",
        thickness=3.84, #Microns
        min_thickness=3.83,
        max_thickness=4.84,
        decimals=2,
        is_detector=True
    ),
    Initial_Guess(
        chemical_formula="SiO2",
        thickness=0.2,
        min_thickness=0,
        max_thickness=0.3,
        decimals=2
    ),
    Initial_Guess(
        chemical_formula="C7H10O3",
        thickness=1,
        min_thickness=.8,
        max_thickness=1.5,
        decimals=2
    )
    ]
    real_data = np.load("260520_CMOS-QE-Export.npy")
    x, y = real_data[0,3:], real_data[1,3:]
    yerr = real_data[2,3:]
    start_time = process_time()
    result : lmfit.model.ModelResult = do_QE_fit(x, y, yerr, 30, 2000, initial_guesses_list, "differential_evolution")
    end_time = process_time()
    print(f"Time to fit: {end_time-start_time} seconds")
    print(result.fit_report())
    plot = result.plot(show_init=True)
    plt.show()
    
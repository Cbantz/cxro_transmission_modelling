import numpy as np
import matplotlib.pyplot as plt
from Quantum_Efficiency_Local import QE_Interpolated_Function
from Element_Layer import Initial_Guess
import lmfit


def _build_function_(x, y, energy_min : int, energy_max : int, initial_guesses : list[Initial_Guess], should_round : bool):
    def generated_QE_model(x, **kwargs):
        for guess in initial_guesses:
            if should_round:
                guess.thickness = np.round(kwargs[f"{guess.chemical_formula}_thickness"], guess.decimals) # this will always be able to pull an arg.
            else:
                guess.thickness = kwargs[f"{guess.chemical_formula}_thickness"]
        return QE_Interpolated_Function(x, energy_min, energy_max, composition=initial_guesses, use_database=should_round)
    return generated_QE_model

def _make_params_(initial_guesses : list[Initial_Guess]):
    params = lmfit.Parameters()
    for element in initial_guesses:
        param_name = f"{element.chemical_formula}_thickness"
        parameter = lmfit.Parameter(name=param_name, value=element.thickness, vary=True, min=element.min_thickness, max=element.max_thickness)
        params.add(parameter)

    return params

def do_QE_fit(x, y, yerr, energy_min : int, energy_max : int, initial_guesses : list[Initial_Guess], fitting_method : str):
    # If using leastsq or another gradient-based method, turn off rounding. Can also use "differential_evolution" for gradient-less or "brute" for force-checking every combination. These two should have rounding turned on.
    rounding_needed_methods = ["differential_evolution", "brute"]
    no_rounding_methods = ["leastsq", "least_squares"]
    if fitting_method in rounding_needed_methods:
        should_round = True 
    elif fitting_method in no_rounding_methods:
        should_round = False
    model = lmfit.Model(_build_function_(x, y, energy_min, energy_max, initial_guesses, should_round))
    params = _make_params_(initial_guesses)
    result = model.fit(data = y, params = params, x=x, weights = 1./yerr, method=fitting_method)
    return result

if __name__ == "__main__":
    initial_guesses_list = [
    Initial_Guess(
        chemical_formula="Si",
        thickness=5,
        min_thickness=1,
        max_thickness=10,
        decimals=2,
        is_detector=True
    ),
    Initial_Guess(
        chemical_formula="SiO2",
        thickness=0.5,
        min_thickness=0.01,
        max_thickness=2,
        decimals=2
    ),
    Initial_Guess(
        chemical_formula="C7H10O3",
        thickness=0.5,
        min_thickness=0.01,
        max_thickness=2,
        decimals=2
    )
]
    real_data = np.load("260520_CMOS-QE-Export.npy")
    x, y = real_data[0,3:], real_data[1,3:]
    yerr = real_data[2,3:]
    result : lmfit.model.ModelResult = do_QE_fit(x, y, yerr, 30, 2000, initial_guesses_list, "differential_evolution")
    print(result.fit_report())
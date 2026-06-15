from CXRO_Tools import Filter_Transmission
import numpy as np
from pathlib import Path

cxro = Filter_Transmission()
def add_database_item(chemical_formula : str, thickness : float, energy_min : int, energy_max : int, steps : int = 100):

    filepath = get_formatted_filepath(chemical_formula=chemical_formula, thickness=thickness, energy_min=energy_min, energy_max=energy_max, steps=steps)

    if filepath.is_file():
        print(f"{filepath} already exists. Skipping.")
        return
    data = np.array(cxro.get_transmission(chemical_formula=chemical_formula, thickness=thickness, energy_max=energy_max, energy_min=energy_min, steps=steps))
    if data.size > 0:
        np.save(filepath, data)

    print(f"Saved array to {filepath}. Parameters: Chemical Formula = {chemical_formula}, Thickness = {thickness}μm, Energy Range: {energy_min}eV-{energy_max}eV, Steps: {steps}")
    return filepath

def get_formatted_filepath(chemical_formula : str, thickness : float, energy_min : int, energy_max : int, steps : int):
    thickness = float(thickness) #Do this so that there is a period after if a whole number is passed. Keeps consistency with file naming.
    save_dir = f"cxro_saved_data/{chemical_formula}_transmission/"
    thickness_str = str(thickness).replace(".", "p")
    file_name = f"{chemical_formula}_{thickness_str}_{energy_min}-{energy_max}ev_{steps}steps"
    filepath = Path(save_dir + file_name + ".npy")
    return filepath
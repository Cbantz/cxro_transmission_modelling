import numpy as np
from database_tools import add_database_item

class Element_Layer:

    def __init__(self, chemical_formula : str, thickness : float, is_detector : bool = False, surface_coverage : float = 1, steps : int = 100) -> None:
        self.chemical_formula = chemical_formula
        self.thickness = thickness
        self.is_detector = is_detector
        self.surface_coverage = surface_coverage
        self.steps = steps
        self.cxro_data : np.ndarray

class Initial_Guess(Element_Layer):
    
    def __init__(self, chemical_formula : str, thickness : float, min_thickness : float, max_thickness : float, decimals : int, is_detector : bool = False, surface_coverage : float = 1, steps : int = 100) -> None:
        super().__init__(chemical_formula, thickness, is_detector, surface_coverage, steps)
        self.min_thickness = min_thickness
        self.max_thickness = max_thickness
        self.decimals = decimals

        


        
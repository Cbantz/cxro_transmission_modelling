from PySide6.QtCore import QObject, Signal
from Quantum_Efficiency_Local import QE_Interpolated_Function
from Element_Layer import Element_Layer
from Layer_Options import Layer_Widget
import numpy as np

class Modeler(QObject):
    results = Signal(np.ndarray, np.ndarray)
    finished = Signal()
    def __init__(self, layer_list : list[Layer_Widget]):
        super().__init__()
        self.layer_widgets = layer_list


    def model(self):

        layers = self.make_layers_from_widgets()
        x,y = self.get_qe_data(layers)
        self.results.emit(x,y)
        self.finished.emit()


    def make_layers_from_widgets(self):
        element_layers = []
        for widget in self.layer_widgets:
            layer = Element_Layer(
                chemical_formula=widget.chemical_formula_entry.text(),
                thickness=float(widget.thickness_entry.value()),
                is_detector=widget.is_detector_box.isChecked()
            )
            element_layers.append(layer)
        return element_layers
    
    def get_qe_data(self, layers : list[Element_Layer]):

        energy_min = 30
        energy_max = 2000
        x = np.linspace(energy_min, energy_max, 1000)
        y = QE_Interpolated_Function(x, energy_min, energy_max, composition=layers)
        return x, y


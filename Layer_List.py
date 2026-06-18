from Layer_Options import Layer_Widget
from PySide6.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QPushButton, QCheckBox, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea

class Layer_List(QGroupBox):
    
    def __init__(self):
        super().__init__()
        self.setTitle("Layers")
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.active_layers : list[Layer_Widget] = []


        add_layer_button = QPushButton("Add Layer")
        add_layer_button.setFixedWidth(80)
        add_layer_button.setCheckable(False)
        add_layer_button.pressed.connect(self.add_layer)

        self.show_fitting_parameters_check = QCheckBox()
        self.show_fitting_parameters_check.stateChanged.connect(self.show_fitting_options)
        show_fitting_parameters_form = QFormLayout()
        show_fitting_parameters_form.addRow("Fitting Options: ", self.show_fitting_parameters_check)

        top_options_layout = QHBoxLayout()
        top_options_layout.addWidget(add_layer_button)
        top_options_layout.addSpacerItem(QSpacerItem(50, 0))
        top_options_layout.addLayout(show_fitting_parameters_form)
    

        self.vlayout.addLayout(top_options_layout)

        self.list_widget = QFrame()
        
        self.layer_list_layout = QVBoxLayout()
        self.layer_list_layout.addStretch()
        self.list_widget.setLayout(self.layer_list_layout)

        layer_list_area = QScrollArea()
        
        layer_list_area.setWidgetResizable(True)
        layer_list_area.setWidget(self.list_widget)
        
        self.vlayout.addWidget(layer_list_area)

        self.plot_QE_from_layers_button = QPushButton("Plot!")

        self.vlayout.addWidget(self.plot_QE_from_layers_button)
        

        
        


        


     


    def add_layer(self, chemical_formula : str = "", thickness : float = 0.0, is_detector = False):
        new_layer = Layer_Widget()
        self.layer_list_layout.insertWidget(0, new_layer)
        new_layer.set_chemical_formula(chemical_formula)
        new_layer.set_thickness(thickness)
        new_layer.set_is_detector(is_detector)
        new_layer.set_fitting_options_visible(self.show_fitting_parameters_check.isChecked())
        
        self.active_layers.append(new_layer)
        new_layer.delete_button.clicked.connect(lambda: self.remove_layer(new_layer))
        

        

    def remove_layer(self, layer_to_remove):
        self.vlayout.removeWidget(layer_to_remove)
        self.active_layers.remove(layer_to_remove)
        layer_to_remove.deleteLater()

    def show_fitting_options(self):
        for layer in self.active_layers:
            layer.set_fitting_options_visible(self.show_fitting_parameters_check.isChecked())



if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication()
    widget = Layer_List()
    widget.add_layer("Si", 3, True)
    widget.add_layer("SiO2", 0.2, False)
    widget.show()
    app.exec()
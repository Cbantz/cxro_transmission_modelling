from PySide6.QtWidgets import QPushButton, QLineEdit, QDoubleSpinBox, QHBoxLayout, QLabel, QFormLayout, QVBoxLayout, QFrame, QCheckBox, QSizePolicy, QSpinBox

class Layer_Widget(QFrame):
    def __init__(self):
        super().__init__()
        
        
        core_options_form_layout = QFormLayout()
        #CHEMICAL FORMULA ENTRY
        self.chemical_formula_entry = QLineEdit()
        core_options_form_layout.addRow("Chemical Formula: ", self.chemical_formula_entry)

        #THICKNESS ENTRY
        self.thickness_entry = QDoubleSpinBox(singleStep=0.01)
        core_options_form_layout.addRow("Thickness: ", self.thickness_entry)
        self.thickness_entry.focusPolicy


        #IS_DETECTOR
        self.is_detector_box = QCheckBox()
        core_options_form_layout.addRow("Is Detector: ", self.is_detector_box)

        #DELETE BUTTON
        self.delete_button = QPushButton("Delete Layer")
        self.delete_button.setCheckable(False)
        self.delete_button.setFixedWidth(80)
        

        #FITTING OPTIONS
        self.fitting_options = QFrame()
        fitting_form = QFormLayout()

        #Decimals
        self.decimal_entry = QSpinBox(value=2, singleStep=1, minimum=0, maximum=4)
        self.decimal_entry.valueChanged.connect(self._decimal_changed_)
        fitting_form.addRow("Decimals to Use: ", self.decimal_entry)

        #Min/Max thickness
        self.min_thickness_entry = QDoubleSpinBox(value=0.00, singleStep=0.01, minimum=0, decimals=2)
        fitting_form.addRow("Minimum Thickness: ", self.min_thickness_entry)
        self.min_thickness_entry.valueChanged.connect(self._min_thickness_changed_)

        self.max_thickness_entry = QDoubleSpinBox(value=1.00, singleStep=0.01, minimum=0, decimals=2)
        fitting_form.addRow("Maximum Thickness: ", self.max_thickness_entry)
        self.max_thickness_entry.valueChanged.connect(self._max_thickness_changed_)

        self.fitting_options.setLayout(fitting_form)

        
        self.fitting_options.setVisible(False)



        
        vlayout = QVBoxLayout()
        vlayout.addLayout(core_options_form_layout)
        vlayout.addWidget(self.delete_button)
        vlayout.addWidget(self.fitting_options)
        

        


        

        self.setLayout(vlayout)



        self.setStyleSheet(".Layer_Widget { background-color: darkslategray; border: 1px solid gray; }")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)







    def set_chemical_formula(self, chemical_formula : str):
        self.chemical_formula_entry.setText(chemical_formula)

    def set_thickness(self, thickness : float):
        self.thickness_entry.setValue(thickness)

    def set_is_detector(self, is_detector : bool):
        self.is_detector_box.setChecked(is_detector)

    def set_fitting_options_visible(self, visible: bool):
        self.fitting_options.setVisible(visible)

    def _min_thickness_changed_(self):
        self.max_thickness_entry.setMinimum(self.min_thickness_entry.value())

    def _max_thickness_changed_(self):
        self.min_thickness_entry.setMaximum(self.max_thickness_entry.value())

    def _decimal_changed_(self):
        decimals = self.decimal_entry.value()
        stepsize = 10**(-decimals)
        self.max_thickness_entry.setDecimals(decimals)
        self.min_thickness_entry.setDecimals(decimals)
        self.max_thickness_entry.setSingleStep(stepsize)
        self.min_thickness_entry.setSingleStep(stepsize)

        


            

class advanced_Line(QHBoxLayout):
    def __init__(self) -> None:
        super().__init__()
        
        self.parameters_visibility_button = QPushButton("▶")
        self.parameters_visibility_button.setFixedWidth(30)
        self.parameters_visibility_button.setStyleSheet("""
            QPushButton {
            background-color: transparent;
            background: transparent;
            border: none;
            padding: 0px;
            }
            QPushButton:hover {
                background-color: transparent; 
                color: #555555;                
            }
            QPushButton:pressed {
                background-color: transparent;
            }
                                                        """)
        
        self.addWidget(QLabel("Fitting Parameters"))
        self.addWidget(self.parameters_visibility_button)


        




if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    widget = Layer_Widget()
    widget.show()
    app.exec()

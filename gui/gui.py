from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QHBoxLayout
from PySide6.QtCore import QSize, Qt, Signal, QThread
from Layer_List import Layer_List
from qegraph import QE_Graph_Widget
from Layer_Options import Layer_Widget
from Element_Layer import Initial_Guess
from fitting import do_QE_fit
from Quantum_Efficiency_Local import QE_Interpolated_Function
from modeler import Modeler







app = QApplication()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        interface = QWidget()
        interface_layout = QHBoxLayout()
        self.layer_list = Layer_List()
        self.layer_list.add_layer("Si", 1, is_detector=True)
        self.graph_widget = QE_Graph_Widget()

        interface_layout.addWidget(self.layer_list)
        interface_layout.addWidget(self.graph_widget)

        self.layer_list.plot_QE_from_layers_button.clicked.connect(lambda: self.graph_widget.model_qe(self.layer_list.active_layers))

        interface.setLayout(interface_layout)

        self.setCentralWidget(interface)





    def print_results(self, results):
        print(results)






main_window = MainWindow()
main_window.show()

app.exec()

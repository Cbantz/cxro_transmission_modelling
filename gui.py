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

        self.layer_list.plot_QE_from_layers_button.clicked.connect(self.model_qe)

        interface.setLayout(interface_layout)

        self.setCentralWidget(interface)




    def model_qe(self):
        
        self.modeling_thread = QThread()
        self.modeler = Modeler(self.layer_list.active_layers)

        self.modeler.moveToThread(self.modeling_thread)

        self.modeling_thread.started.connect(self.modeler.model)

        self.modeler.results.connect(self.graph_widget.plot_modeled_qe)

        self.modeler.finished.connect(self.modeling_thread.quit)
        self.modeler.finished.connect(self.modeler.deleteLater)
        self.modeling_thread.finished.connect(self.modeling_thread.deleteLater)

        self.modeling_thread.start()

    def print_results(self, results):
        print(results)






main_window = MainWindow()
main_window.show()

app.exec()

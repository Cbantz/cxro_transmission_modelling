from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class QE_Graph_Widget(QGroupBox):

    def __init__(self, parent=None, width=10, height=10, dpi=100):
        super().__init__()

        
        #GRAPH
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.graph = FigureCanvasQTAgg(fig)
        self.graph.main_axes = fig.add_subplot(3, 1, (1,2))
        self.graph.main_axes.set_ylabel("Quantum Efficiency")
        self.graph.main_axes.tick_params('x', labelbottom=False)

        
        self.graph.residual_axes = fig.add_subplot(3, 1, 3, sharex=self.graph.main_axes)
        self.graph.residual_axes.set_xlabel("Energy (eV)")
        
        self.graph.residual_axes.set_ylabel("Residual")

        self.graph.main_axes.plot([0,1,2,3,4], [10,1,20,3,40])

        vlayout = QVBoxLayout()
        
        vlayout.addWidget(self.graph)
        self.setLayout(vlayout)

    def plot_modeled_qe(self, x, y):
        self.graph.main_axes.cla()
        self.graph.main_axes.plot(x, y)
        self.graph.main_axes.set_ylabel("Quantum Efficiency")
        self.graph.main_axes.tick_params('x', labelbottom=False)
        self.graph.main_axes.set_xlim(min(x), max(x))
        self.graph.main_axes.set_ylim(0,1)
        self.graph.main_axes.autoscale_view()
        self.graph.residual_axes.relim()
        self.graph.residual_axes.autoscale_view()
        self.graph.draw()

        

    


















if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    widget = QE_Graph_Widget()
    
    widget.show()
    app.exec()





    




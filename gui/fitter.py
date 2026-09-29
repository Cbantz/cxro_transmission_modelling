from PySide6.QtCore import QObject, Signal
import lmfit

class Fitter(QObject):
    fit_result = Signal(lmfit.model.ModelResult)
    finished = Signal()
    def __init__(self) -> None:
        super().__init__()




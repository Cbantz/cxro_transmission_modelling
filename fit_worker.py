from PySide6.QtCore import QObject, Signal
import lmfit

class Fit_Worker(QObject):
    fit_result = Signal(lmfit.model.ModelResult)
    def __init__(self) -> None:
        super().__init__()




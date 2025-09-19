# PerfilWindow.py
import sys
from pathlib import Path

# Ajustar sys.path para importar desde la raíz (si lo necesitas)
BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt

class Perfil_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("PerfilWindow")
        self.setStyleSheet("background-color: #CCE7ED;")
        # Usa layouts si vas a crecer; por ahora, simple:
        self.lbl = QLabel("Perfil del usuario (WIP)", self)
        self.lbl.setGeometry(30, 30, 400, 30)
        self.lbl.setStyleSheet(
            'font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui; '
            "font-size: 18px; color: #1f2937; font-weight: bold;"
        )
        self.setMinimumSize(900, 500)

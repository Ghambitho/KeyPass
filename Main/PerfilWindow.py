import sys
from pathlib import Path

# Ajustar sys.path para importar desde la raíz del proyecto
BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QToolButton, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea, QApplication, 
    QFrame, QStackedWidget, QGraphicsDropShadowEffect, QCheckBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor

class Perfil_Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("PerfilWindow")
        self.setStyleSheet("background-color: #FEFEFE;")
        self.setGeometry(20, 30, 900, 500)

        self.perfil = QLabel("Profile Settings", self)
        self.perfil.setGeometry(40, 30, 250, 50)
        self.perfil.setStyleSheet("""
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui;
            font-size: 28px; 
            color: #1f2937; 
            font-weight: bold;

        """)
    
        self.input_name = QLineEdit(self)
        self.input_name.setGeometry(40, 250, 250, 50)
        self.input_name.setPlaceholderText("Name")
        self.input_name.setStyleSheet("""
            border: 3px solid #D4D2D2;
            border-radius: 10px;
            color: #111111;
            font-family: Helvetica;
            font-size: 18px;
            padding: 10px;
        """) 

        self.input_name = QLineEdit(self)
        self.input_name.setGeometry(40, 310, 250, 50)
        self.input_name.setPlaceholderText("Email")
        self.input_name.setStyleSheet("""
            border: 3px solid #D4D2D2;
            border-radius: 10px;
            color: #111111;
            font-family: Helvetica;
            font-size: 18px;
            padding: 10px;
        """)

        self.noti_check = QCheckBox("Email notifications", self)
        self.noti_check.setGeometry(40, 370, 370, 50)
        self.noti_check.setStyleSheet("""
            QCheckBox {
                color: Black;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 3px solid #e2e8f0;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:hover {
                border-color: #3182ce;
                background-color: #f7fafc;
            }
            QCheckBox::indicator:checked {
                background-color: #041D42;
                border-color: #102A52;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #102A52;
            }
        """)

        self.savebton = QPushButton("Save change", self)
        self.savebton.setGeometry(40, 430, 150, 50)
        self.savebton.setStyleSheet("""
            QPushButton {
                background: #366CF0;
                border-radius: 10px;
                border: none;
                font-family: Helvetica; font-size: 20px;
                color: white;
            }
            """)
        self.savebton = QPushButton("Export password", self)
        self.savebton.setGeometry(220, 430, 170, 50)
        self.savebton.setStyleSheet("""
            QPushButton {
                background: #366CF0;
                border-radius: 10px;
                border: none;
                font-family: Helvetica; font-size: 20px;
                color: white;
            }
            """)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Perfil_Window()
    w.show()
    sys.exit(app.exec())
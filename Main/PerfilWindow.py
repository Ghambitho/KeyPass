import sys
from pathlib import Path
import sqlite3
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
from Logic.session import load_session
from Logic.login import get_user_profile, update_user_profile
from Logic.storage import _load_all_passwords
import csv
from datetime import datetime

class Perfil_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("PerfilWindow")
        self.setStyleSheet("background-color: #FEFEFE;")
        self.setGeometry(20, 30, 900, 500)

        # Inicializar variables
        self.user_id = None
        self.usuario = "N/A"
        self.email = "N/A"

        estilo_boton = """
                    QPushButton {
                        background: #366CF0;
                        border-radius: 10px;
                        border: none;
                        font-family: Helvetica; font-size: 20px;
                        color: white;
                    }
                    QPushButton:hover {
                        background: #305DC9;
                    }
                    QPushButton:pressed {
                        background: #051B33;
                        color: white;
                    }
                    """

        self.user_name_label = QLabel(self.usuario, self)
        self.user_name_label.setGeometry(450, 120, 200, 30)
        self.user_name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1f2937;")

        self.user_email_label = QPushButton(self.email, self)
        self.user_email_label.setGeometry(320, 250, 300, 50)
        self.user_email_label.setStyleSheet(estilo_boton)
      

        self.perfil = QLabel("Profile Settings", self)
        self.perfil.setGeometry(40, 30, 250, 50)
        self.perfil.setStyleSheet("""
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui;
            font-size: 28px; 
            color: #1f2937; 
            font-weight: bold;
            background: transparent;
        """)
        
        self.config = QLabel("Change settings", self)
        self.config.setGeometry(40, 130, 200, 50)
        self.config.setStyleSheet("""
            QLabel {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui;
                color: black;
                font-size: 20px;
                font-weight: bold;
                background: transparent;                
            }
        """)
       #estilo de QlineEdit
        estiloline_styleSheet ="""
            border: 3px solid #D4D2D2;
            border-radius: 10px;
            color: #111111;
            font-family: Helvetica;
            font-size: 18px;
            padding: 10px;
        """
        self.input_name = QLineEdit(self)
        self.input_name.setGeometry(40, 190, 250, 50)
        self.input_name.setPlaceholderText(self.usuario)  # Mostrar el nombre actual
        self.input_name.setStyleSheet(estiloline_styleSheet)

        self.input_email = QLineEdit(self)
        self.input_email.setGeometry(40, 250, 250, 50)
        self.input_email.setPlaceholderText(self.email)
        self.input_email.setStyleSheet(estiloline_styleSheet)
        
        self.input_pass = QLineEdit(self)
        self.input_pass.setGeometry(40, 310, 250, 50)
        self.input_pass.setPlaceholderText("Password")
        self.input_pass.setStyleSheet(estiloline_styleSheet)

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

        #Estilo de botones

        
        self.savebton = QPushButton("Save change", self)
        self.savebton.setGeometry(40, 430, 150, 50)
        self.savebton.setStyleSheet(estilo_boton)
        self.savebton.clicked.connect(self.save_changes)
        
        self.exportbton = QPushButton("Export password", self)
        self.exportbton.setGeometry(220, 430, 170, 50)
        self.exportbton.setStyleSheet(estilo_boton)
           
        self.exportbton.clicked.connect(self.export_passwords)
    
    def set_current_user(self, user_id):
        """Establece el usuario actual y carga sus datos"""
        self.user_id = user_id
        self._load_user_data()
        self._update_display()
    
    def showEvent(self, event):
        """Se ejecuta cada vez que se muestra la ventana"""
        super().showEvent(event)
        # Si no hay user_id establecido, intentar cargar desde sesión
        if self.user_id is None:
            self._load_user_data_from_session()
            self._update_display()
        
    def _load_user_data(self):
        """Carga los datos del usuario actual usando self.user_id"""
        if self.user_id:
            data = get_user_profile(self.user_id)
            self.email, self.usuario = data if data else ("N/A", "N/A")
        else:
            self.usuario, self.email = "N/A", "N/A"
    
    def _load_user_data_from_session(self):
        """Carga los datos desde la sesión (fallback)"""
        payload = load_session()
        if payload:
            self.user_id = payload["user"]
            data = get_user_profile(self.user_id)
            self.email, self.usuario = data if data else ("N/A", "N/A")
        else:
            self.user_id = None
            self.usuario, self.email = "N/A", "N/A"
    
    def _update_display(self):
        """Actualiza la interfaz con los datos del usuario actual"""
        self.user_name_label.setText(self.usuario)
        self.user_email_label.setText(self.email)
        self.input_name.setPlaceholderText(self.usuario)
        self.input_email.setPlaceholderText(self.email)
        
    def save_changes(self):
        """Guarda los cambios del perfil del usuario"""
        new_name = self.input_name.text().strip()
        new_email = self.input_email.text().strip()
        
        # Validaciones simples
        if not new_name or not new_email:
            self._show_message("Error: Nombre y email son requeridos", "error")
            return
            
        if not self._valid_email(new_email):
            self._show_message("Error: Formato de email inválido", "error")
            return
            
        # Guardar y mostrar resultado
        if update_user_profile(self.user_id, new_email, new_name):
            self._show_message("Perfil actualizado correctamente", "success")
            self.user_name_label.setText(new_name)
            self.user_email_label.setText(new_email)
        else:
            self._show_message("Error: Email/usuario ya está en uso", "error")
    
    def _valid_email(self, email: str) -> bool:
        """Valida formato básico de email"""
        return "@" in email and "." in email.split("@")[1]
    
    def _show_message(self, text: str, msg_type: str = "info"):
        """Muestra un mensaje al usuario"""
        if not hasattr(self, 'msg_label'):
            self.msg_label = QLabel(self)
            self.msg_label.setGeometry(40, 480, 400, 20)
        
        # Colores simples
        colors = {"error": "#B91C1C", "success": "#065F46", "info": "#6B7280"}
        self.msg_label.setStyleSheet(f"font-size: 14px; color: {colors[msg_type]};")
        self.msg_label.setText(text)
        self.msg_label.show()
        
    def export_passwords(self):
        """Exporta las contraseñas del usuario a un archivo CSV"""
        if not self.user_id:
            self._show_message("Error: Usuario no identificado", "error")
            return
            
        passwords = _load_all_passwords(self.user_id)
        if not passwords:
            self._show_message("No hay contraseñas guardadas", "info")
            return
        
        # Crear archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"keypass_export_{timestamp}.csv"
        
        # Escribir CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Sitio', 'Usuario', 'Contraseña'])
            writer.writeheader()
            for pwd in passwords:
                writer.writerow({
                    'Sitio': pwd.get('sitio', ''),
                    'Usuario': pwd.get('usuario', ''),
                    'Contraseña': pwd.get('contraseña', '')
                })
        
        self._show_message(f"Contraseñas exportadas a: {filename}", "success")

def mostrar_perfil(self):
    # Cargar datos de perfil del usuario activo (si existe)
    if self.current_user_id is not None:
        try:
            prof = get_user_profile(self.current_user_id)  # (email, usuario)
            if prof and hasattr(self.perfil_widget, "set_profile"):
                email, usuario = prof
                self.perfil_widget.set_profile(user_id=self.current_user_id, email=email, usuario=usuario)
        except Exception:
            pass
    self.stack.setCurrentWidget(self.perfil_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Perfil_Window()
    w.show()
    sys.exit(app.exec())
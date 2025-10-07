# -*- coding: utf-8 -*-
import sys

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFrame, QApplication, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from client.Logic.session import load_session, clear_session
from backend.Logic.login import get_user_profile
from backend.Logic.storage import _load_all_passwords
import csv
from datetime import datetime

class Perfil_Window(QWidget):
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #FAFAFA; font-family: Helvetica;")
        
        # Variables
        self.user_id = None
        self.usuario = "N/A"
        self.email = "N/A"
        
        

        # Frame principal de la tarjeta
        card = QFrame(self)
        card.setGeometry(210, 20, 480, 520)
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #E5E7EB;
                border-radius: 20px;
            }
        """)
        # Título
        self.title = QLabel("Profile Settings", self)
        self.title.setGeometry(300, 10, 300, 40)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; color: #1f2937; background: white; border: 2px solid #e5e7eb; border-radius: 12px;")
        
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(shadow)

        # Avatar
        self.avatar = QLabel("👤", card)
        self.avatar.setGeometry(180, 30, 120, 120)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setStyleSheet("""
            QLabel {
                font-size: 70px;
                background: #F3F4F6;
                border-radius: 60px;
                border: 3px solid #E5E7EB;
            }
        """)

        # Frame de información del usuario
        info_frame = QFrame(card)
        info_frame.setGeometry(40, 170, 400, 120)
        info_frame.setStyleSheet("""
            QFrame {
                background: #F9FAFB;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)

        # Username
        username_title = QLabel("USERNAME", info_frame)
        username_title.setGeometry(20, 15, 100, 20)
        username_title.setStyleSheet("""
        font-size: 12px; 
        font-weight: bold; 
        bold; color: #000000; 
        border: none;
        """)
        
        self.username_label = QLabel("Loading...", info_frame)
        self.username_label.setGeometry(20, 35, 360, 25)
        self.username_label.setStyleSheet("""
        font-size: 18px; 
        color: #6B7280;
        border: none;
        """)

        # Email
        email_title = QLabel("EMAIL ADDRESS", info_frame)
        email_title.setGeometry(20, 65, 120, 20)
        email_title.setStyleSheet("""
        font-size: 12px; 
        font-weight: bold; 
        bold; color: #000000; 
        border: none;
        """)
        
        self.email_label = QLabel("Loading...", info_frame)
        self.email_label.setGeometry(20, 85, 360, 25)
        self.email_label.setStyleSheet("""
        font-size: 18px; 
        color: #6B7280;
        border: none;
        """)

        # Estadísticas - Contraseñas guardadas
        passwords_card = QFrame(card)
        passwords_card.setGeometry(40, 310, 190, 80)
        passwords_card.setStyleSheet("""
            QFrame {
                background: #F9FAFB;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)
        
       
        
        passwords_title = QLabel("Saved Passwords", passwords_card)
        passwords_title.setGeometry(10, 15, 140, 20)
        passwords_title.setStyleSheet("""
        font-size: 18px; 
        color: #6B7280;
        border: none;
        """)
        
        self.passwords_count = QLabel("0", passwords_card)
        self.passwords_count.setGeometry(15, 45, 160, 25)
        self.passwords_count.setStyleSheet("""
        font-size: 20px; 
        font-weight: bold; 
        bold; color: #000000; 
        border: none;
        """)

        # Estadísticas - Miembro desde
        member_card = QFrame(card)
        member_card.setGeometry(250, 310, 190, 80)
        member_card.setStyleSheet("""
            QFrame {
                background: #F9FAFB;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)
        
        member_title = QLabel("Member Since", member_card)
        member_title.setGeometry(10, 15, 140, 20)
        member_title.setStyleSheet("""
        font-size: 18px; 
        color: #6B7280;
        border: none;
        """)
        
        self.member_since = QLabel("Today", member_card)
        self.member_since.setGeometry(15, 45, 160, 25)
        self.member_since.setStyleSheet("""
        font-size: 20px; 
        font-weight: bold; 
        bold; color: #000000; 
        border: none;
        """)
        # Botón Export
        self.export_btn = QPushButton("Export Passwords", card)
        self.export_btn.setGeometry(40, 420, 180, 50)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background: #366CF0;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background: #2563EB; }
            QPushButton:pressed { background: #1D4ED8; }
        """)
        self.export_btn.clicked.connect(self.export_passwords)

        # Botón Logout
        self.logout_btn = QPushButton("Logout", card)
        self.logout_btn.setGeometry(250, 420, 120, 50)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background: #EF4444;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background: #DC2626; }
            QPushButton:pressed { background: #B91C1C; }
        """)
        self.logout_btn.clicked.connect(self.logout)

        # Mensajes
        self.msg_label = QLabel("", self)
        self.msg_label.setGeometry(50, 520, 800, 30)
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setStyleSheet("font-size: 14px; color: #6B7280;")

    def logout(self):
        """Maneja el logout"""
        try:
            clear_session()
        except Exception:
            pass
        self.logout_requested.emit()

    def showEvent(self, event):
        """Se ejecuta cuando se muestra la ventana"""
        super().showEvent(event)
        # Siempre recargar los datos de la sesión para mostrar el usuario actual
        self._load_user_data_from_session()
        self._update_display()
        
    def _load_user_data_from_session(self):
        """Carga los datos desde la sesión"""
        payload = load_session()
        if payload:
            self.user_id = payload["user"]
            data = get_user_profile(self.user_id)
            self.email, self.usuario = data if data else ("N/A", "N/A")
        else:
            self.user_id = None
            self.usuario, self.email = "N/A", "N/A"
    
    def _update_display(self):
        """Actualiza la interfaz con los datos del usuario"""
        self.username_label.setText(self.usuario)
        self.email_label.setText(self.email)
        
        # Actualizar contador de contraseñas
        if self.user_id:
            try:
                passwords = _load_all_passwords(self.user_id)
                count = len(passwords) if passwords else 0
                self.passwords_count.setText(str(count))
            except Exception:
                self.passwords_count.setText("0")
        else:
            self.passwords_count.setText("0")

    def _show_message(self, text: str, msg_type: str = "info"):
        """Muestra un mensaje al usuario"""
        colors = {"error": "#EF4444", "success": "#10B981", "info": "#6B7280"}
        self.msg_label.setStyleSheet(f"font-size: 14px; color: {colors[msg_type]};")
        self.msg_label.setText(text)
        self.msg_label.show()
        
    def export_passwords(self):
        """Exporta las contraseñas a CSV"""
        if not self.user_id:
            self._show_message("Error: Usuario no identificado", "error")
            return
            
        try:
            passwords = _load_all_passwords(self.user_id)
            if not passwords:
                self._show_message("No hay contraseñas guardadas", "info")
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"keypass_export_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Sitio', 'Usuario', 'Contraseña'])
                writer.writeheader()
                for pwd in passwords:
                    writer.writerow({
                        'Sitio': pwd.get('sitio', ''),
                        'Usuario': pwd.get('usuario', ''),
                        'Contraseña': pwd.get('contraseña', '')
                    })
            
            self._show_message(f"Exportado: {filename}", "success")
            self._update_display()
            
        except Exception as e:
            self._show_message(f"Error: {str(e)}", "error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Perfil_Window()
    w.show()
    sys.exit(app.exec())
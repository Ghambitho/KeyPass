# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QFrame, QGraphicsDropShadowEffect
)
from Logic.login import create_user, user_exists
from Logic.session import save_session

class SignupView(QWidget):
    registered = pyqtSignal(int)
    back_to_login = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(900, 600)
        self._create_ui()
        self._connect_events()

    def _create_ui(self):
        """Crea la interfaz de usuario"""
        self.setStyleSheet("""
            QWidget {
                background: #FAFAFA;
                font-family: Helvetica;
            }
        """)

        # Layout principal
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 10, 0, 40)
        root.setSpacing(0)

        # Contenedor centrado
        container_layout = QHBoxLayout()
        container_layout.addStretch(1)
        
        # Card de registro
        self.signup_card = self._create_signup_card()
        container_layout.addWidget(self.signup_card, 0, Qt.AlignmentFlag.AlignCenter)
        
        container_layout.addStretch(1)
        root.addLayout(container_layout)

    def _create_signup_card(self):
        """Crea la tarjeta de registro"""
        card = QFrame(self)
        card.setObjectName("card")
        card.setFixedWidth(560)
        card.setStyleSheet("""
            QFrame#card {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
        """)
        
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(36)
        shadow.setXOffset(0)
        shadow.setYOffset(14)
        shadow.setColor(QColor(0, 0, 0, 45))
        card.setGraphicsEffect(shadow)

        # Layout interno
        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 32, 32, 24)
        cl.setSpacing(16)

        # Título
        self.title = QLabel("Create Account", card)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: 800;
                color: black;
                background: transparent;
            }
        """)
        cl.addWidget(self.title)

        # Campo username
        self.input_name = QLineEdit(card)
        self.input_name.setPlaceholderText("Username")
        self.input_name.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 14px 16px;
                color: black;
                font-size: 16px;
            }
            QLineEdit:focus { border: 1px solid #366CF0; }
        """)
        cl.addWidget(self.input_name)

        # Campo email
        self.input_email = QLineEdit(card)
        self.input_email.setPlaceholderText("Email Address")
        self.input_email.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 14px 16px;
                color: black;
                font-size: 16px;
            }
            QLineEdit:focus { border: 1px solid #366CF0; }
        """)
        cl.addWidget(self.input_email)

        # Campo contraseña
        self.input_pw = QLineEdit(card)
        self.input_pw.setPlaceholderText("Password")
        self.input_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pw.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px 8px;
                font-size: 16px;
                color: black;
            }
            QLineEdit:focus { border: 1px solid #366CF0; }
        """)
        cl.addWidget(self.input_pw)

        # Campo confirmar contraseña
        self.input_pw_confirm = QLineEdit(card)
        self.input_pw_confirm.setPlaceholderText("Confirm Password")
        self.input_pw_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pw_confirm.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px 8px;
                font-size: 16px;
                color: black;
            }
            QLineEdit:focus { border: 1px solid #366CF0; }
        """)
        cl.addWidget(self.input_pw_confirm)

        # Checkbox términos
        self.terms = QCheckBox("I agree to the Terms and Conditions", card)
        self.terms.setStyleSheet("""
            QCheckBox {
                background: transparent;
                color: #111827;
                font-size: 15px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #D1D5DB;
                border-radius: 5px;
                background: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background: #366CF0;
                border-color: #366CF0;
            }
        """)
        cl.addWidget(self.terms)

        # Botón signup
        self.btn_signup = QPushButton("Sign Up", card)
        self.btn_signup.setStyleSheet("""
            QPushButton {
                background: #366CF0;
                border: 1px solid #D1D5DB;
                color: white;
                border-radius: 12px;
                padding: 14px 16px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover { background: #3964CC; }
            QPushButton:pressed { background: #001F69; }
        """)
        cl.addWidget(self.btn_signup)

        # Link de login
        self.link_login = QPushButton("Already have an account? Sign In", card)
        self.link_login.setStyleSheet(
            "QPushButton { border:none; background:transparent; color:#366CF0; font-size:14px; }"
            "QPushButton:hover { text-decoration: underline; }"
        )
        cl.addWidget(self.link_login, 0, Qt.AlignmentFlag.AlignLeft)

        # Mensajes
        self.msg = QLabel("", card)
        self.msg.setWordWrap(True)
        cl.addWidget(self.msg)

        return card

    def _connect_events(self):
        """Conecta los eventos"""
        self.btn_signup.clicked.connect(self._do_signup)
        self.link_login.clicked.connect(self.back_to_login.emit)

        # Enter para enviar
        self.input_name.returnPressed.connect(self._do_signup)
        self.input_email.returnPressed.connect(self._do_signup)
        self.input_pw.returnPressed.connect(self._do_signup)
        self.input_pw_confirm.returnPressed.connect(self._do_signup)

    def _info(self, text: str):
        """Muestra información"""
        self.msg.setStyleSheet("color:#6B7280;")
        self.msg.setText(text)

    def _error(self, text: str):
        """Muestra error"""
        self.msg.setStyleSheet("color:#B91C1C;")
        self.msg.setText(text)

    def _success(self, text: str):
        """Muestra éxito"""
        self.msg.setStyleSheet("color:#065F46;")
        self.msg.setText(text)

    def _valid_email(self, email: str) -> bool:
        """Validación básica de email"""
        return "@" in email and "." in email.split("@")[1]

    def _do_signup(self):
        """Maneja el registro"""
        self.msg.clear()
        
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        password = self.input_pw.text()
        password_confirm = self.input_pw_confirm.text()
        
        # Validaciones
        if not name or not email or not password:
            self._error("Please fill in all fields.")
            return
            
        if len(name) < 3:
            self._error("Username must be at least 3 characters long.")
            return
            
        if len(password) < 6:
            self._error("Password must be at least 6 characters long.")
            return
            
        if password != password_confirm:
            self._error("Passwords do not match.")
            return
            
        if not self._valid_email(email):
            self._error("Please enter a valid email address.")
            return
            
        if not self.terms.isChecked():
            self._error("Please agree to the Terms and Conditions.")
            return
        
        # Verificar si ya existe
        if user_exists(email, name):
            self._error("Email or username already exists.")
            return
        
        # Crear usuario
        try:
            user_id = create_user(email, name, password)
            if user_id:
                # Guardar sesión automáticamente
                try:
                    save_session(user_id, ttl_days=30)
                except Exception:
                    pass
                
                self._success("Account created successfully!")
                self.registered.emit(user_id)
            else:
                self._error("Failed to create account. Please try again.")
        except Exception as e:
            self._error(f"Error creating account: {str(e)}")
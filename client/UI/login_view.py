# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import  QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QFrame, QGraphicsDropShadowEffect
)
import requests
from client.config import API_BASE_URL, API_TIMEOUT
from client.Logic.session import save_session

class LoginView(QWidget):
    authenticated = pyqtSignal(int)
    ask_signup = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(900, 600)
        self.setStyleSheet("background: #FAFAFA; font-family: Helvetica;")

        # Layout principal
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 10, 0, 40)
        root.setSpacing(0)

        # Contenedor centrado
        container_layout = QHBoxLayout()
        container_layout.addStretch(1)
        
        # Card de login
        card = QFrame(self)
        card.setObjectName("card")
        card.setFixedWidth(560)
        card.move(210, 20)
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
        self.title = QLabel("Welcome Back!", card)
        self.title.setStyleSheet("font-size: 32px; font-weight: 800; color: black; background: transparent;")
        cl.addWidget(self.title)

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

        # Remember me y Forgot password
        row = QHBoxLayout()
        row.setSpacing(8)

        self.remember = QCheckBox("Remember me", card)
        self.remember.setStyleSheet("""
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

        self.forgot = QPushButton("Forgot Password?", card)
        self.forgot.setStyleSheet("""
            QPushButton { 
                border: none; 
                background: transparent; 
                color: #374151; 
            }
            QPushButton:hover { text-decoration: underline; }
        """)

        row.addWidget(self.remember, 0, Qt.AlignmentFlag.AlignLeft)
        row.addStretch(1)
        row.addWidget(self.forgot, 0, Qt.AlignmentFlag.AlignRight)
        cl.addLayout(row)

        # Divider
        div = QHBoxLayout()
        div.setContentsMargins(0, 8, 0, 8)

        lineL = QFrame(card)
        lineL.setFrameShape(QFrame.Shape.HLine)
        lineL.setFixedHeight(1)
        lineL.setStyleSheet("QFrame{background:#E5E7EB;}")

        txt = QLabel("Or continue with", card)
        txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt.setStyleSheet("QLabel{color:#6B7280; font-size:12px;}")

        lineR = QFrame(card)
        lineR.setFrameShape(QFrame.Shape.HLine)
        lineR.setFixedHeight(1)
        lineR.setStyleSheet("QFrame{background:#E5E7EB;}")

        div.addWidget(lineL, 1)
        div.addWidget(txt)
        div.addWidget(lineR, 1)
        cl.addLayout(div)

        # Botón login
        self.btn_login = QPushButton("Log In", card)
        self.btn_login.setStyleSheet("""
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
        cl.addWidget(self.btn_login)

        # Link de registro
        self.link_signup = QPushButton("Create an account", card)
        self.link_signup.setStyleSheet(
            "QPushButton { border:none; background:transparent; color:#366CF0; font-size:14px; }"
            "QPushButton:hover { text-decoration: underline; }"
        )
        cl.addWidget(self.link_signup, 0, Qt.AlignmentFlag.AlignLeft)

        # Mensajes
        self.msg = QLabel("", card)
        self.msg.setWordWrap(True)
        cl.addWidget(self.msg)

        container_layout.addWidget(card, 0, Qt.AlignmentFlag.AlignCenter)
        container_layout.addStretch(1)
        root.addLayout(container_layout)

        # Conectar eventos
        self.btn_login.clicked.connect(self._do_login)
        self.forgot.clicked.connect(lambda: self._info("Password reset flow not implemented."))
        self.link_signup.clicked.connect(self.ask_signup.emit)

        # Enter para enviar
        self.input_email.returnPressed.connect(self._do_login)
        self.input_pw.returnPressed.connect(self._do_login)

    def _info(self, text: str):
        self.msg.setStyleSheet("color:#6B7280;")
        self.msg.setText(text)

    def _do_login(self):
        self.msg.clear()
        email = self.input_email.text().strip()
        password = self.input_pw.text()

        if not email or not password:
            self.msg.setStyleSheet("color:#B91C1C;")
            self.msg.setText("Please enter your credentials.")
            return
        try:
            r = requests.post(
                f"{API_BASE_URL}/api/auth/login",
                json={"email": email, "password": password},
                timeout=API_TIMEOUT
            )
            if r.ok and r.json().get("success"):
                data = r.json()
                uid = data["user_id"]
                token = data["token"]
                try:
                    save_session(uid, token, ttl_days=30)
                except Exception:
                    pass
                self.msg.setStyleSheet("color:#065F46;")
                self.msg.setText("Signed in.")
                self.authenticated.emit(uid)
            else:
                msg = "Invalid credentials."
                try:
                    if r.headers.get("content-type", "").startswith("application/json"):
                        msg = r.json().get("message", msg)
                except Exception:
                    pass
                self.msg.setStyleSheet("color:#B91C1C;")
                self.msg.setText(msg)
        except Exception as e:
            self.msg.setStyleSheet("color:#B91C1C;")
            self.msg.setText(f"API error: {e}")

# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QGraphicsDropShadowEffect, QCheckBox
)

# path-hack como en tu app
BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from Logic.login import create_user, user_exists


class SignupView(QWidget):
    registered    = pyqtSignal()  # se emite cuando el usuario fue creado
    back_to_login = pyqtSignal()  # volver a la pantalla de login

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._wire()

    # ---------- UI ----------
    def _build_ui(self):
        self.setStyleSheet(
            "QWidget{background:#FEFEFE; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui;}"
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 40, 0, 40)
        root.setSpacing(0)

        # Card contenedora
        card = QFrame(self)
        card.setObjectName("card")
        card.setFixedWidth(560)
        card.setStyleSheet("""
            QFrame#card {
                background:#FFFFFF;
                border:1px solid #E5E7EB;
                border-radius:16px;
            }
            QLineEdit {
                background:#FFFFFF;
                border:1px solid #E5E7EB;
                border-radius:12px;
                padding:14px 16px;
                font-size:16px;
                color: black;
            }
            QLineEdit:focus { border:1px solid #366CF0; }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(36); shadow.setXOffset(0); shadow.setYOffset(14)
        shadow.setColor(QColor(0,0,0,45))
        card.setGraphicsEffect(shadow)

        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 32, 32, 24)
        cl.setSpacing(16)

        # Título
        title = QLabel("Create Your Account", card)
        title.setStyleSheet("QLabel{font-size:32px; font-weight:800; color:#111827;}")
        cl.addWidget(title)

        # Campos
        self.in_name = QLineEdit(card);  self.in_name.setPlaceholderText("Full Name");      cl.addWidget(self.in_name)
        self.in_email = QLineEdit(card); self.in_email.setPlaceholderText("Email Address"); cl.addWidget(self.in_email)

        self.in_pw1 = QLineEdit(card)
        self.in_pw1.setPlaceholderText("Password")
        self.in_pw1.setEchoMode(QLineEdit.EchoMode.Password)
        cl.addWidget(self.in_pw1)

        self.in_pw2 = QLineEdit(card)
        self.in_pw2.setPlaceholderText("Confirm Password")
        self.in_pw2.setEchoMode(QLineEdit.EchoMode.Password)
        cl.addWidget(self.in_pw2)

        # Aceptar términos
        terms_row = QHBoxLayout(); terms_row.setSpacing(8)
        self.chk_terms = QCheckBox("", card)
        self.chk_terms.setStyleSheet("""
         QCheckBox {
                background: transparent;
                color: #111827;
                font-size: 15px;
                border: none;
                border-radius: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #D1D5DB;
                border-radius: 5px;
                background: #FFFFFF;
                margin-right: 8px;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #366CF0;
            }
            QCheckBox::indicator:checked {
                background: #366CF0;
                border-color: #366CF0;
            }
            QCheckBox::indicator:checked:hover {
                background: #2F5CD3;
                border-color: #2F5CD3;
            }                                     
        """)
        lbl_terms = QLabel(
            'I agree to <a href="https://example.com/terms">Terms</a> & '
            '<a href="https://example.com/privacy">Privacy Policy</a>', card
        )
        lbl_terms.setOpenExternalLinks(True)
        lbl_terms.setStyleSheet("QLabel{color:#374151;}")
        terms_row.addWidget(self.chk_terms, 0, Qt.AlignmentFlag.AlignLeft)
        terms_row.addWidget(lbl_terms, 0, Qt.AlignmentFlag.AlignLeft)
        terms_row.addStretch(1)
        cl.addLayout(terms_row)

        # Botón principal
        self.btn_signup = QPushButton("Create Account", card)
        self.btn_signup.setStyleSheet("""
            QPushButton{
                background:#366CF0; color:#fff; border:none;
                border-radius:12px; padding:12px 16px; font-size:18px; font-weight:600;
            }
            QPushButton:hover{ background:#2F5CD3; }
            QPushButton:pressed{ background:#001F69; }
        """)
        cl.addWidget(self.btn_signup)

        # Link para volver a login
        self.btn_back = QPushButton("Already have an account? Log In", card)
        self.btn_back.setStyleSheet("""
            QPushButton{ border:none; background:transparent; color:#366CF0; }
            QPushButton:hover{ text-decoration:underline; }
        """)
        cl.addWidget(self.btn_back, 0, Qt.AlignmentFlag.AlignHCenter)

        # Mensajes
        self.msg = QLabel("", card)
        self.msg.setWordWrap(True)
        cl.addWidget(self.msg)

        # Centrado vertical
        wrap = QVBoxLayout()
        wrap.addStretch(1)
        wrap.addWidget(card, 0, Qt.AlignmentFlag.AlignHCenter)
        wrap.addStretch(1)
        root.addLayout(wrap)

    # ---------- eventos / lógica ----------
    def _wire(self):
        self.btn_back.clicked.connect(self.back_to_login.emit)
        self.btn_signup.clicked.connect(self._do_create)

        # Enter para enviar
        self.in_name.returnPressed.connect(self._do_create)
        self.in_email.returnPressed.connect(self._do_create)
        self.in_pw1.returnPressed.connect(self._do_create)
        self.in_pw2.returnPressed.connect(self._do_create)

    # Helpers de mensajes
    def _error(self, text: str):
        self.msg.setStyleSheet("QLabel{color:#B91C1C;}")
        self.msg.setText(text)

    def _ok(self, text: str):
        self.msg.setStyleSheet("QLabel{color:#065F46;}")
        self.msg.setText(text)

    # Validaciones
    def _valid_email(self, email: str) -> bool:
        if "@" not in email: return False
        local, _, dom = email.partition("@")
        return bool(local) and "." in dom and not dom.startswith(".") and not dom.endswith(".")

    def _do_create(self):
        self.msg.clear()

        name  = self.in_name.text().strip()   # se guardará como 'usuario'
        email = self.in_email.text().strip()
        pw1   = self.in_pw1.text()
        pw2   = self.in_pw2.text()

        # Checks
        if not name or not email or not pw1 or not pw2:
            self._error("All fields are required."); return
        if not self._valid_email(email):
            self._error("Invalid email address."); return
        if pw1 != pw2:
            self._error("Passwords do not match."); return
        if len(pw1) < 8:
            self._error("Password must be at least 8 characters."); return
        if not self.chk_terms.isChecked():
            self._error("You must agree to the Terms & Privacy Policy."); return

        # Unicidad
        try:
            if user_exists(email=email, usuario=name):
                self._error("Email or username already exists."); return
        except Exception as e:
            self._error(f"Error checking user: {e}"); return

        # Crear usuario
        try:
            create_user(email, name, pw1)  # usa tu tabla 'login' (email, usuario, pass)
            self._ok("Account created. You can sign in now.")
            self.registered.emit()         # si quieres entrar directo, ya lo conectaste en app.py
        except Exception as e:
            self._error(f"Error creating user: {e}")

# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# Ajustar sys.path para importar desde la raíz
BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QCheckBox, QSlider, QGraphicsDropShadowEffect, QMenu, QStackedWidget, QVBoxLayout
)
from PyQt6.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QIcon

from Logic.password_generator import generate_password
from Logic.storage import save_password, get_password_for_site
from Main.PerfilWindow import Perfil_Window
from Main.login_view import LoginView
from Main.password import View_Password
from Main.signup_view import SignupView   # <-- vista de registro


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Contraseñas")
        self.setGeometry(20, 20, 900, 500)
        self.setStyleSheet("background-color: #FEFEFE;")

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # QStackedWidget para gestionar pantallas
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Instancias de pantallas
        self.pantalla_principal = PasswordGenerator()
        self.perfil_widget = Perfil_Window()
        self.password_widget = View_Password()
        self.login_view = LoginView()
        self.signup_view = SignupView()

        # Añadir pantallas al stack
        self.stack.addWidget(self.login_view)          # index 0
        self.stack.addWidget(self.signup_view)         # index 1
        self.stack.addWidget(self.pantalla_principal)  # index 2
        self.stack.addWidget(self.perfil_widget)       # index 3
        self.stack.addWidget(self.password_widget)     # index 4

        # Arrancar mostrando el login
        self.stack.setCurrentWidget(self.login_view)

        # Botón menú (hamburguesa)
        self.btn_ventana = QPushButton("\u2630", self)
        self.btn_ventana.setGeometry(800, 20, 50, 30)
        self.btn_ventana.setStyleSheet("""
            QPushButton {
                background: #171C22;
                font-family: Helvetica;
                font-size: 16px;
                color: white;
                text-align: center;
                border: none;
                padding: 2px 2px;
                border-radius: 10px;
            }
            QPushButton::menu-indicator { image: none; width: 0px; }
        """)
        self.btn_ventana.clicked.connect(self.mostrar_menu_centrado)
        self.btn_ventana.setEnabled(False)

        # Flujo de autenticación
        def _on_auth():
            self.btn_ventana.setEnabled(True)
            self.mostrar_generador()

        self.login_view.authenticated.connect(_on_auth)
        self.login_view.ask_signup.connect(lambda: self.stack.setCurrentWidget(self.signup_view))
        self.signup_view.back_to_login.connect(lambda: self.stack.setCurrentWidget(self.login_view))
        self.signup_view.registered.connect(_on_auth)

        # Refresco inmediato cuando se guarda una contraseña
        self.pantalla_principal.password_saved.connect(
            lambda payload: getattr(self.password_widget, "refresh", lambda: None)()
        )

    def mostrar_menu_centrado(self):
        menu = QMenu(self)
        menu.addAction("Profile", self.mostrar_perfil)
        menu.addAction("Generator", self.mostrar_generador)
        menu.addAction("Password", self.mostrar_password)
        menu.setStyleSheet("""
            QMenu {
                background-color: #020C17;
                color: white;
                border: none;
                padding: 4px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui;
                font-size: 14px;
                border-radius: 8px;
            }
            QMenu::item { padding: 7px 14px; border-radius: 8px; }
            QMenu::item:selected { background-color: #112545; color: white; border-radius: 8px; }
        """)
        button_rect = self.btn_ventana.rect()
        button_center = self.btn_ventana.mapToGlobal(button_rect.center())
        menu_pos = QPoint(button_center.x() - 50, button_center.y() + 15)
        menu.exec(menu_pos)

    def mostrar_perfil(self):
        self.stack.setCurrentWidget(self.perfil_widget)

    def mostrar_generador(self):
        self.stack.setCurrentWidget(self.pantalla_principal)

    def mostrar_password(self):
        # Refresca al entrar, para garantizar que se vea lo último
        if hasattr(self.password_widget, "refresh"):
            self.password_widget.refresh()
        self.stack.setCurrentWidget(self.password_widget)


class PasswordGenerator(QWidget):
    # Señal: se emite cuando se guarda una contraseña nueva
    password_saved = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #FEFEFE;")
        self.setGeometry(0, 0, 900, 500)  # Tamaño dentro del stack

        # Título
        self.titulo = QLabel("Password Generator", self)
        self.titulo.setGeometry(105, 30, 400, 40)
        self.titulo.setStyleSheet(
            "font-family: Helvetica; font-size: 24px; color: black;"
        )

        # Salida de contraseña
        self.output = QLineEdit(self)
        self.output.setGeometry(100, 90, 440, 60)
        self.output.setText("PASSWORD")
        self.output.setReadOnly(True)
        self.output.setStyleSheet('''
           QLineEdit {
                font-family: "Courier New", monospace;
                font-size: 30px;
                color: #FFFFFF;
                background-color: #171C22;
                border: 2px solid #171C22;
                border-radius: 10px;
                padding: 15px 18px;
                selection-background-color: #007bff;
                selection-color: white;
            }
        ''')

        # Botón de copiar
        self.btn_copy = QPushButton(self)
        self.btn_copy.setIcon(QIcon("assets/copy-pass.png"))
        self.btn_copy.setGeometry(530, 89, 200, 62)
        self.btn_copy.setIconSize(QSize(80, 49))
        self.btn_copy.clicked.connect(self.copiar_al_portapapeles)
        self.btn_copy.setStyleSheet('''
            QPushButton {
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 32px;
                color: black;
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                padding: 12px 10px;
            }
            QPushButton:hover { color: #212529; }
            QPushButton:pressed { background-color: #dee2e6; }
        ''')
        shadow_btn = QGraphicsDropShadowEffect()
        shadow_btn.setBlurRadius(20)
        shadow_btn.setXOffset(4)
        shadow_btn.setYOffset(5)
        shadow_btn.setColor(QColor(0, 0, 0, 80))
        self.btn_copy.setGraphicsEffect(shadow_btn)

        # Checkboxes
        modern_checkbox_style = '''
            QCheckBox {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui;
                font-size: 16px;
                color: #4a5568;
                spacing: 12px;
                padding: 0px 4px;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 2px solid #e2e8f0;
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
            QCheckBox::indicator:checked:hover { background-color: #102A52; }
        '''
        self.chk_simbolos = QCheckBox("Include symbols", self)
        self.chk_simbolos.setGeometry(110, 170, 200, 30)
        self.chk_simbolos.setStyleSheet(modern_checkbox_style)

        self.chk_numeros = QCheckBox("Include numbers", self)
        self.chk_numeros.setGeometry(110, 200, 200, 30)
        self.chk_numeros.setStyleSheet(modern_checkbox_style)

        self.chk_mayusculas = QCheckBox("Uppercase letters", self)
        self.chk_mayusculas.setGeometry(110, 230, 200, 30)
        self.chk_mayusculas.setStyleSheet(modern_checkbox_style)

        # Usuario / Sitio
        self.lbl_usuario = QLabel("User", self)
        self.lbl_usuario.setGeometry(110, 270, 80, 27)
        self.lbl_usuario.setStyleSheet('font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui; font-size: 14px; color: black; font-weight: bold;')

        self.input_usuario = QLineEdit(self)
        self.input_usuario.setGeometry(150, 270, 200, 28)
        self.input_usuario.setStyleSheet('''
            QLineEdit {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui;
                font-size: 14px;
                color: #2c3e50;
                background-color: #ffffff;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 3px 12px;
            }
            QLineEdit:focus {
                border-color: #0B396B;
                background-color: #f8f9fa;
                outline: 0;
                box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
            }
            QLineEdit:hover { border-color: #ced4da; }
        ''')

        self.lbl_sitio = QLabel("Site", self)
        self.lbl_sitio.setGeometry(110, 300, 80, 27)
        self.lbl_sitio.setStyleSheet(self.lbl_usuario.styleSheet())

        self.input_sitio = QLineEdit(self)
        self.input_sitio.setGeometry(150, 300, 200, 28)
        self.input_sitio.setStyleSheet(self.input_usuario.styleSheet())

        # Slider longitud
        self.lbl_longitud = QLabel("Password Length", self)
        self.lbl_longitud.setGeometry(110, 350, 200, 20)
        self.lbl_longitud.setStyleSheet('font-family: Helvetica; font-size: 18px; color: black;')

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(6, 32)
        self.slider.setValue(14)
        self.slider.setGeometry(110, 380, 600, 30)
        self.slider.valueChanged.connect(self.actualizar_longitud)
        self.slider.setStyleSheet('''
            QSlider::groove:horizontal {
                border: none;
                height: 8px;
                background: #366CF0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #366CF0;
                width: 24px;
                height: 24px;
                border-radius: 12px;
                margin: -8px 0;
            }
            QSlider::handle:horizontal:pressed { background: #366CF0; }
            QSlider::sub-page:horizontal { background: #366CF0; border-radius: 2px; }
            QSlider::add-page:horizontal { background: #E0E0E0; border-radius: 2px; }
        ''')

        self.lbl_valor = QLabel("14", self)
        self.lbl_valor.setGeometry(720, 380, 30, 30)
        self.lbl_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_valor.setStyleSheet('''
            QLabel {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui;
                font-size: 18px; color: black; background-color: #DBDBDB;
                font-weight: bold; border-radius: 4px; padding: 2px 2px; border: 3px solid #CFCFCF;
            }
        ''')

        # Botón generar
        self.btn_generar = QPushButton("Generate Password", self)
        self.btn_generar.setGeometry(350, 430, 230, 50)
        self.btn_generar.clicked.connect(self.generar_contrasena)
        self.btn_generar.setStyleSheet('''
            QPushButton {
                font-family: Helvetica;
                font-size: 20px;
                color: white;
                background-color: #366CF0;
                border: none;
                border-radius: 5px;
                text-align: center;
            }
            QPushButton:hover { background-color: #366CF0; }
            QPushButton:pressed { background-color: #051B33; color: white; }
        ''')

    def actualizar_longitud(self, valor):
        self.lbl_valor.setText(f"{valor}")

    def copiar_al_portapapeles(self):
        self.output.selectAll()
        self.output.copy()

    def generar_contrasena(self):
        longitud = int(self.slider.value())
        incluir_mayusculas = self.chk_mayusculas.isChecked()
        incluir_numeros = self.chk_numeros.isChecked()
        incluir_simbolos = self.chk_simbolos.isChecked()

        pwd = generate_password(longitud, incluir_mayusculas, incluir_numeros, incluir_simbolos)
        self.output.setText(pwd)

        usuario = self.input_usuario.text().strip()
        sitio = self.input_sitio.text().strip()
        if usuario and sitio:
            save_password(sitio, usuario, pwd)
            # Notificar que hay una contraseña nueva (para refrescar otras vistas)
            self.password_saved.emit({"site": sitio, "user": usuario})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ventana()
    w.show()
    sys.exit(app.exec())

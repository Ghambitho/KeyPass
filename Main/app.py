# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# Ajustar sys.path para importar desde la raíz
BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QToolButton, QHBoxLayout,
    QCheckBox, QSlider, QGraphicsDropShadowEffect, QMenu, QStackedWidget, QVBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QIcon

from Logic.password_generator import generate_password
from Logic.storage import save_password
import config

# Usando versiones simples de los módulos
from Main.PerfilWindow import Perfil_Window
from Main.login_view import LoginView
from Main.password import View_Password
from Main.signup_view import SignupView   # <-- vista de registro
from Logic.session import has_session, load_session, clear_session
from Logic.login import get_user_profile
from Logic.database_init import init_database
import config


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setFixedSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.setStyleSheet("background-color: #F6F7FB;")
        
        # Crear barra de título personalizada
        self._create_title_bar()

        # Quitar la barra de título del sistema operativo
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

      

        self.current_user_id = None
        
        # Inicializar base de datos
        init_database()

        # --- Layout principal + Stack ---
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 40, 0, 0)  # Margen superior para la barra de título
        self.setLayout(self.layout)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # --- Instancias de pantallas ---
        self.pantalla_principal = PasswordGenerator()
        self.perfil_widget = Perfil_Window()
        self.password_widget = View_Password()
        self.login_view = LoginView()
        self.signup_view = SignupView()
        
        # Pasar referencia de la ventana principal al generador
        self.pantalla_principal.main_window = self

        # --- Agregar pantallas al stack ---
        self.stack.addWidget(self.login_view)          # index 0
        self.stack.addWidget(self.signup_view)         # index 1
        self.stack.addWidget(self.pantalla_principal)  # index 2
        self.stack.addWidget(self.perfil_widget)       # index 3
        self.stack.addWidget(self.password_widget)     # index 4

        # --- Botón menú (hamburguesa) ---
        self.btn_ventana = QPushButton("\u2630", self)
        self.btn_ventana.setGeometry(800, 50, 50, 30)
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

        # --- Pantalla inicial por defecto: Login ---
        self.stack.setCurrentWidget(self.login_view)

        # --- Flujo de autenticación ---
        def _on_auth(user_id):
            # Recibir user_id directamente del login
            self.current_user_id = user_id
            self.btn_ventana.setEnabled(True)
            self.mostrar_generador()

        self.login_view.authenticated.connect(_on_auth)
        self.login_view.ask_signup.connect(lambda: self.stack.setCurrentWidget(self.signup_view))
        self.signup_view.back_to_login.connect(lambda: self.stack.setCurrentWidget(self.login_view))
        # Para signup, recibir el user_id directamente
        self.signup_view.registered.connect(_on_auth)
        
        # Conectar logout desde perfil
        self.perfil_widget.logout_requested.connect(self.logout)

        # Refresco inmediato cuando se guarda una contraseña
        self.pantalla_principal.password_saved.connect(
            lambda payload: getattr(self.password_widget, "refresh", lambda: None)()
        )

        # --- Autologin si existe sesión válida (AHORA que todo ya existe) ---
        try:
            s = load_session()
            if s and isinstance(s, dict) and "user" in s:
                self.current_user_id = int(s["user"])
                self.btn_ventana.setEnabled(True)
                self.stack.setCurrentWidget(self.pantalla_principal)
            else:
                self.stack.setCurrentWidget(self.login_view)
        except Exception:
            self.stack.setCurrentWidget(self.login_view)

    def _create_title_bar(self):
        """Crea una barra de título personalizada"""
        # Barra de título
        self.title_bar = QFrame(self)
        self.title_bar.setGeometry(0, 0, 900, 30)
        self.title_bar.setStyleSheet("""
            QFrame {
                background-color: #F6F7FB;
                border: none;
            }
        """)
        
        # Título de la aplicación
        self.title_label = QLabel("KeyPass", self.title_bar)
        self.title_label.setGeometry(15, 0, 300, 30)
        self.title_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
                font-family: Helvetica;
            }
        """)
        
        # Botón minimizar
        self.minimize_btn = QPushButton("−", self.title_bar)
        self.minimize_btn.setGeometry(820, 2, 25, 25)
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                border: none;
                font-size: 18px;
                font-weight: bold;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #366CF0;
                color: white;
            }
        """)
        self.minimize_btn.clicked.connect(self.showMinimized)
        
        # Botón cerrar
        self.close_btn = QPushButton("×", self.title_bar)
        self.close_btn.setGeometry(860, 2, 25, 25)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                border: none;
                font-size: 18px;
                font-weight: bold;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #A32114;
                color: white;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        
        # Variables para arrastrar la ventana
        self.dragging = False
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        """Maneja el clic del mouse para arrastrar la ventana"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Solo arrastrar si se hace clic en la barra de título
            if event.pos().y() <= 40:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        """Maneja el movimiento del mouse para arrastrar la ventana"""
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Maneja la liberación del mouse"""
        self.dragging = False

    def mostrar_menu_centrado(self):
        menu = QMenu(self)
        menu.addAction("Profile", self.mostrar_perfil)
        menu.addAction("Generator", self.mostrar_generador)
        menu.addAction("Password", self.mostrar_password)
        menu.addSeparator()
        menu.addAction("Logout", self.logout)
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

    def logout(self):
        try:
            clear_session()
        except Exception:
            pass
        self.current_user_id = None
        self.btn_ventana.setEnabled(False)
        self.stack.setCurrentWidget(self.login_view)

    def mostrar_perfil(self):
        # Pasar el user_id actual al perfil
        if hasattr(self.perfil_widget, 'set_current_user'):
            self.perfil_widget.set_current_user(self.current_user_id)
        self.stack.setCurrentWidget(self.perfil_widget)

    def mostrar_generador(self):
        self.stack.setCurrentWidget(self.pantalla_principal)

    def mostrar_password(self):
        # Pasar el user_id actual al password widget
        if hasattr(self.password_widget, 'set_current_user'):
            self.password_widget.set_current_user(self.current_user_id)
        # Refresca al entrar, para garantizar que se vea lo último
        elif hasattr(self.password_widget, "refresh"):
            self.password_widget.refresh()
        self.stack.setCurrentWidget(self.password_widget)


class PasswordGenerator(QWidget):
    # Señal: se emite cuando se guarda una contraseña nueva
    password_saved = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
      

        self.setStyleSheet("background-color: #F6F7FB;")

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
                spacing: 14px;
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
        self.chk_simbolos.setGeometry(110, 180, 200, 30)
        self.chk_simbolos.setStyleSheet(modern_checkbox_style)

        self.chk_numeros = QCheckBox("Include numbers", self)
        self.chk_numeros.setGeometry(110, 210, 200, 30)
        self.chk_numeros.setStyleSheet(modern_checkbox_style)

        self.chk_mayusculas = QCheckBox("Uppercase letters", self)
        self.chk_mayusculas.setGeometry(110, 240, 200, 30)
        self.chk_mayusculas.setStyleSheet(modern_checkbox_style)

        # Usuario / Sitio
        self.lbl_usuario = QLabel("User", self)
        self.lbl_usuario.setGeometry(110, 290, 80, 27)
        self.lbl_usuario.setStyleSheet('font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui; font-size: 18px; color: black; font-weight: bold;')

        self.input_usuario = QLineEdit(self)
        self.input_usuario.setGeometry(150, 290, 200, 28)
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
        self.lbl_sitio.setGeometry(110, 330, 80, 27)
        self.lbl_sitio.setStyleSheet(self.lbl_usuario.styleSheet())

        self.input_sitio = QLineEdit(self)
        self.input_sitio.setGeometry(150, 330, 200, 28)
        self.input_sitio.setStyleSheet(self.input_usuario.styleSheet())

        # Slider longitud
        self.lbl_longitud = QLabel("Password Length", self)
        self.lbl_longitud.setGeometry(110, 400, 230, 20)
        self.lbl_longitud.setStyleSheet('background: transparent; font-family: Helvetica; font-size: 24px; color: black; font-weight: bold;')

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(6, 32)
        self.slider.setValue(14)
        self.slider.setGeometry(110, 430, 600, 30)
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
        self.lbl_valor.setGeometry(720, 430, 30, 30)
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
        self.btn_generar.setGeometry(320, 480, 230, 50)
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
            # Obtener user_id de la ventana principal
            user_id = getattr(self.main_window, 'current_user_id', None)
            if user_id:
                save_password(sitio, usuario, pwd, user_id)
                # Notificar que hay una contraseña nueva (para refrescar otras vistas)
                self.password_saved.emit({"site": sitio, "user": usuario})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ventana()
    w.show()
    sys.exit(app.exec())

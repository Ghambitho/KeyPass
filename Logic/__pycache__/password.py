# -*- coding: utf-8 -*-
import sys
from pathlib import Path

# Ajustar sys.path para importar desde la raíz del proyecto
BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QToolButton, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea, QApplication, QFrame, QStackedWidget, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor

# Importa del almacenamiento cifrado
# Nota: _load_all_passwords es "interno", pero lo usamos para listar en el visor.
from Logic.storage import _load_all_passwords
from Main.PerfilWindow import Perfil_Window



class View_Password(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ViewPassword")
        self.setStyleSheet("background: #FEFEFE;")
        self.setGeometry(20, 30, 900, 500)

        # ----- Cabecera -----
        self.titulo_saved = QLabel("Saved passwords", self)
        self.titulo_saved.setGeometry(105, 30, 400, 40)
        self.titulo_saved.setStyleSheet("""
            font-family: Helvetica; 
            font-size: 24px;
            color: black; border: none;
        """)

        self.input_pass = QLineEdit(self)
        self.input_pass.setPlaceholderText("search...")
        self.input_pass.setGeometry(100, 90, 700, 60)
        self.input_pass.setStyleSheet("""
            border: 3px solid #D4D2D2;
            border-radius: 10px;
            color: #111111;
            font-family: Helvetica;
            font-size: 18px;
            padding: 10px;
        """)

        # ----- Scroll + contenedor -----
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(100, 170, 700, 300)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("""
        QScrollArea { background: transparent; }
        QScrollBar:vertical {
            background: transparent;
            width: 8px;
            margin: 6px 2px 6px 0;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #FEFEFE;
            min-height: 30px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0; width: 0;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: transparent;
        }
        """)

        self.container = QWidget()
        self.vbox = QVBoxLayout(self.container)
        self.vbox.setContentsMargins(16, 8, 16, 8)
        self.vbox.setSpacing(15)
        self.scroll.setWidget(self.container)

        # Datos en memoria
        self._all_records = []   # [{'sitio': str, 'usuario': str, 'contraseña': str}, ...]
        self._item_widgets = []  # lista de QFrame

        # Filtro
        self.input_pass.textChanged.connect(self._apply_filter)

        # Cargar desde el almacén encriptado y pintar
        self._load_from_store()
        self._rebuild_list()

    # ================== Carga de datos ==================
    def _load_from_store(self):
        """
        Lee el archivo encriptado y trae todos los registros.
        Estructura esperada: [{'sitio':..., 'usuario':..., 'contraseña':...}, ...]
        """
        try:
            self._all_records = _load_all_passwords()
            if not isinstance(self._all_records, list):
                self._all_records = []
        except Exception:
            # Si hay cualquier problema de lectura/descifrado
            self._all_records = []

    # ================== Filtrado y render ==================
    def _apply_filter(self, text: str):
        self._rebuild_list(text)

    def _clear_vbox(self):
    # Saca TODO del layout: widgets y spacers
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def _rebuild_list(self, text: str | None = None):
        self._clear_vbox()
        self._item_widgets.clear()

        query = (text or self.input_pass.text() or "").strip().lower()
        for rec in self._all_records:
            if self._matches_filter(rec, query):
                self._insert_item_widget(rec)

        # estirador final para empujar al inicio
        self.vbox.addStretch(1)

    def _matches_filter(self, rec: dict, query: str) -> bool:
        if not query:
            return True
        hay = f"{rec.get('sitio','')} {rec.get('usuario','')}".lower()
        return query in hay

    def _insert_item_widget(self, rec: dict):
        card = self._build_card(rec)
        # Inserta antes del stretch final
        self.vbox.addWidget(card)  # basta así; si quieres, alinéalo arriba:
        self._item_widgets.append(card)

    # ================== UI de cada card ==================
    def _build_card(self, rec: dict) -> QWidget:
        """
        Card con:
          [ Sitio + Usuario ] [ ************ ] [👁] [📋]
        """
        sitio = rec.get("sitio", "")
        usuario = rec.get("usuario", "")
        password = rec.get("contraseña", "")

        card = QFrame(self)
        card.setFrameShape(QFrame.Shape.NoFrame)
        card.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 10px;       
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)              # Qué tan difusa la sombra
        shadow.setXOffset(4)                  # Desplazamiento horizontal
        shadow.setYOffset(6)                  # Desplazamiento vertical
        shadow.setColor(QColor(0, 0, 0, 55))  # Color negro con 60/255 de opacidad
        card.setGraphicsEffect(shadow)

        lay = QHBoxLayout(card)
        lay.setContentsMargins(16, 12, 12, 12)
        lay.setSpacing(6)

        # Columna izquierda: sitio + usuario
        left = QVBoxLayout()
        lbl_site = QLabel(sitio, card)
        lbl_site.setStyleSheet("font-size: 16px; color: #111827; font-weight: 600; border: none; font-weight: bold;")
        lbl_user = QLabel(usuario, card)
        lbl_user.setStyleSheet("font-size: 16px; color: #000000; border: none;")
        left.addWidget(lbl_site)
        left.addWidget(lbl_user)
        
        lay.addLayout(left, 21)

        # Campo contraseña (oculta, solo lectura)
        pwd = QLineEdit(card)
        pwd.setText(password)
        pwd.setReadOnly(True)
        pwd.setEchoMode(QLineEdit.EchoMode.Password)
        pwd.setFixedWidth(340)

        pwd.setMinimumWidth(120)
        pwd.setMaximumWidth(180)  # evita que empuje los botones
        pwd.setStyleSheet("""
            QLineEdit {
                font-size: 20px;
                background: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 6px 10px; 
                font-family: "Courier New", monospace;
                color: black;
                font-weight: bold;
            }
        """)
        lay.addWidget(pwd)
        lay.addStretch(1)

        # Botón ver/ocultar
        btn_eye = QToolButton(card)
        btn_eye.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_eye.setIcon(QIcon("assets/eye-closed.png"))  # inicia oculto
        btn_eye.setIconSize(QSize(28, 28))
        btn_eye.setFixedSize(44, 40)                     # <-- ancho correcto
        btn_eye.setToolTip("Ver contraseña")
        btn_eye.setStyleSheet("""
            QToolButton {
                background: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 6px;
            }
            QToolButton:hover { background: #F3F4F6; }
            QToolButton:pressed { background: #E5E7EB; }
        """)

        """
        eyeShadow = QGraphicsDropShadowEffect(btn_eye)
        eyeShadow.setBlurRadius(18)
        eyeShadow.setXOffset(0)
        eyeShadow.setYOffset(2)
        eyeShadow.setColor(QColor(0, 0, 0, 40))
        btn_eye.setGraphicsEffect(eyeShadow)
        """

        def _toggle():
            if pwd.echoMode() == QLineEdit.EchoMode.Password:
                pwd.setEchoMode(QLineEdit.EchoMode.Normal)
                btn_eye.setIcon(QIcon("assets/eye-open.png"))
                pwd.setStyleSheet("""
                    QLineEdit {
                font-size: 20px;
                background: #F3F4F6;
                border: none;
                border-radius: 10px;
                padding: 6px 10px; 
                font-family: "Courier New", monospace;
                color: black;
                font-weight: bold;
                }                """)
                btn_eye.setToolTip("Ocultar contraseña")
            else:
                pwd.setEchoMode(QLineEdit.EchoMode.Password)
                btn_eye.setIcon(QIcon("assets/eye-closed.png"))
                btn_eye.setToolTip("Ver contraseña")
                pwd.setStyleSheet("""
                QLineEdit {
                    font-size: 20px;
                    background: #FFFFFF;
                    border: none;
                    border-radius: 10px;
                    padding: 6px 10px; 
                    font-family: "Courier New", monospace;
                    color: black;
                    font-weight: bold;
                }
            """)
        btn_eye.clicked.connect(_toggle)
        lay.addWidget(btn_eye)


        # Botón copiar
        btn_copy = QToolButton(card)
        btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy.setIcon(QIcon("assets/copy-savepass.png"))
        btn_copy.setIconSize(QSize(22, 22))
        btn_copy.setFixedSize(44, 40)
        btn_copy.setToolTip("Copiar al portapapeles")
        btn_copy.setStyleSheet("""
            QToolButton {
                background: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 6px;
            }
            QToolButton:hover { background: #F3F4F6; }
            QToolButton:pressed { background: #E5E7EB; }
        """)

        """
        eyeShadow = QGraphicsDropShadowEffect(btn_eye)
        eyeShadow.setBlurRadius(18)
        eyeShadow.setXOffset(0)
        eyeShadow.setYOffset(2)
        eyeShadow.setColor(QColor(0, 0, 0, 40))
        btn_eye.setGraphicsEffect(eyeShadow)
        """

        def _copy():
            pwd.selectAll()
            pwd.copy()
        btn_copy.clicked.connect(_copy)
        lay.addWidget(btn_copy)

        return card


# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QToolButton, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QMessageBox, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor


import requests
from client.config import API_BASE_URL, API_TIMEOUT
from client.Logic.session import load_session

class View_Password(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #FAFAFA;")
        
        # Inicializar user_id
        self.user_id = None

        # ----- Cabecera -----
        self.titulo_saved = QLabel("Saved passwords", self)
        self.titulo_saved.setGeometry(105, 30, 400, 40)
        self.titulo_saved.setStyleSheet("""
            font-family: Helvetica;
            font-size: 24px;
            font-weight: bold;
            color: black; border: none;
            background: transparent;
        """)

        self.input_pass = QLineEdit(self)
        self.input_pass.setPlaceholderText("search...")
        self.input_pass.setGeometry(90, 90, 700, 60)
        self.input_pass.setStyleSheet("""
            border: 3px solid #D4D2D2;
            border-radius: 10px;
            color: #111111;
            font-family: Helvetica;
            font-size: 18px;
            padding: 10px;
        """)

        # Botón para agregar
        self.btn_add = QPushButton("+ Add", self)
        self.btn_add.setGeometry(800, 100, 60, 40)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background: #2563EB;
                color: white;
                font-family: Helvetica;
                font-size: 14px;
                border: none;
                border-radius: 10px;
                padding: 6px 12px;
            }
            QPushButton:hover { background: #1D4ED8; }
            QPushButton:pressed { background: #1E40AF; }
        """)
        self.btn_add.clicked.connect(self._open_add_dialog)

        # ----- Scroll + contenedor -----
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(90, 170, 700, 300)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("""
        background: transparent;
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

    # ---------- API pública ----------
    def set_current_user(self, user_id):
        """Establece el usuario actual y recarga los datos"""
        self.user_id = user_id
        self.refresh()
    
    def refresh(self):
        """Recarga desde la base de datos y reconstruye la lista al instante."""
        self._load_from_store()
        current_query = self.input_pass.text()
        self._rebuild_list(current_query)

    def showEvent(self, event):
        super().showEvent(event)
        # Al mostrar la vista, garantizamos que se ve lo último
        try:
            self.refresh()
        except Exception:
            pass

    # ================== Carga de datos ==================
    def _load_from_store(self):
        if self.user_id:
            s = load_session()
            self._all_records = []
            if s and "token" in s:
                r = requests.get(
                    f"{API_BASE_URL}/api/passwords",
                    headers={"Authorization": f"Bearer {s['token']}"},
                    timeout=API_TIMEOUT
                )
                if r.ok and r.json().get("success"):
                    self._all_records = r.json().get("passwords", [])
        else:
            self._all_records = []
        if not isinstance(self._all_records, list):
            self._all_records = []
            
    # ================== Filtrado y render ==================
    def _apply_filter(self, text: str):
        self._rebuild_list(text)

    def _clear_layout(self):
        """Elimina TODOS los widgets/espaciadores del layout para evitar acumulación de stretches."""
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def _rebuild_list(self, text: str | None = None):
        # Evitar parpadeo al reconstruir
        self.setUpdatesEnabled(False)

        # limpiar cards previas + stretches anteriores
        self._clear_layout()
        self._item_widgets.clear()

        query = (text or self.input_pass.text() or "").strip().lower()
        for rec in self._all_records:
            if self._matches_filter(rec, query):
                self._insert_item_widget(rec)

        # estirador final para empujar al inicio
        self.vbox.addStretch(1)

        self.setUpdatesEnabled(True)

    def _matches_filter(self, rec: dict, query: str) -> bool:
        if not query:
            return True
        hay = f"{rec.get('site','')} {rec.get('username','')}".lower()
        return query in hay

    def _insert_item_widget(self, rec: dict) -> QWidget:
        card = self._build_card(rec)
        # Inserta antes del stretch final
        self.vbox.insertWidget(max(self.vbox.count() - 1, 0), card)
        self._item_widgets.append(card)
        return card

    # ================== UI de cada card ==================
    def _build_card(self, rec: dict) -> QWidget:
        """
        Card con:
          [ Sitio + Usuario ] [ ************ ] [👁] [📋]
        """
        sitio = rec.get("site", "")
        usuario = rec.get("username", "")
        password = rec.get("password", "")

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
        shadow.setBlurRadius(25)
        shadow.setXOffset(4)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 55))
        card.setGraphicsEffect(shadow)

        lay = QHBoxLayout(card)
        lay.setContentsMargins(16, 12, 12, 12)
        lay.setSpacing(6)

        rec_id = rec.get("id")  # requiere que storage devuelva 'id'
        
        # Botón Editar
        btn_edit = QToolButton(card)
        btn_edit.setText("Edit")
        btn_edit.setToolTip("Editar esta contraseña")
        btn_edit.setStyleSheet("""
            QToolButton {
                background: #3B82F6;
                color: white;
                font-family: Helvetica;
                font-size: 12px;
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
            }
            QToolButton:hover { background: #2563EB; }
            QToolButton:pressed { background: #1D4ED8; }
        """)
        
        def _edit():
            if not self.user_id:
                msg = QMessageBox(self)
                msg.setWindowTitle("Error")
                msg.setText("No hay usuario en sesión.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStyleSheet(" Color: black; ")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return
                
            if rec_id is None:
                msg = QMessageBox(self)
                msg.setWindowTitle("Error")
                msg.setText("No se encontró el identificador del registro.")
                msg.setStyleSheet(" Color: black; ")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return
            
            # Abrir diálogo de edición
            dlg = EditPasswordDialog(self, sitio, usuario, password)
            dlg.setWindowTitle("Edit Password")
            dlg.setStyleSheet("background: #FEFEFE; Color: black;")

            if dlg.exec() == QDialog.DialogCode.Accepted:
                new_sitio, new_usuario, new_clave = dlg.get_data()

                if new_sitio and new_usuario and new_clave:
                    try:
                        s = load_session()
                        if not s or "token" not in s:
                            raise RuntimeError("No valid session found.")
                        
                        dr = requests.delete(
                            f"{API_BASE_URL}/api/passwords/{rec_id}",
                            headers={"Authorization": f"Bearer {s['token']}"},
                            timeout=API_TIMEOUT
                        )
                        if not dr.ok:
                            raise RuntimeError("No se pudo eliminar el registro antiguo")
                        
                        cr = requests.post(
                            f"{API_BASE_URL}/api/passwords",
                            headers={"Authorization": f"Bearer {s['token']}"},
                            json={"site": new_sitio, "username": new_usuario, "password": new_clave},
                            timeout=API_TIMEOUT
                        )
                        if not (cr.ok and cr.json().get("success")):
                            raise RuntimeError(cr.json().get("message", "Error al guardar")
                                               )
                        # Mostrar mensaje de éxito
                        success_msg = QMessageBox(self)
                        success_msg.setWindowTitle("Éxito")
                        success_msg.setText(f"Contraseña de '{new_sitio}' actualizada correctamente.")
                        success_msg.setStyleSheet(" Color: black; ")
                        success_msg.setIcon(QMessageBox.Icon.Information)
                        success_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        success_msg.exec()
                        self.refresh()
                    except Exception as e:
                        error_msg = QMessageBox(self)
                        error_msg.setWindowTitle("Error")
                        error_msg.setText(f"Error al actualizar: {str(e)}")
                        error_msg.setIcon(QMessageBox.Icon.Critical)
                        error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        error_msg.exec()
        
        btn_edit.clicked.connect(_edit)
        lay.addWidget(btn_edit)
        
        # Botón Eliminar
        btn_del = QToolButton(card)
        btn_del.setText("Delete")
        btn_del.setToolTip("Eliminar esta contraseña")
        btn_del.setStyleSheet("""
            QToolButton {
                background: #EF4444;
                color: white;
                font-family: Helvetica;
                font-size: 12px;
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
            }
            QToolButton:hover { background: #DC2626; }
            QToolButton:pressed { background: #B91C1C; }
        """)
        def _delete():
            if not self.user_id:
                msg = QMessageBox(self)
                msg.setWindowTitle("Error")
                msg.setText("No hay usuario en sesión.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStyleSheet(" Color: black; ")

                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return
                
            if rec_id is None:
                msg = QMessageBox(self)
                msg.setWindowTitle("Error")
                msg.setText("No se encontró el identificador del registro.")
                msg.setStyleSheet(" Color: black; ")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return
            
            # Crear diálogo de confirmación personalizado
            msg = QMessageBox(self)
            msg.setWindowTitle("Confirmar eliminación")
            msg.setText(f"¿Estás seguro de que quieres eliminar la contraseña de '{sitio}' para el usuario '{usuario}'?")
            msg.setStyleSheet(" Color: black; ")
            msg.setInformativeText("Esta acción no se puede deshacer.")
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            
            # Personalizar los botones
            yes_button = msg.button(QMessageBox.StandardButton.Yes)
            yes_button.setText("Sí, eliminar")
            yes_button.setStyleSheet("""
                QPushButton {
                    background: #EF4444;
                    color: white;
                    font-family: Helvetica;
                    font-size: 14px;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 100px;
                }
                QPushButton:hover { background: #DC2626; }
                QPushButton:pressed { background: #B91C1C; }
            """)
            
            no_button = msg.button(QMessageBox.StandardButton.No)
            no_button.setText("Cancelar")
            no_button.setStyleSheet("""
                QPushButton {
                    background: #6B7280;
                    color: white;
                    font-family: Helvetica;
                    font-size: 14px;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 100px;
                }
                QPushButton:hover { background: #4B5563; }
                QPushButton:pressed { background: #374151; }
            """)
            
            resp = msg.exec()
            if resp == QMessageBox.StandardButton.Yes:
                try:
                    s = load_session()
                    if not s or "token" not in s:
                        raise RuntimeError("No valid session found.")
                    r = requests.delete(
                        f"{API_BASE_URL}/api/passwords/{rec_id}",
                        headers={"Authorization": f"Bearer {s['token']}"},
                        timeout=API_TIMEOUT
                    )
                    if r.ok and r.json().get("success"):
                        # Mostrar mensaje de éxito
                        success_msg = QMessageBox(self)
                        success_msg.setWindowTitle("Éxito")
                        success_msg.setText(f"Contraseña de '{sitio}' eliminada correctamente.")
                        success_msg.setStyleSheet(" Color: black; ")
                        success_msg.setIcon(QMessageBox.Icon.Information)
                        success_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        success_msg.exec()
                        self.refresh()
                    else:
                        error_msg = QMessageBox(self)
                        error_msg.setWindowTitle("Error")
                        error_msg.setText(r.json().get("message", "No se pudo eliminar el registro."))
                        error_msg.setIcon(QMessageBox.Icon.Warning)
                        error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        error_msg.exec()
                except Exception as e:
                    error_msg = QMessageBox(self)
                    error_msg.setWindowTitle("Error")
                    error_msg.setText(f"Error al eliminar: {str(e)}")
                    error_msg.setIcon(QMessageBox.Icon.Critical)
                    error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    error_msg.exec()
        
        btn_del.clicked.connect(_delete)
        lay.addWidget(btn_del)

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
        pwd.setFixedWidth(200)  # Ancho fijo consistente
        pwd.setMinimumWidth(120)
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
        btn_eye.setFixedSize(44, 40)
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
                    }""")
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

        def _copy():
            pwd.selectAll()
            pwd.copy()
        btn_copy.clicked.connect(_copy)
        lay.addWidget(btn_copy)

        return card

    def _open_add_dialog(self):
        if not self.user_id:
            open = QMessageBox(self)
            open.setWindowTitle("Error")
            open.setText("No hay usuario en sesión.")
            open.setIcon(QMessageBox.Icon.Warning)
            open.setStyleSheet(" Color: black; ")
            open.setStandardButtons(QMessageBox.StandardButton.Ok)
            open.exec()
            return
        
        dlg = AddPasswordDialog(self)
        dlg.setWindowTitle("Add Password")
        dlg.setStyleSheet("background: #FEFEFE; Color: black;")
        if dlg.exec() == QDialog.DialogCode.Accepted:
            sitio, usuario, clave = dlg.get_data()
            if sitio and usuario and clave:
                try:
                    s = load_session()
                    if not s or "token" not in s:
                        raise RuntimeError("No valid session found.")
                    r = requests.post(
                        f"{API_BASE_URL}/api/passwords",
                        headers={"Authorization": f"Bearer {s['token']}"},
                        json={"site": sitio, "username": usuario, "password": clave},
                        timeout=API_TIMEOUT
                    )
                    if r.ok and r.json().get("success"):
                        self.refresh()
                    else:
                        QMessageBox.warning(self, "Error", r.json().get("message", "No se pudo guardar la contraseña."))
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo guardar la contraseña: {e}")


class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Password")
        form = QFormLayout(self)

        self.input_site = QLineEdit(self)
        self.input_site.setPlaceholderText("Site")
        self.input_user = QLineEdit(self)
        self.input_user.setPlaceholderText("Username")
        self.input_pass = QLineEdit(self)
        self.input_pass.setPlaceholderText("Password")

        form.addRow("Site:", self.input_site)
        form.addRow("Username:", self.input_user)
        form.addRow("Password:", self.input_pass)

        row = QHBoxLayout()
        btn_ok = QPushButton("Save", self)
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.clicked.connect(self.reject)
        row.addStretch(1)
        row.addWidget(btn_ok)
        row.addWidget(btn_cancel)
        form.addRow(row)

    def get_data(self):
        return (self.input_site.text().strip(), self.input_user.text().strip(), self.input_pass.text().strip())


class EditPasswordDialog(QDialog):
    def __init__(self, parent=None, sitio="", usuario="", password=""):
        super().__init__(parent)
        self.setWindowTitle("Edit Password")
        self.setFixedSize(400, 250)
        form = QFormLayout(self)

        self.input_site = QLineEdit(self)
        self.input_site.setPlaceholderText("Site")
        self.input_site.setText(sitio)
        self.input_site.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #E5E7EB;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
        """)

        self.input_user = QLineEdit(self)
        self.input_user.setPlaceholderText("Username")
        self.input_user.setText(usuario)
        self.input_user.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #E5E7EB;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
        """)

        self.input_pass = QLineEdit(self)
        self.input_pass.setPlaceholderText("Password")
        self.input_pass.setText(password)
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #E5E7EB;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
        """)

        # Botón para mostrar/ocultar contraseña
        self.btn_toggle_pass = QPushButton("👁", self)
        self.btn_toggle_pass.setFixedSize(30, 30)
        self.btn_toggle_pass.setStyleSheet("""
            QPushButton {
                background: #F3F4F6;
                border: 2px solid #E5E7EB;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #E5E7EB;
            }
        """)
        
        def toggle_password():
            if self.input_pass.echoMode() == QLineEdit.EchoMode.Password:
                self.input_pass.setEchoMode(QLineEdit.EchoMode.Normal)
                self.btn_toggle_pass.setText("🙈")
            else:
                self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
                self.btn_toggle_pass.setText("👁")
        
        self.btn_toggle_pass.clicked.connect(toggle_password)

        # Layout para contraseña con botón
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(self.input_pass)
        pass_layout.addWidget(self.btn_toggle_pass)

        form.addRow("Site:", self.input_site)
        form.addRow("Username:", self.input_user)
        form.addRow("Password:", pass_layout)

        # Botones
        row = QHBoxLayout()
        btn_save = QPushButton("Save Changes", self)
        btn_save.setStyleSheet("""
            QPushButton {
                background: #3B82F6;
                color: white;
                font-family: Helvetica;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover { background: #2563EB; }
            QPushButton:pressed { background: #1D4ED8; }
        """)
        btn_save.clicked.connect(self.accept)
        
        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: #6B7280;
                color: white;
                font-family: Helvetica;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover { background: #4B5563; }
            QPushButton:pressed { background: #374151; }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        row.addStretch(1)
        row.addWidget(btn_save)
        row.addWidget(btn_cancel)
        form.addRow(row)

    def get_data(self):
        return (self.input_site.text().strip(), self.input_user.text().strip(), self.input_pass.text().strip())


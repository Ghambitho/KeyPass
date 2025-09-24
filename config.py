# -*- coding: utf-8 -*-
"""
Configuración global de KeyPass
"""

# Configuración de la aplicación
APP_NAME = "KeyPass"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Gestor de Contraseñas Seguro"

# Configuración de base de datos
DB_NAME = "keypass.db"
DB_PATH = "db/"

# Configuración de cifrado
ENCRYPTION_ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 200_000
SALT_BYTES = 16

# Configuración de sesiones
DEFAULT_TTL_DAYS = 30
SESSION_FILE = "session.bin"
SESSION_KEY_FILE = "session.key"

# Configuración de UI
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 500
WINDOW_TITLE = "Generador de Contraseñas"

# Configuración de contraseñas
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 32
DEFAULT_PASSWORD_LENGTH = 14

# Configuración de archivos
ASSETS_PATH = "assets/"
DOCS_PATH = "docs/"

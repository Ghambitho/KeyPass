# -*- coding: utf-8 -*-
"""
Configuración global de KeyPass
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv('keypass.env')

# Configuración de la aplicación
APP_NAME = "KeyPass"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Gestor de Contraseñas Seguro"

# Configuración de entorno
ENV = os.getenv('KEYPASS_ENV', 'development')
DEBUG = os.getenv('KEYPASS_DEBUG', 'true').lower() == 'true'
LOG_LEVEL = os.getenv('KEYPASS_LOG_LEVEL', 'INFO')

# Configuración de base de datos
DB_NAME = os.getenv('DB_NAME', 'keypass.db')
DB_PATH = os.getenv('DB_PATH', 'db/')

# Configuración de cifrado
ENCRYPTION_ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 200_000
SALT_BYTES = 16

# Configuración de sesiones
DEFAULT_TTL_DAYS = int(os.getenv('SESSION_TTL_DAYS', '30'))
SESSION_FILE = "session.bin"

# Configuración de seguridad
MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', '5'))
LOCKOUT_TIME_MINUTES = int(os.getenv('LOCKOUT_TIME_MINUTES', '5'))

# Configuración de UI
WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '900'))
WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
WINDOW_TITLE = os.getenv('WINDOW_TITLE', 'KeyPass - Gestor de Contraseñas')

# Configuración de contraseñas
MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '6'))
MAX_PASSWORD_LENGTH = int(os.getenv('MAX_PASSWORD_LENGTH', '32'))
DEFAULT_PASSWORD_LENGTH = int(os.getenv('DEFAULT_PASSWORD_LENGTH', '14'))

# Configuración de archivos
ASSETS_PATH = os.getenv('ASSETS_PATH', 'assets/')
DOCS_PATH = os.getenv('DOCS_PATH', 'docs/')

# Función para verificar si estamos en producción
def is_production():
    return ENV.lower() == 'production'

# Función para verificar si el debug está habilitado
def is_debug():
    return DEBUG

# -*- coding: utf-8 -*-
"""Configuración global de KeyPass"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Entorno
ENV = os.getenv('ENV', 'development')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# Base de datos SQLite local
DB_PATH = os.getenv('DB_PATH', 'db')
DB_FILE = os.getenv('DB_FILE', 'keypass.db')

# JWT
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = "HS256"

# Cifrado
ENCRYPTION_ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = int(os.getenv('DEFAULT_ITERATIONS', '200000'))
SALT_BYTES = int(os.getenv('SALT_BYTES', '16'))

# Sesión
DEFAULT_TTL_DAYS = int(os.getenv('SESSION_TTL_DAYS', '30'))
SESSION_FILE = "session.bin"

# UI (para el .exe)
WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '900'))
WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
WINDOW_TITLE = os.getenv('WINDOW_TITLE', 'KeyPass - Gestor de Contraseñas')

# Contraseñas
MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '6'))
MAX_PASSWORD_LENGTH = int(os.getenv('MAX_PASSWORD_LENGTH', '32'))
DEFAULT_PASSWORD_LENGTH = int(os.getenv('DEFAULT_PASSWORD_LENGTH', '14'))

# Archivos
ASSETS_PATH = os.getenv('ASSETS_PATH', 'Main/assets/')
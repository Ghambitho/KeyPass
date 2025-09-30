# -*- coding: utf-8 -*-
"""Configuración global de KeyPass"""
import os
from dotenv import load_dotenv

load_dotenv('keypass.env')

ENV = os.getenv('KEYPASS_ENV', 'development')
DEBUG = os.getenv('KEYPASS_DEBUG', 'true').lower() == 'true'

DB_NAME = os.getenv('DB_NAME', 'keypass.db')
DB_PATH = os.getenv('DB_PATH', 'db/')

ENCRYPTION_ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 200_000
SALT_BYTES = 16

DEFAULT_TTL_DAYS = int(os.getenv('SESSION_TTL_DAYS', '30'))
SESSION_FILE = "session.bin"


WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '900'))
WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
WINDOW_TITLE = os.getenv('WINDOW_TITLE', 'KeyPass - Gestor de Contraseñas')

MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '6'))
MAX_PASSWORD_LENGTH = int(os.getenv('MAX_PASSWORD_LENGTH', '32'))
DEFAULT_PASSWORD_LENGTH = int(os.getenv('DEFAULT_PASSWORD_LENGTH', '14'))

ASSETS_PATH = os.getenv('ASSETS_PATH', 'assets/')
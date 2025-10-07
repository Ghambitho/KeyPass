# -*- coding: utf-8 -*-
"""Configuración global de KeyPass"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Entorno
ENV = os.getenv('ENV', 'development')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# Base de datos PostgreSQL
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

# Validar variables de base de datos
if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
    raise RuntimeError("Faltan variables de base de datos: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD")


# JWT
JWT_SECRET = os.getenv("JWT_SECRET") or ""
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", "15"))
if not JWT_SECRET:
    raise RuntimeError("Falta JWT_SECRET")

# Cifrado
ENCRYPTION_ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = int(os.getenv('DEFAULT_ITERATIONS', '200000'))
SALT_BYTES = int(os.getenv('SALT_BYTES', '16'))

ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]

# Configuración de contraseñas
DEFAULT_PASSWORD_LENGTH = int(os.getenv('DEFAULT_PASSWORD_LENGTH', '16'))
MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '8'))
MAX_PASSWORD_LENGTH = int(os.getenv('MAX_PASSWORD_LENGTH', '128'))
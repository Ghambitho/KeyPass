# -*- coding: utf-8 -*-
"""Configuración global de KeyPass"""
import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

# Entorno
ENV = os.getenv('ENV', 'development')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# Base de datos PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "keypass")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

if not os.getenv("DB_HOST"):
    logger.warning("DB_HOST no está configurado. Usando valores de desarrollo por defecto.")


# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", "15"))

if JWT_SECRET == "change-me-in-production":
    logger.warning("JWT_SECRET no configurado. Usando clave insegura para desarrollo.")

# Cifrado
ENCRYPTION_ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = int(os.getenv('DEFAULT_ITERATIONS', '200000'))
SALT_BYTES = int(os.getenv('SALT_BYTES', '16'))

# Contraseñas
MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '6'))
MAX_PASSWORD_LENGTH = int(os.getenv('MAX_PASSWORD_LENGTH', '32'))
DEFAULT_PASSWORD_LENGTH = int(os.getenv('DEFAULT_PASSWORD_LENGTH', '14'))

ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]

# Configuración de contraseñas
DEFAULT_PASSWORD_LENGTH = int(os.getenv('DEFAULT_PASSWORD_LENGTH', '16'))
MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '8'))
MAX_PASSWORD_LENGTH = int(os.getenv('MAX_PASSWORD_LENGTH', '128'))
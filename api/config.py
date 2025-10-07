# -*- coding: utf-8 -*-
"""Configuración global de KeyPass"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Entorno
ENV = os.getenv('ENV', 'development')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

#Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL") or "" 
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or ""
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL y/o SUPABASE_KEY")

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

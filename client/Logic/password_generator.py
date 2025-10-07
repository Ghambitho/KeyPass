# -*- coding: utf-8 -*-
import random
import string
from client import config

def generate_password(longitud=None, incluir_mayusculas=True, incluir_numeros=True, incluir_simbolos=True):
    """
    Genera una contraseña segura con la longitud especificada.
    Si no se especifica longitud, usa la configuración por defecto.
    """
    if longitud is None:
        longitud = config.DEFAULT_PASSWORD_LENGTH
    
    # Validar longitud
    longitud = max(config.MIN_PASSWORD_LENGTH, min(config.MAX_PASSWORD_LENGTH, int(longitud)))
    
    caracteres = string.ascii_lowercase
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += "{[|'}¬¦!£$]%^&<:*>;#~_-+=,@"
    
    return ''.join(random.choices(caracteres, k=longitud))

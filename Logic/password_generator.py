# -*- coding: utf-8 -*-
import random
import string

def generate_password(longitud, incluir_mayusculas=True, incluir_numeros=True, incluir_simbolos=True):
    caracteres = string.ascii_lowercase
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += "!@#$%&()_-+^*?"
    return ''.join(random.choices(caracteres, k=int(longitud)))

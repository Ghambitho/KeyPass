# -*- coding: utf-8 -*-
"""
Módulo de almacenamiento usando la API de KeyPass
Reemplaza las funciones de storage local por llamadas a la API
"""

from Logic.api_client import KeyPassAPIClient
from typing import List, Dict

# Cliente global de la API
_api_client = KeyPassAPIClient()

def _load_all_passwords(user_id: int) -> List[Dict]:
    """Cargar todas las contraseñas del usuario usando la API"""
    passwords = _api_client.get_passwords()
    
    # Convertir formato de la API al formato esperado por la aplicación
    result = []
    for pwd in passwords:
        result.append({
            "id": pwd.get("id"),
            "sitio": pwd.get("site"),
            "usuario": pwd.get("username"),
            "contraseña": pwd.get("password")
        })
    
    return result

def delete_password(record_id: int, user_id: int) -> bool:
    """Eliminar contraseña usando la API"""
    return _api_client.delete_password(record_id)

def save_password(sitio: str, usuario: str, contraseña: str, user_id: int) -> bool:
    """Guardar nueva contraseña usando la API"""
    return _api_client.save_password(sitio, usuario, contraseña)

def get_api_client() -> KeyPassAPIClient:
    """Obtener el cliente de la API para uso directo"""
    return _api_client

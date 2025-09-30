# -*- coding: utf-8 -*-
"""
Módulo de login usando la API de KeyPass
Reemplaza las funciones de login local por llamadas a la API
"""

from Logic.api_client import KeyPassAPIClient
from typing import Optional

# Cliente global de la API
_api_client = KeyPassAPIClient()

def user_exists(email: str = "", usuario: str = "") -> bool:
    """Verificar si un usuario existe (no disponible en API, retorna False)"""
    # La API no expone esta funcionalidad por seguridad
    return False

def create_user(email: str, usuario: str, password: str) -> int:
    """Crear nuevo usuario usando la API"""
    if _api_client.register(email, usuario, password):
        # Después del registro exitoso, hacer login automático para obtener el user_id
        if _api_client.login(email, password):
            return _api_client.user_id or 1
        return 1  # Fallback si no se puede obtener el user_id
    return 0  # Retorna 0 si falla

def verify_user(login: str, password: str) -> bool:
    """Verificar credenciales usando la API"""
    return _api_client.login(login, password)

def get_user_profile(user_id: int) -> tuple | None:
    """Obtener perfil del usuario (no disponible en API actual)"""
    # La API actual no expone esta funcionalidad
    return None

def update_user_profile(user_id: int, new_email: str, new_usuario: str) -> bool:
    """Actualizar perfil del usuario usando la API"""
    return _api_client.update_profile(new_email, new_usuario)

def get_user_id(login: str) -> int | None:
    """Obtener ID del usuario (retorna el ID de la sesión actual)"""
    if _api_client.is_logged_in():
        return _api_client.user_id
    return None

def get_api_client() -> KeyPassAPIClient:
    """Obtener el cliente de la API para uso directo"""
    return _api_client

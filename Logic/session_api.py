# -*- coding: utf-8 -*-
"""
Módulo de sesión usando la API de KeyPass
Maneja sesiones usando tokens JWT de la API
"""

from Logic.api_client import KeyPassAPIClient
from typing import Optional, Dict
import config
import time

# Cliente global de la API
_api_client = KeyPassAPIClient()

def save_session(user_id: int, ttl_days: int = None) -> None:
    """Guarda la sesión del usuario (ya está guardada en el cliente API)"""
    # La sesión ya está guardada en el cliente API después del login
    # No necesitamos hacer nada adicional
    pass

def load_session() -> Dict | None:
    """Devuelve la información de la sesión si existe"""
    if _api_client.is_logged_in():
        return {
            "user": _api_client.user_id,
            "ts": int(time.time()),
            "ttl": 86400  # 24 horas
        }
    return None

def has_session() -> bool:
    """Verificar si hay una sesión activa"""
    return _api_client.is_logged_in()

def clear_session() -> None:
    """Limpiar la sesión"""
    _api_client.logout()

def get_user_id_from_session() -> Optional[int]:
    """Obtener el user_id de la sesión actual"""
    if _api_client.is_logged_in():
        return _api_client.user_id
    return None

def get_api_client() -> KeyPassAPIClient:
    """Obtener el cliente de la API"""
    return _api_client

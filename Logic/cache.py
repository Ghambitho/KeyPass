# -*- coding: utf-8 -*-
"""Sistema de caché para optimizar rendimiento"""
import time
from typing import Dict, Any, Optional

class UserCache:
    """Caché simple para datos del usuario"""
    
    def __init__(self, ttl_seconds: int = 300):  # 5 minutos por defecto
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_seconds
    
    def _is_expired(self, timestamp: float) -> bool:
        """Verifica si el caché ha expirado"""
        return time.time() - timestamp > self.ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if not self._is_expired(timestamp):
                return data
            else:
                # Eliminar entrada expirada
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Guarda un valor en el caché"""
        self.cache[key] = (value, time.time())
    
    def clear(self, key: Optional[str] = None) -> None:
        """Limpia el caché"""
        if key:
            self.cache.pop(key, None)
        else:
            self.cache.clear()
    
    def clear_user_data(self, user_id: int) -> None:
        """Limpia todos los datos de un usuario específico"""
        keys_to_remove = [k for k in self.cache.keys() if k.startswith(f"user_{user_id}_")]
        for key in keys_to_remove:
            del self.cache[key]

# Instancia global del caché
user_cache = UserCache(ttl_seconds=300)  # 5 minutos

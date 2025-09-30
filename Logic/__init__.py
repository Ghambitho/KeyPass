# -*- coding: utf-8 -*-
"""Módulo principal de Logic con optimizaciones automáticas"""
import config

# Importar módulos optimizados o normales según configuración
if config.USE_OPTIMIZED_MODULES:
    try:
        from Logic import storage_optimized as storage
        from Logic import login_optimized as login
        print("Using optimized modules for better performance")
    except ImportError as e:
        print(f"Optimized modules not available, using standard modules: {e}")
        from Logic import storage
        from Logic import login
else:
    from Logic import storage
    from Logic import login
    print("Using standard modules")

# Re-exportar funciones principales
from Logic import session
from Logic import encryption
from Logic import password_generator

__all__ = ['storage', 'login', 'session', 'encryption', 'password_generator']

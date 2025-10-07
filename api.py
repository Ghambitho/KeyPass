#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada para Render - api.py en la raíz
"""

# Importar la app desde el módulo backend
from backend.api import app

# Esto permite que Render encuentre "app" en el módulo "api" (este archivo)
__all__ = ['app']
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada para Render - compatible con cualquier estructura
"""

try:
    # Intentar importar desde backend/ (estructura nueva)
    from backend.api import app
except ImportError:
    try:
        # Fallback: importar desde api/ (estructura original)
        from api.api import app
    except ImportError:
        # Último recurso: crear una app mínima
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/")
        def root():
            return {"error": "No se pudo cargar la aplicación principal"}

# Esto permite que Render encuentre "app" en el módulo "api" (este archivo)
__all__ = ['app']
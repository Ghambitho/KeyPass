#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para KeyPass API
"""

if __name__ == "__main__":
    import uvicorn
    from backend.api import app
    
    # Para desarrollo local
    uvicorn.run(app, host="0.0.0.0", port=8000)
else:
    # Para producción (importado por Render)
    from backend.api import app
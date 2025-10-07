# KeyPass - Deploy Instructions

## Últimas correcciones aplicadas:

1. **Versiones compatibles**: Downgrade a versiones estables de FastAPI/Pydantic que funcionan con Python 3.11
2. **Forzar Python 3.11**: Agregado `.python-version` para que Render use la versión correcta
3. **Importación robusta**: `api.py` ahora maneja múltiples estructuras de carpetas
4. **Dependencias estables**: Cryptography 3.4.8 y email-validator 1.3.1 para evitar problemas de compilación

## Para deployar:

```bash
git add .
git commit -m "Fix Python version compatibility for Render deployment"
git push
```

## Configuración en Render:

- **Build Command**: `pip install -r requirements.txt`  
- **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
- **Python Version**: Se forzará a 3.11.9 automáticamente

## Variables de entorno necesarias:

```
DATABASE_URL=postgresql://...
JWT_SECRET=tu-clave-secreta
ENV=production
DEBUG=false
```
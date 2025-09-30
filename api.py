# -*- coding: utf-8 -*-
"""
KeyPass API - Servidor FastAPI para Render
API intermedia para conectar el .exe con la base de datos PostgreSQL
"""

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import datetime, timedelta
import os
import logging
from typing import Optional

# Importar lógica de KeyPass
from Logic.login import verify_user, get_user_id, create_user, user_exists
from Logic.storage import _load_all_passwords, save_password, delete_password
from Logic.encryption import get_encryption_key
from Logic.password_generator import generate_password
import config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="KeyPass API",
    description="API intermedia para KeyPass - Gestor de Contraseñas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS para permitir conexiones desde tu .exe
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar IPs específicas
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

security = HTTPBearer()

def create_token(user_id: int) -> str:
    """Crear token JWT para el usuario"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Verificar token JWT y devolver user_id"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds()
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    return response

# Endpoints de la API

@app.get("/")
async def root():
    """Endpoint raíz - información de la API"""
    return {
        "message": "KeyPass API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check para Render"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/auth/login")
async def api_login(request: dict):
    """Autenticar usuario"""
    try:
        email = request.get("email", "").strip()
        password = request.get("password", "").strip()
        
        if not email or not password:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Email y contraseña requeridos"}
            )
        
        if verify_user(email, password):
            user_id = get_user_id(email)
            token = create_token(user_id)
            return {
                "success": True,
                "token": token,
                "user_id": user_id,
                "expires_in": ACCESS_TOKEN_EXPIRE_HOURS * 3600
            }
        else:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Credenciales inválidas"}
            )
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error interno del servidor"}
        )

@app.post("/api/auth/register")
async def api_register(request: dict):
    """Registrar nuevo usuario"""
    try:
        email = request.get("email", "").strip()
        username = request.get("username", "").strip()
        password = request.get("password", "").strip()
        
        if not all([email, username, password]):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Todos los campos son requeridos"}
            )
        
        if user_exists(email=email, usuario=username):
            return JSONResponse(
                status_code=409,
                content={"success": False, "message": "Email o usuario ya existe"}
            )
        
        user_id = create_user(email, username, password)
        token = create_token(user_id)
        
        return {
            "success": True,
            "token": token,
            "user_id": user_id,
            "message": "Usuario creado exitosamente"
        }
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error interno del servidor"}
        )

@app.get("/api/passwords")
async def api_get_passwords(user_id: int = Depends(verify_token)):
    """Obtener todas las contraseñas del usuario"""
    try:
        passwords = _load_all_passwords(user_id)
        return {
            "success": True,
            "passwords": passwords,
            "count": len(passwords)
        }
    except Exception as e:
        logger.error(f"Error obteniendo contraseñas: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error interno del servidor"}
        )

@app.post("/api/passwords")
async def api_save_password(request: dict, user_id: int = Depends(verify_token)):
    """Guardar nueva contraseña"""
    try:
        site = request.get("site", "").strip()
        username = request.get("username", "").strip()
        password = request.get("password", "").strip()
        
        if not all([site, username, password]):
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Todos los campos son requeridos"}
            )
        
        success = save_password(site, username, password, user_id)
        if success:
            return {"success": True, "message": "Contraseña guardada exitosamente"}
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Error al guardar contraseña"}
            )
    except Exception as e:
        logger.error(f"Error guardando contraseña: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error interno del servidor"}
        )

@app.delete("/api/passwords/{password_id}")
async def api_delete_password(password_id: int, user_id: int = Depends(verify_token)):
    """Eliminar contraseña"""
    try:
        success = delete_password(password_id, user_id)
        if success:
            return {"success": True, "message": "Contraseña eliminada exitosamente"}
        else:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Contraseña no encontrada"}
            )
    except Exception as e:
        logger.error(f"Error eliminando contraseña: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error interno del servidor"}
        )

@app.post("/api/generate-password")
async def api_generate_password(request: dict, user_id: int = Depends(verify_token)):
    """Generar contraseña aleatoria"""
    try:
        length = request.get("length", config.DEFAULT_PASSWORD_LENGTH)
        include_uppercase = request.get("include_uppercase", True)
        include_numbers = request.get("include_numbers", True)
        include_symbols = request.get("include_symbols", True)
        
        # Validar longitud
        length = max(config.MIN_PASSWORD_LENGTH, min(config.MAX_PASSWORD_LENGTH, int(length)))
        
        password = generate_password(
            length, include_uppercase, include_numbers, include_symbols
        )
        
        return {
            "success": True,
            "password": password,
            "length": length
        }
    except Exception as e:
        logger.error(f"Error generando contraseña: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error interno del servidor"}
        )

@app.get("/api/user/profile")
async def api_get_profile(user_id: int = Depends(verify_token)):
    """Obtener perfil del usuario"""
    try:
        from Logic.login import get_user_profile
        profile = get_user_profile(user_id)
        if profile:
            return {
                "success": True,
                "profile": {
                    "user_id": user_id,
                    "email": profile[0],
                    "username": profile[1]
                }
            }
        else:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Usuario no encontrado"}
            )
    except Exception as e:
        logger.error(f"Error obteniendo perfil: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error interno del servidor"}
        )

# Manejo de errores global
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Error interno del servidor"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

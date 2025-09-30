# -*- coding: utf-8 -*-
"""
Cliente API para KeyPass - Conecta con la API de Render
"""

import requests
import json
from typing import Optional, Dict, List
import config

class KeyPassAPIClient:
    """Cliente para conectar con la API de KeyPass en Render"""
    
    def __init__(self):
        self.api_url = config.API_BASE_URL.rstrip('/')
        self.timeout = config.API_TIMEOUT
        self.token: Optional[str] = None
        self.user_id: Optional[int] = None
        self.user_email: Optional[str] = None
        self.user_username: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Obtiene los headers para las peticiones"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def register(self, email: str, usuario: str, password: str) -> bool:
        """Registrar nuevo usuario"""
        try:
            response = requests.post(
                f"{self.api_url}/api/auth/register",
                json={
                    "email": email,
                    "username": usuario,  # La API espera 'username', no 'usuario'
                    "password": password
                },
                headers=self._get_headers(),
                timeout=self.timeout
            )
            if response.status_code == 200:
                # Almacenar información del usuario para el registro
                self.user_email = email
                self.user_username = usuario
                return True
            return False
        except Exception:
            return False
    
    def login(self, login: str, password: str) -> bool:
        """Iniciar sesión"""
        try:
            response = requests.post(
                f"{self.api_url}/api/auth/login",
                json={
                    "email": login,  # La API espera 'email', no 'login'
                    "password": password
                },
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.token = data.get("token")
                    self.user_id = data.get("user_id")
                    # Almacenar información del usuario para el login
                    self.user_email = login  # El login es el email
                    return True
            return False
        except Exception:
            return False
    
    def get_passwords(self) -> List[Dict]:
        """Obtener todas las contraseñas del usuario"""
        try:
            response = requests.get(
                f"{self.api_url}/passwords",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("passwords", [])
            return []
        except Exception:
            return []
    
    def save_password(self, site: str, username: str, password: str) -> bool:
        """Guardar nueva contraseña"""
        try:
            response = requests.post(
                f"{self.api_url}/passwords",
                json={
                    "site": site,
                    "username": username,
                    "password": password
                },
                headers=self._get_headers(),
                timeout=self.timeout
            )
            return response.status_code == 201
        except Exception:
            return False
    
    def delete_password(self, password_id: int) -> bool:
        """Eliminar contraseña"""
        try:
            response = requests.delete(
                f"{self.api_url}/passwords/{password_id}",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def update_profile(self, email: str, usuario: str) -> bool:
        """Actualizar perfil del usuario"""
        try:
            response = requests.put(
                f"{self.api_url}/profile",
                json={
                    "email": email,
                    "usuario": usuario
                },
                headers=self._get_headers(),
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def logout(self):
        """Cerrar sesión"""
        self.token = None
        self.user_id = None
        self.user_email = None
        self.user_username = None
    
    def is_logged_in(self) -> bool:
        """Verificar si hay sesión activa"""
        return self.token is not None and self.user_id is not None

# -*- coding: utf-8 -*-
"""
Ejemplo de cliente para conectar el .exe con la API
Este archivo muestra cómo modificar tu aplicación PyQt6 para usar la API
"""

import requests
import json
from typing import Optional, Dict, List

class KeyPassAPIClient:
    """Cliente para conectar con la API de KeyPass"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip('/')
        self.token: Optional[str] = None
        self.user_id: Optional[int] = None
    
    def login(self, email: str, password: str) -> bool:
        """Iniciar sesión en la API"""
        try:
            response = requests.post(
                f"{self.api_url}/api/auth/login",
                json={"email": email, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.token = data["token"]
                    self.user_id = data["user_id"]
                    return True
            
            return False
        except Exception as e:
            print(f"Error en login: {e}")
            return False
    
    def register(self, email: str, username: str, password: str) -> bool:
        """Registrar nuevo usuario"""
        try:
            response = requests.post(
                f"{self.api_url}/api/auth/register",
                json={"email": email, "username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.token = data["token"]
                    self.user_id = data["user_id"]
                    return True
            
            return False
        except Exception as e:
            print(f"Error en registro: {e}")
            return False
    
    def get_passwords(self) -> List[Dict]:
        """Obtener todas las contraseñas del usuario"""
        if not self.token:
            return []
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.api_url}/api/passwords",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("passwords", [])
            
            return []
        except Exception as e:
            print(f"Error obteniendo contraseñas: {e}")
            return []
    
    def save_password(self, site: str, username: str, password: str) -> bool:
        """Guardar nueva contraseña"""
        if not self.token:
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.api_url}/api/passwords",
                json={"site": site, "username": username, "password": password},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("success", False)
            
            return False
        except Exception as e:
            print(f"Error guardando contraseña: {e}")
            return False
    
    def delete_password(self, password_id: int) -> bool:
        """Eliminar contraseña"""
        if not self.token:
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(
                f"{self.api_url}/api/passwords/{password_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("success", False)
            
            return False
        except Exception as e:
            print(f"Error eliminando contraseña: {e}")
            return False
    
    def generate_password(self, length: int = 14, include_uppercase: bool = True, 
                         include_numbers: bool = True, include_symbols: bool = True) -> Optional[str]:
        """Generar contraseña aleatoria"""
        if not self.token:
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.api_url}/api/generate-password",
                json={
                    "length": length,
                    "include_uppercase": include_uppercase,
                    "include_numbers": include_numbers,
                    "include_symbols": include_symbols
                },
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("password")
            
            return None
        except Exception as e:
            print(f"Error generando contraseña: {e}")
            return None
    
    def get_profile(self) -> Optional[Dict]:
        """Obtener perfil del usuario"""
        if not self.token:
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.api_url}/api/user/profile",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("profile")
            
            return None
        except Exception as e:
            print(f"Error obteniendo perfil: {e}")
            return None
    
    def logout(self):
        """Cerrar sesión"""
        self.token = None
        self.user_id = None
    
    def is_authenticated(self) -> bool:
        """Verificar si está autenticado"""
        return self.token is not None and self.user_id is not None


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar URL de tu API en Render
    API_URL = "https://your-keypass-api.onrender.com"
    
    # Crear cliente
    client = KeyPassAPIClient(API_URL)
    
    # Ejemplo de login
    if client.login("user@example.com", "password"):
        print("✅ Login exitoso")
        
        # Obtener contraseñas
        passwords = client.get_passwords()
        print(f"📋 Contraseñas encontradas: {len(passwords)}")
        
        # Generar contraseña
        new_password = client.generate_password(length=16)
        if new_password:
            print(f"🔑 Contraseña generada: {new_password}")
        
        # Guardar contraseña
        if client.save_password("example.com", "user", new_password):
            print("💾 Contraseña guardada")
        
    else:
        print("❌ Error en login")

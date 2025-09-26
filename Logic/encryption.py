# -*- coding: utf-8 -*-
from pathlib import Path
from cryptography.fernet import Fernet
import keyring
import getpass

BASE = Path(__file__).resolve().parent.parent

def get_encryption_key():
    """
    Obtiene la clave de encriptación desde el keyring del sistema.
    Si no existe, la genera y la guarda en el keyring.
    """
    service_name = "KeyPass"
    username = getpass.getuser()
    
    try:
        # Intentar obtener clave del keyring
        key_str = keyring.get_password(service_name, username)
        
        if key_str:
            # Convertir string a bytes
            key = key_str.encode('utf-8')
        else:
            # Generar nueva clave
            key = Fernet.generate_key()
            # Guardar en keyring
            keyring.set_password(service_name, username, key.decode('utf-8'))
            print("✅ Encryption key created and saved to system keyring")
            
    except Exception as e:
        # Si keyring falla, mostrar error claro
        raise Exception(f"Failed to access system keyring: {e}. Please ensure keyring is properly configured.")
    
    return Fernet(key)

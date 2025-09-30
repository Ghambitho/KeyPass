# -*- coding: utf-8 -*-
from pathlib import Path
import json, time
from Logic.encryption import AESEncryption
import keyring
import getpass
import config
import os
import base64

BASE = Path(__file__).resolve().parent.parent
DB = BASE / config.DB_PATH
DB.mkdir(exist_ok=True)
SESSION_FILE = DB / config.SESSION_FILE

def _get_or_create_key() -> bytes:
    """Obtiene la clave de sesión desde el keyring del sistema"""
    service_name = "KeyPass-Session"
    username = getpass.getuser()
    
    try:
        key_str = keyring.get_password(service_name, username)
        
        if key_str:
            key = base64.b64decode(key_str)
        else:
            key = os.urandom(32)
            keyring.set_password(service_name, username, base64.b64encode(key).decode('utf-8'))
            print("✅ AES session key created and saved to system keyring")
            
    except Exception as e:
        raise Exception(f"Failed to access system keyring for sessions: {e}. Please ensure keyring is properly configured.")
    
    return key

def _aes_encryption() -> AESEncryption:
    return AESEncryption(_get_or_create_key())

def save_session(user_id: int, ttl_days: int = None) -> None:
    """Guarda la sesión del usuario por un tiempo (TTL) dado en días."""
    if ttl_days is None:
        ttl_days = config.DEFAULT_TTL_DAYS
    payload = {"user": user_id, "ts": int(time.time()), "ttl": ttl_days * 86400}
    token = _aes_encryption().encrypt(json.dumps(payload).encode("utf-8"))
    SESSION_FILE.write_bytes(token)

def load_session() -> dict | None:
    """Devuelve el payload si existe y no ha expirado; si no, None."""
    if not SESSION_FILE.exists():
        return None
    try:
        data = _aes_encryption().decrypt(SESSION_FILE.read_bytes())
        payload = json.loads(data.decode("utf-8"))
        ts = payload.get("ts", 0)
        ttl = payload.get("ttl", 0)
        if int(time.time()) - ts <= int(ttl):
            return payload
        clear_session()
        return None
    except Exception:
        clear_session()
        return None

def has_session() -> bool:
    return load_session() is not None

def clear_session() -> None:
    try:
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
    except Exception:
        pass

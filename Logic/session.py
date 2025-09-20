# -*- coding: utf-8 -*-
"""
Manejo de sesión persistente (Recordar sesión) usando Fernet.
Guarda un pequeño JSON cifrado con el identificador del usuario y fecha.
Archivos:
  - session.key: clave Fernet
  - session.bin: sesión cifrada
"""
from pathlib import Path
import json, time
from cryptography.fernet import Fernet

BASE = Path(__file__).resolve().parent.parent  # raíz del proyecto
DB = BASE / "db"
DB.mkdir(exist_ok=True)

KEY_FILE = DB / "session.key"
SESSION_FILE = DB / "session.bin"

def _get_or_create_key() -> bytes:
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    return key

def _fernet() -> Fernet:
    return Fernet(_get_or_create_key())

def save_session(user_id: str, ttl_days: int = 30) -> None:
    """Guarda la sesión del usuario por un tiempo (TTL) dado en días."""
    payload = {"user": user_id, "ts": int(time.time()), "ttl": ttl_days * 86400}
    token = _fernet().encrypt(json.dumps(payload).encode("utf-8"))
    SESSION_FILE.write_bytes(token)

def load_session() -> dict | None:
    """Devuelve el payload si existe y no ha expirado; si no, None."""
    if not SESSION_FILE.exists():
        return None
    try:
        data = _fernet().decrypt(SESSION_FILE.read_bytes(), ttl=None)
        payload = json.loads(data.decode("utf-8"))
        ts = payload.get("ts", 0)
        ttl = payload.get("ttl", 0)
        if int(time.time()) - ts <= int(ttl):
            return payload
        # expiró
        clear_session()
        return None
    except Exception:
        # token inválido/clave distinta
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

# -*- coding: utf-8 -*-
import json
from pathlib import Path
from Logic.encryption import get_encryption_key

BASE = Path(__file__).resolve().parent.parent
ENCRYPTED_FILE = BASE / "passwords.enc"

def _load_all_passwords():
    if not ENCRYPTED_FILE.exists():
        return []
    f = get_encryption_key()
    data = f.decrypt(ENCRYPTED_FILE.read_bytes())
    return json.loads(data.decode('utf-8'))

def _save_all_passwords(passwords):
    f = get_encryption_key()
    data = json.dumps(passwords, indent=4, ensure_ascii=False).encode('utf-8')
    ENCRYPTED_FILE.write_bytes(f.encrypt(data))

def save_password(sitio, usuario, contraseña):
    pwds = _load_all_passwords()
    pwds.append({"sitio": sitio, "usuario": usuario, "contraseña": contraseña})
    _save_all_passwords(pwds)

def get_password_for_site(sitio, usuario):
    for entry in _load_all_passwords():
        if entry["sitio"] == sitio and entry["usuario"] == usuario:
            return entry["contraseña"]
    return None

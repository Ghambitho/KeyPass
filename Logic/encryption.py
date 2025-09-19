# -*- coding: utf-8 -*-
from pathlib import Path
from cryptography.fernet import Fernet

BASE = Path(__file__).resolve().parent.parent
KEY_FILE = BASE / "secret.key"

def get_encryption_key():
    if KEY_FILE.exists():
        key = KEY_FILE.read_bytes()
    else:
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
    return Fernet(key)

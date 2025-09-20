# -*- coding: utf-8 -*-
import os
import hmac
import sqlite3
import hashlib
from pathlib import Path
from typing import Optional, Tuple

# Ruta al mismo .db que usa storage.py
BASE = Path(__file__).resolve().parent.parent
DB_FILE = BASE / "db" / "keypass.db"

# Formato de almacenamiento de contraseña:
# pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>
ALGO = "pbkdf2_sha256"
DEFAULT_ITER = 200_000
SALT_BYTES = 16


# ---------------------- helpers de DB ----------------------
def _conn():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ---------------------- helpers de hash ----------------------
def _pbkdf2(password: str, salt: bytes, iterations: int = DEFAULT_ITER) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def _encode_record(iterations: int, salt: bytes, dk: bytes) -> str:
    return f"{ALGO}${iterations}${salt.hex()}${dk.hex()}"


def _decode_record(record: str) -> Optional[Tuple[int, bytes, bytes]]:
    """
    Devuelve (iterations, salt_bytes, hash_bytes) o None si no es formato PBKDF2.
    """
    parts = record.split("$")
    if len(parts) == 4 and parts[0] == ALGO:
        try:
            iterations = int(parts[1])
            salt = bytes.fromhex(parts[2])
            dk = bytes.fromhex(parts[3])
            return iterations, salt, dk
        except Exception:
            return None
    return None


def _sha256_hex(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------------------- API pública ----------------------
def user_exists(email: str = "", usuario: str = "") -> bool:
    email = (email or "").strip()
    usuario = (usuario or "").strip()
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM login WHERE email=? OR usuario=? LIMIT 1",
        (email, usuario),
    )
    found = cur.fetchone() is not None
    conn.close()
    return found


def create_user(email: str, usuario: str, password: str) -> int:
    """
    Crea un usuario con contraseña PBKDF2 y devuelve el id insertado.
    Lanza sqlite3.IntegrityError si hay duplicados (si tienes UNIQUE en email/usuario).
    """
    email = email.strip()
    usuario = usuario.strip()

    salt = os.urandom(SALT_BYTES)
    dk = _pbkdf2(password, salt, DEFAULT_ITER)
    record = _encode_record(DEFAULT_ITER, salt, dk)

    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO login(email, usuario, pass) VALUES(?,?,?)",
        (email, usuario, record),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def verify_user(login: str, password: str) -> bool:
    """
    Verifica credenciales. Acepta email o usuario en 'login'.
    - Si detecta formato antiguo (texto plano o sha256), migra automáticamente a PBKDF2.
    """
    login = login.strip()
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, pass FROM login WHERE email=? OR usuario=? LIMIT 1",
        (login, login),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return False

    user_id, stored = row

    # Caso 1: formato PBKDF2 actual
    parsed = _decode_record(stored)
    if parsed is not None:
        iterations, salt, good_dk = parsed
        candidate = _pbkdf2(password, salt, iterations)
        ok = hmac.compare_digest(candidate, good_dk)
        conn.close()
        return ok

    # Caso 2: posible SHA-256 legacy (64 hex)
    if len(stored) == 64 and all(c in "0123456789abcdef" for c in stored.lower()):
        ok = hmac.compare_digest(_sha256_hex(password), stored)
        # Migramos a PBKDF2 si coincide
        if ok:
            _migrate_to_pbkdf2(user_id, password, conn)
        conn.close()
        return ok

    # Caso 3: texto plano legacy
    ok = hmac.compare_digest(password, stored)
    if ok:
        _migrate_to_pbkdf2(user_id, password, conn)
    conn.close()
    return ok


def change_password(login: str, old_password: str, new_password: str) -> bool:
    """
    Cambia contraseña si old_password es correcta. Devuelve True/False.
    """
    if not verify_user(login, old_password):
        return False
    conn = _conn()
    cur = conn.cursor()
    # Buscamos id nuevamente (verify_user cerró la conexión)
    cur.execute(
        "SELECT id FROM login WHERE email=? OR usuario=? LIMIT 1",
        (login, login),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    user_id = row[0]
    _migrate_to_pbkdf2(user_id, new_password, conn)
    conn.close()
    return True


# ---------------------- utilidades internas ----------------------
def _migrate_to_pbkdf2(user_id: int, password: str, conn: sqlite3.Connection) -> None:
    """Actualiza la fila a formato PBKDF2 en la conexión abierta."""
    salt = os.urandom(SALT_BYTES)
    dk = _pbkdf2(password, salt, DEFAULT_ITER)
    record = _encode_record(DEFAULT_ITER, salt, dk)
    cur = conn.cursor()
    cur.execute("UPDATE login SET pass=? WHERE id=?", (record, user_id))
    conn.commit()

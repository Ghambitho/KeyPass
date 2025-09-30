# -*- coding: utf-8 -*-
import os
import hmac
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
from typing import Optional, Tuple
import config

ALGO = config.ENCRYPTION_ALGORITHM
DEFAULT_ITER = config.DEFAULT_ITERATIONS
SALT_BYTES = config.SALT_BYTES

def _conn():
    """Conexión a PostgreSQL"""
    return psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        port=config.DB_PORT,
        sslmode='require'
    )
def _pbkdf2(password: str, salt: bytes, iterations: int = DEFAULT_ITER) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)

def _encode_record(iterations: int, salt: bytes, dk: bytes) -> str:
    return f"{ALGO}${iterations}${salt.hex()}${dk.hex()}"

def _decode_record(record: str) -> Optional[Tuple[int, bytes, bytes]]:
    """Devuelve (iterations, salt_bytes, hash_bytes) o None si no es formato PBKDF2."""
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

def user_exists(email: str = "", usuario: str = "") -> bool:
    email = (email or "").strip()
    usuario = (usuario or "").strip()
    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM login WHERE email=%s OR usuario=%s LIMIT 1",
            (email, usuario),
        )
        found = cur.fetchone() is not None
        return found
    finally:
        conn.close()


def create_user(email: str, usuario: str, password: str) -> int:
    email = email.strip().lower()
    usuario = usuario.strip().lower()

    salt = os.urandom(SALT_BYTES)
    dk = _pbkdf2(password, salt, DEFAULT_ITER)
    record = _encode_record(DEFAULT_ITER, salt, dk)

    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO login(email, usuario, pass) VALUES(%s,%s,%s) RETURNING id",
            (email, usuario, record),
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        conn.close()


def verify_user(login: str, password: str) -> bool:
    """Verifica credenciales. Acepta email o usuario en 'login'."""
    login = login.strip()
    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, pass FROM login WHERE email=%s OR usuario=%s LIMIT 1",
            (login, login),
        )
        row = cur.fetchone()
        if not row:
            return False

        user_id, stored = row

        parsed = _decode_record(stored)
        if parsed is not None:
            iterations, salt, good_dk = parsed
            candidate = _pbkdf2(password, salt, iterations)
            ok = hmac.compare_digest(candidate, good_dk)
            return ok

        if len(stored) == 64 and all(c in "0123456789abcdef" for c in stored.lower()):
            ok = hmac.compare_digest(_sha256_hex(password), stored)
            if ok:
                _migrate_to_pbkdf2(user_id, password, conn)
            return ok

        ok = hmac.compare_digest(password, stored)
        if ok:
            _migrate_to_pbkdf2(user_id, password, conn)
        return ok
    finally:
        conn.close()


def _migrate_to_pbkdf2(user_id: int, password: str, conn: psycopg2.extensions.connection) -> None:
    """Actualiza la fila a formato PBKDF2 en la conexión abierta."""
    salt = os.urandom(SALT_BYTES)
    dk = _pbkdf2(password, salt, DEFAULT_ITER)
    record = _encode_record(DEFAULT_ITER, salt, dk)
    cur = conn.cursor()
    cur.execute("UPDATE login SET pass=%s WHERE id=%s", (record, user_id))
    conn.commit()

def get_user_profile(user_id: int) -> tuple | None:
    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT email, usuario FROM login WHERE id=%s",
            (user_id,)
        )
        row = cur.fetchone()
        return row
    finally:
        conn.close()


def update_user_profile(user_id: int, new_email: str, new_usuario: str) -> bool:
    """Actualiza el perfil del usuario"""
    try:
        new_email = new_email.strip()
        new_usuario = new_usuario.strip()
        
        if not new_email or not new_usuario:
            return False
        
        conn = _conn()
        try:
            cur = conn.cursor()
            
            # Verificar que no esté en uso por otro usuario
            cur.execute(
                "SELECT id FROM login WHERE (email=%s OR usuario=%s) AND id!=%s",
                (new_email, new_usuario, user_id)
            )
            if cur.fetchone():
                return False
            
            # Actualizar
            cur.execute(
                "UPDATE login SET email=%s, usuario=%s WHERE id=%s",
                (new_email, new_usuario, user_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()
    except Exception:
        return False
    
def get_user_id(login: str) -> int | None:
    """
    Devuelve el id del usuario para email o usuario dado; None si no existe.
    """
    login = (login or "").strip().lower()
    if not login:
        return None
    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM login WHERE email=%s OR usuario=%s LIMIT 1", (login, login))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()
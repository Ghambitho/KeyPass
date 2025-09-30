# -*- coding: utf-8 -*-
"""Versión optimizada del login con pool de conexiones y caché"""
import hashlib
import hmac
import os
from Logic.db_pool import db_pool
from Logic.cache import user_cache
import config

def _conn():
    """Obtiene conexión del pool"""
    return db_pool.get_connection()

def verify_user(login, password):
    """Verifica usuario con caché de perfil"""
    login = (login or "").strip().lower()
    if not login or not password:
        return False
    
    conn = _conn()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, pass FROM login WHERE email=%s OR usuario=%s LIMIT 1", (login, login))
        row = cur.fetchone()
        
        if not row:
            return False
        
        user_id, stored_hash = row
        return _verify_password(password, stored_hash)
        
    except Exception as e:
        print(f"Error verifying user: {e}")
        return False
    finally:
        db_pool.return_connection(conn)

def get_user_id(login):
    """Obtiene ID del usuario con caché"""
    login = (login or "").strip().lower()
    if not login:
        return None
    
    cache_key = f"user_id_{login}"
    cached_id = user_cache.get(cache_key)
    if cached_id is not None:
        return cached_id
    
    conn = _conn()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM login WHERE email=%s OR usuario=%s LIMIT 1", (login, login))
        row = cur.fetchone()
        user_id = row[0] if row else None
        
        if user_id:
            user_cache.set(cache_key, user_id)
        
        return user_id
        
    except Exception as e:
        print(f"Error getting user ID: {e}")
        return None
    finally:
        db_pool.return_connection(conn)

def get_user_profile(user_id):
    """Obtiene perfil del usuario con caché"""
    cache_key = f"user_{user_id}_profile"
    cached_profile = user_cache.get(cache_key)
    if cached_profile is not None:
        return cached_profile
    
    conn = _conn()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT email, usuario FROM login WHERE id=%s", (user_id,))
        row = cur.fetchone()
        
        if row:
            user_cache.set(cache_key, row)
            return row
        return None
        
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return None
    finally:
        db_pool.return_connection(conn)

def create_user(email, usuario, password):
    """Crea usuario y limpia caché relacionado"""
    email = (email or "").strip().lower()
    usuario = (usuario or "").strip()
    
    if not email or not usuario or not password:
        return None
    
    conn = _conn()
    if not conn:
        return None
    
    try:
        # Verificar si ya existe
        cur = conn.cursor()
        cur.execute("SELECT id FROM login WHERE email=%s OR usuario=%s LIMIT 1", (email, usuario))
        if cur.fetchone():
            return None
        
        # Crear hash de contraseña
        password_hash = _hash_password(password)
        
        # Insertar usuario
        cur.execute(
            "INSERT INTO login (email, usuario, pass) VALUES (%s, %s, %s) RETURNING id",
            (email, usuario, password_hash)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        
        # Limpiar caché relacionado
        user_cache.clear(f"user_id_{email}")
        user_cache.clear(f"user_id_{usuario}")
        
        return user_id
        
    except Exception as e:
        print(f"Error creating user: {e}")
        conn.rollback()
        return None
    finally:
        db_pool.return_connection(conn)

def _hash_password(password):
    """Crea hash seguro de la contraseña"""
    salt = os.urandom(config.SALT_BYTES)
    pwd_hash = hashlib.pbkdf2_hmac(
        config.ENCRYPTION_ALGORITHM.split('_')[0],
        password.encode('utf-8'),
        salt,
        config.DEFAULT_ITERATIONS
    )
    return salt + pwd_hash

def _verify_password(password, stored_hash):
    """Verifica contraseña contra hash almacenado"""
    try:
        salt = stored_hash[:config.SALT_BYTES]
        stored_pwd_hash = stored_hash[config.SALT_BYTES:]
        
        pwd_hash = hashlib.pbkdf2_hmac(
            config.ENCRYPTION_ALGORITHM.split('_')[0],
            password.encode('utf-8'),
            salt,
            config.DEFAULT_ITERATIONS
        )
        
        return hmac.compare_digest(pwd_hash, stored_pwd_hash)
    except Exception:
        return False

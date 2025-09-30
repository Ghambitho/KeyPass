# -*- coding: utf-8 -*-
"""Versión optimizada del storage con pool de conexiones y caché"""
from Logic.encryption import get_encryption_key
from Logic.db_pool import db_pool
from Logic.cache import user_cache
from psycopg2.extras import RealDictCursor
import config

def _load_all_passwords(user_id):
    """Carga todas las contraseñas con caché"""
    cache_key = f"user_{user_id}_passwords"
    
    # Verificar caché primero
    cached_data = user_cache.get(cache_key)
    if cached_data is not None:
        print(f"Cache hit for user {user_id} passwords")
        return cached_data
    
    # Si no está en caché, cargar desde BD
    conn = db_pool.get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, site, user_name, pass FROM keypass WHERE user_id=%s ORDER BY id DESC", (user_id,))
        rows = cur.fetchall()

        f = get_encryption_key()
        salida = []
        for row in rows:
            try:
                # Convertir memoryview a bytes si es necesario
                pass_data = row['pass']
                if isinstance(pass_data, memoryview):
                    pass_data = bytes(pass_data)
                pwd = f.decrypt(pass_data).decode('utf-8')
            except Exception as e:
                print(f"Decryption error for row {row['id']}: {e}")
                pwd = "<decryption-error>"
            salida.append({
                "id": row['id'], 
                "sitio": row['site'], 
                "usuario": row['user_name'], 
                "contraseña": pwd
            })
        
        # Guardar en caché
        user_cache.set(cache_key, salida)
        print(f"Cached passwords for user {user_id}")
        return salida
        
    except Exception as e:
        print(f"Error loading passwords: {e}")
        return []
    finally:
        db_pool.return_connection(conn)

def save_password(site, user_name, password, user_id):
    """Guarda una contraseña y limpia el caché"""
    conn = db_pool.get_connection()
    if not conn:
        return False
    
    try:
        f = get_encryption_key()
        encrypted = f.encrypt(password.encode('utf-8'))
        
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO keypass (site, user_name, pass, user_id) VALUES (%s, %s, %s, %s)",
            (site, user_name, encrypted, user_id)
        )
        conn.commit()
        
        # Limpiar caché del usuario
        user_cache.clear_user_data(user_id)
        print(f"Cleared cache for user {user_id} after saving password")
        return True
        
    except Exception as e:
        print(f"Error saving password: {e}")
        conn.rollback()
        return False
    finally:
        db_pool.return_connection(conn)

def delete_password(record_id, user_id):
    """Elimina una contraseña y limpia el caché"""
    conn = db_pool.get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM keypass WHERE id=%s AND user_id=%s", (record_id, user_id))
        conn.commit()
        
        # Limpiar caché del usuario
        user_cache.clear_user_data(user_id)
        print(f"Cleared cache for user {user_id} after deleting password")
        return cur.rowcount > 0
        
    except Exception as e:
        print(f"Error deleting password: {e}")
        conn.rollback()
        return False
    finally:
        db_pool.return_connection(conn)

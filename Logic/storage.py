# -*- coding: utf-8 -*-
from Logic.encryption import get_encryption_key
import sqlite3
from pathlib import Path
import config

# Directorio de datos local
DATA_DIR = Path(__file__).resolve().parent.parent / "db"
DATA_DIR.mkdir(exist_ok=True)

# Archivo de base de datos SQLite
DB_FILE = DATA_DIR / "keypass.db"

def _conn():
    """Conexión a SQLite"""
    return sqlite3.connect(DB_FILE)


def _load_all_passwords(user_id):
    """Carga todas las contraseñas de un usuario desde SQLite"""
    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, site, user_name, pass FROM keypass WHERE user_id=? ORDER BY id DESC", (user_id,))
        rows = cur.fetchall()

        f = get_encryption_key()
        salida = []
        for row in rows:
            try:
                pwd = f.decrypt(row[3]).decode('utf-8')  # row[3] es la columna 'pass'
            except Exception:
                pwd = "<decryption-error>"
            salida.append({
                "id": row[0], 
                "sitio": row[1], 
                "usuario": row[2], 
                "contraseña": pwd
            })
        return salida
    except Exception:
        return []
    finally:
        conn.close()

def delete_password(record_id, user_id):
    """Elimina una contraseña de SQLite"""
    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM keypass WHERE id=? AND user_id=?", (record_id, user_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def save_password(sitio, usuario, contraseña, user_id):
    """Guarda una contraseña en SQLite"""
    try:
        f = get_encryption_key()
        enc = f.encrypt(contraseña.encode('utf-8'))

        conn = _conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO keypass(site, user_name, pass, user_id) VALUES (?,?,?,?)", (sitio, usuario, enc, user_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
    except Exception:
        return False

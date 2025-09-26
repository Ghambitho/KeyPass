# -*- coding: utf-8 -*-
from pathlib import Path
from Logic.encryption import get_encryption_key
import sqlite3
import config

BASE = Path(__file__).resolve().parent.parent
DB_DIR = BASE / config.DB_PATH
DB_DIR.mkdir(exist_ok=True)  # Crear directorio si no existe
DB_FILE = DB_DIR / config.DB_NAME


def _load_all_passwords(user_id):
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        # Filtrar por user_id
        cur.execute("SELECT id, site, User, pass FROM KEYPASS WHERE user_id=? ORDER BY id DESC;", (user_id,))
        rows = cur.fetchall()

        f = get_encryption_key()
        salida = []
        for rec_id, sitio, usuario, enc in rows:
            try:
                pwd = f.decrypt(enc).decode('utf-8')
            except Exception:
                pwd = "<decryption-error>"
            salida.append({"id": rec_id, "sitio": sitio, "usuario": usuario, "contraseña": pwd})
        return salida
    except Exception:
        return []
    finally:
        conn.close()

def delete_password(record_id, user_id):
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM KEYPASS WHERE id=? AND user_id=?;", (record_id, user_id))
        conn.commit()
        ok = cur.rowcount > 0
        return ok
    except Exception:
        return False
    finally:
        conn.close()

def save_password(sitio, usuario, contraseña, user_id):
    try:
        f = get_encryption_key()
        enc = f.encrypt(contraseña.encode('utf-8'))

        conn = sqlite3.connect(DB_FILE)
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO KEYPASS(site, User, pass, user_id) VALUES (?,?,?,?)",
                (sitio, usuario, enc, user_id)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
    except Exception:
        return False


def get_password_for_site(sitio, usuario, user_id):
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT pass FROM KEYPASS
               WHERE site=? AND User=? AND user_id=?
               ORDER BY id DESC LIMIT 1;""",
            (sitio, usuario, user_id)
        )
        row = cur.fetchone()

        if not row:
            return None

        f = get_encryption_key()
        try:
            return f.decrypt(row[0]).decode('utf-8')
        except Exception:
            return None
    except Exception:
        return None
    finally:
        conn.close()

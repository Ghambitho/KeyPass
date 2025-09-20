# -*- coding: utf-8 -*-
from pathlib import Path
from Logic.encryption import get_encryption_key
import sqlite3

BASE = Path(__file__).resolve().parent.parent
DB_FILE = BASE / "db" / "keypass.db"


def _load_all_passwords():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Ahora tienes columna id AUTOINCREMENT → ordenamos por id
    cur.execute("SELECT site, User, pass FROM KEYPASS ORDER BY id DESC;")
    rows = cur.fetchall()
    conn.close()

    f = get_encryption_key()
    salida = []
    for sitio, usuario, enc in rows:
        try:
            pwd = f.decrypt(enc).decode('utf-8')
        except Exception:
            pwd = "<decryption-error>"
        salida.append({"sitio": sitio, "usuario": usuario, "contraseña": pwd})
    return salida


def save_password(sitio, usuario, contraseña):
    f = get_encryption_key()
    enc = f.encrypt(contraseña.encode('utf-8'))

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO KEYPASS(site, User, pass) VALUES (?,?,?)",
        (sitio, usuario, enc)
    )
    conn.commit()
    conn.close()


def get_password_for_site(sitio, usuario):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """SELECT pass FROM KEYPASS
           WHERE site=? AND User=?
           ORDER BY id DESC LIMIT 1;""",
        (sitio, usuario)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    f = get_encryption_key()
    try:
        return f.decrypt(row[0]).decode('utf-8')
    except Exception:
        return None

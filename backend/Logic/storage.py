# -*- coding: utf-8 -*-
from client.Logic.encryption import get_encryption_key
import psycopg2
from psycopg2.extras import RealDictCursor
import backend.config as config

def _conn():
    """Conexión a PostgreSQL (compatible con Supabase)"""
    # Si existe DATABASE_URL (formato Supabase), usarlo
    if config.DATABASE_URL:
        return psycopg2.connect(
            config.DATABASE_URL,
            sslmode='require'
        )
    else:
        # Usar variables individuales
        return psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT,
            sslmode='require'
        )


def _load_all_passwords(user_id):
    conn = _conn()
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
        return salida
    except Exception:
        return []
    finally:
        conn.close()

def delete_password(record_id, user_id):
    conn = _conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM keypass WHERE id=%s AND user_id=%s", (record_id, user_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def save_password(sitio, usuario, contraseña, user_id):
    try:
        f = get_encryption_key()
        enc = f.encrypt(contraseña.encode('utf-8'))

        conn = _conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO keypass(site, user_name, pass, user_id) VALUES (%s,%s,%s,%s)", (sitio, usuario, enc, user_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
    except Exception:
        return False

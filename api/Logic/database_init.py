# -*- coding: utf-8 -*-
"""
Script de inicialización de base de datos para KeyPass
Crea las tablas necesarias en PostgreSQL
"""
import psycopg2
import backend.config as config

def init_database():
    """Inicializa las tablas de la base de datos"""
    try:
        # Conectar a la base de datos usando configuración flexible
        if config.DATABASE_URL:
            conn = psycopg2.connect(
                config.DATABASE_URL,
                sslmode='require'
            )
        else:
            conn = psycopg2.connect(
                host=config.DB_HOST,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                port=config.DB_PORT,
                sslmode='require'
            )
        
        cur = conn.cursor()
        
        # Crear tabla de usuarios
        cur.execute("""
            CREATE TABLE IF NOT EXISTS login (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                usuario VARCHAR(255) UNIQUE NOT NULL,
                pass TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de contraseñas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS keypass (
                id SERIAL PRIMARY KEY,
                site VARCHAR(255) NOT NULL,
                user_name VARCHAR(255) NOT NULL,
                pass BYTEA NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES login(id) ON DELETE CASCADE
            )
        """)
        
        # Crear índices para mejor rendimiento
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_login_email ON login(email)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_login_usuario ON login(usuario)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_keypass_user_id ON keypass(user_id)
        """)
        
        # Confirmar cambios
        conn.commit()
        print(" Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f" Error inicializando base de datos: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_database()

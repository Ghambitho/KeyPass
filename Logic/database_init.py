import psycopg2
from psycopg2.extras import RealDictCursor
import config

def init_database():
    """Inicializar base de datos PostgreSQL"""
    try:
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
                pass TEXT NOT NULL
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
                FOREIGN KEY (user_id) REFERENCES login(id)
            )
        """)
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False


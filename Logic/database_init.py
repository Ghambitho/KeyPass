import sqlite3
from pathlib import Path
import config

def init_database():
    """Inicializar base de datos SQLite local"""
    try:
        # Crear directorio de datos
        data_dir = Path(__file__).resolve().parent.parent / "db"
        data_dir.mkdir(exist_ok=True)
        
        # Archivo de base de datos SQLite
        db_file = data_dir / "keypass.db"
        
        # Conectar a SQLite
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        
        # Crear tabla de usuarios
        cur.execute("""
            CREATE TABLE IF NOT EXISTS login (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                pass TEXT NOT NULL
            )
        """)
        
        # Crear tabla de contraseñas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS keypass (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT NOT NULL,
                user_name TEXT NOT NULL,
                pass BLOB NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES login(id)
            )
        """)
        
        # Crear índices para mejor rendimiento
        cur.execute("CREATE INDEX IF NOT EXISTS idx_login_email ON login(email)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_login_usuario ON login(usuario)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_keypass_user_id ON keypass(user_id)")
        
        conn.commit()
        conn.close()
        
        print("✅ Base de datos SQLite inicializada correctamente")
        return True
        
    except Exception as e:
        print(f"Error inicializando base de datos SQLite: {e}")
        return False


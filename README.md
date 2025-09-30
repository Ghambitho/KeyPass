# KeyPass API - Gestor de Contraseñas

## Descripción

KeyPass es un gestor de contraseñas seguro que permite almacenar y gestionar contraseñas de forma cifrada. Esta versión incluye una API REST para acceso remoto desde cualquier dispositivo.

##  Estructura del Proyecto

```
KeyPass/
├── api.py                 #  API FastAPI principal
├── Logic/                 #  Lógica de negocio
│   ├── __init__.py
│   ├── database_init.py   #  PostgreSQL
│   ├── encryption.py      #  Cifrado AES-CBC + HMAC
│   ├── login.py          #  Autenticación
│   ├── session.py        #  Gestión de sesiones
│   ├── storage.py        #  Almacenamiento PostgreSQL
│   └── password_generator.py #  Generador de contraseñas
├── Main/                  #  Interfaz PyQt6 (para .exe)
│   ├── app.py
│   ├── login_view.py
│   ├── password.py
│   ├── PerfilWindow.py
│   └── signup_view.py
├── assets/                #  Recursos gráficos (para .exe)
├── config.py             #  Configuración
├── requirements.txt      #  Dependencias
├── Procfile             #  Configuración Render
└── env.example          #  Variables de entorno
```

##  Tecnologías

- **Backend**: FastAPI, PostgreSQL, JWT
- **Cifrado**: AES-CBC + HMAC, PBKDF2-SHA256
- **Frontend**: PyQt6 (para aplicación de escritorio)
- **Base de datos**: PostgreSQL (Supabase)
- **Deploy**: Render

##  Configuración

### 1. Variables de Entorno

Copia `env.example` y configura las variables:

```bash
# Base de datos PostgreSQL (Supabase)
DB_HOST=your-project.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_PORT=5432

# JWT Secret (¡CAMBIA ESTO!)
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Entorno
ENV=production
DEBUG=false
```

### 2. Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
python api.py
```

### 3. Deploy en Render

1. **Crear repositorio** en GitHub
2. **Conectar** con Render
3. **Configurar variables** de entorno
4. **Deploy automático**

## 📡 API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario

### Contraseñas
- `GET /api/passwords` - Obtener contraseñas
- `POST /api/passwords` - Guardar contraseña
- `DELETE /api/passwords/{id}` - Eliminar contraseña

### Utilidades
- `POST /api/generate-password` - Generar contraseña
- `GET /api/user/profile` - Obtener perfil

### Sistema
- `GET /` - Información de la API
- `GET /health` - Health check

##  Seguridad

- **Cifrado**: AES-CBC + HMAC para contraseñas
- **Autenticación**: JWT con expiración
- **Hash**: PBKDF2-SHA256 para contraseñas de usuario
- **Conexión**: SSL/TLS obligatorio
- **Validación**: Sanitización de inputs

##  Aplicación de Escritorio

Para compilar el .exe:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar
pyinstaller --onefile --windowed Main/app.py
```

##  Base de Datos

### Tabla `login`
```sql
CREATE TABLE login (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    usuario VARCHAR(255) UNIQUE NOT NULL,
    pass TEXT NOT NULL
);
```

### Tabla `keypass`
```sql
CREATE TABLE keypass (
    id SERIAL PRIMARY KEY,
    site VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    pass BYTEA NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES login(id)
);
```

##  Uso

### Desde la API
```python
import requests

# Login
response = requests.post("https://your-api.render.com/api/auth/login", 
                        json={"email": "user@example.com", "password": "password"})
token = response.json()["token"]

# Obtener contraseñas
headers = {"Authorization": f"Bearer {token}"}
passwords = requests.get("https://your-api.render.com/api/passwords", headers=headers)
```

### Desde el .exe
El ejecutable se conecta automáticamente a la API usando las credenciales configuradas.

##  Notas

- **Producción**: Cambiar `JWT_SECRET` por una clave segura
- **CORS**: Configurar orígenes específicos en producción
- **Logs**: Monitorear logs de Render para debugging
- **Backup**: Configurar backup automático de Supabase

##  Migración

Si tienes datos en SQLite local, necesitarás migrarlos a PostgreSQL:

1. Exportar datos de SQLite
2. Importar a PostgreSQL
3. Verificar cifrado

##  Soporte

Para problemas o preguntas, revisar los logs de Render o contactar al desarrollador.
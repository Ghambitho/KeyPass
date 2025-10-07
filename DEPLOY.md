# KeyPass - Deployment en Render con Supabase

## Configuración para Render

### 1. Configurar Supabase

1. Ve a [supabase.com](https://supabase.com) y crea un nuevo proyecto
2. En el dashboard de Supabase, ve a **Settings** > **Database**
3. Copia la **Connection String** que tiene este formato:
   ```
   postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
   ```

### 2. Configurar Render

1. Conecta tu repositorio de GitHub a Render
2. Crea un nuevo **Web Service**
3. Configura las siguientes variables de entorno:

#### Variables de Entorno Obligatorias:

```bash
# Base de datos
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres

# JWT (genera una clave secreta fuerte)
JWT_SECRET=tu-clave-super-secreta-jwt-aqui

# Configuración
ENV=production
DEBUG=false
ALLOWED_ORIGINS=*
```

#### Variables Opcionales:
```bash
JWT_ALG=HS256
JWT_EXP_MIN=15
DEFAULT_PASSWORD_LENGTH=16
MIN_PASSWORD_LENGTH=8
MAX_PASSWORD_LENGTH=128
```

### 3. Configuración del Build

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api.api:app --host 0.0.0.0 --port $PORT`

### 4. Inicialización de la Base de Datos

Las tablas se crearán automáticamente cuando la aplicación se inicie por primera vez.

### 5. Configurar el Cliente

Una vez que tengas la URL de tu API en Render, actualiza el archivo `client/config.py`:

```python
API_BASE_URL = "https://tu-app.onrender.com"
```

## URLs de la API

Una vez deployado, tu API tendrá estos endpoints:

- `GET /` - Información de la API
- `GET /health` - Health check
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `GET /api/passwords` - Obtener contraseñas
- `POST /api/passwords` - Guardar contraseña
- `DELETE /api/passwords/{id}` - Eliminar contraseña
- `POST /api/generate-password` - Generar contraseña
- `GET /api/user/profile` - Perfil del usuario

## Notas Importantes

- Asegúrate de que tu clave JWT sea fuerte y única
- La aplicación usa conexiones SSL por defecto
- Las contraseñas se cifran usando PBKDF2 + AES
- Los tokens JWT expiran en 15 minutos por defecto
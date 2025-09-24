# 🔐 KeyPass - Gestor de Contraseñas Seguro

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descripción

KeyPass es una aplicación de escritorio desarrollada en Python que permite a los usuarios generar, almacenar y gestionar contraseñas de forma segura. La aplicación utiliza cifrado avanzado para proteger los datos sensibles y ofrece una interfaz gráfica moderna y fácil de usar.

## ✨ Características Principales

- 🔐 **Generación de contraseñas seguras** con opciones personalizables
- 🛡️ **Cifrado avanzado** usando Fernet (AES 128)
- 👤 **Sistema de autenticación** con hash PBKDF2
- 💾 **Almacenamiento local** con SQLite
- 🎨 **Interfaz moderna** con PyQt6
- 📱 **Gestión de sesiones** persistentes
- 🔍 **Búsqueda y filtrado** de contraseñas
- 📤 **Exportación** a CSV
- 🗑️ **Eliminación segura** de registros

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/Ghambitho/KeyPass
cd KeyPass

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias

```
PyQt6>=6.0.0
cryptography>=41.0.0
pyperclip>=1.8.0
keyring>=24.0.0
```

## 🎯 Uso

### Ejecución Normal

```bash
python Main/app.py
```

### Desarrollo con Auto-reload

```bash
# Instalar watchdog para desarrollo
pip install watchdog

# Ejecutar con auto-reload
watchmedo auto-restart --pattern="*.py" --recursive -- python Main/app.py
```

## 🏗️ Arquitectura del Proyecto

```
KeyPass/
├── Main/                    # Interfaz de usuario (PyQt6)
│   ├── app.py              # Aplicación principal
│   ├── login_view.py       # Vista de inicio de sesión
│   ├── signup_view.py      # Vista de registro
│   ├── password.py         # Vista de gestión de contraseñas
│   └── PerfilWindow.py     # Vista de perfil de usuario
├── Logic/                  # Lógica de negocio
│   ├── encryption.py       # Módulo de cifrado
│   ├── login.py           # Autenticación de usuarios
│   ├── password_generator.py # Generación de contraseñas
│   ├── session.py         # Gestión de sesiones
│   └── storage.py         # Almacenamiento de datos
├── db/                     # Base de datos y archivos de sesión
│   ├── keypass.db         # Base de datos SQLite
│   ├── session.bin        # Archivo de sesión cifrado
│   └── session.key        # Clave de cifrado de sesión
├── assets/                 # Recursos gráficos
│   ├── apple.png          # Icono de Apple
│   ├── google.png         # Icono de Google
│   ├── copy-pass.png      # Icono de copiar
│   ├── copy-savepass.png  # Icono de copiar guardado
│   ├── eye-closed.png     # Icono de ojo cerrado
│   ├── eye-open.png       # Icono de ojo abierto
│   └── lupa.png           # Icono de búsqueda
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🔧 Funcionalidades Detalladas

### 1. Sistema de Autenticación

- **Registro de usuarios** con validación de email
- **Inicio de sesión** con email o nombre de usuario
- **Hash seguro** de contraseñas usando PBKDF2
- **Migración automática** de algoritmos antiguos
- **Gestión de sesiones** persistentes

### 2. Generador de Contraseñas

- **Longitud configurable** (6-32 caracteres)
- **Opciones personalizables:**
  - Letras mayúsculas
  - Números
  - Símbolos especiales
- **Generación instantánea**
- **Copia al portapapeles**

### 3. Gestión de Contraseñas

- **Almacenamiento cifrado** con Fernet
- **Búsqueda y filtrado** en tiempo real
- **Visualización segura** (mostrar/ocultar)
- **Copia rápida** al portapapeles
- **Eliminación** con confirmación
- **Exportación** a formato CSV

### 4. Perfil de Usuario

- **Edición de datos** personales
- **Cambio de contraseña** seguro
- **Exportación** de todas las contraseñas
- **Configuración** de notificaciones

## 🔒 Seguridad

### Cifrado de Datos

- **Fernet (AES 128)** para cifrado de contraseñas
- **Claves únicas** por instalación
- **Almacenamiento seguro** de claves

### Autenticación

- **PBKDF2** con 200,000 iteraciones
- **Salt aleatorio** de 16 bytes
- **Comparación segura** con HMAC
- **Migración automática** de algoritmos antiguos

### Gestión de Sesiones

- **Tokens cifrados** con TTL configurable
- **Almacenamiento local** seguro
- **Expiración automática** de sesiones

## 🗄️ Base de Datos

### Esquema de Tablas

#### Tabla `login`
```sql
CREATE TABLE login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    pass TEXT NOT NULL
);
```

#### Tabla `KEYPASS`
```sql
CREATE TABLE KEYPASS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT NOT NULL,
    User TEXT NOT NULL,
    pass BLOB NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES login(id)
);
```

## 🛠️ Desarrollo

### Estructura de Código

- **Separación de responsabilidades** (UI/Logic)
- **Módulos independientes** para cada funcionalidad
- **Manejo de errores** robusto
- **Código documentado** con comentarios

### Patrones Utilizados

- **MVC (Model-View-Controller)**
- **Observer Pattern** (PyQt6 Signals/Slots)
- **Factory Pattern** (generación de widgets)

## 🧪 Testing

### Pruebas Manuales

1. **Registro de usuario** nuevo
2. **Inicio de sesión** con credenciales válidas
3. **Generación** de contraseñas
4. **Almacenamiento** y recuperación
5. **Búsqueda** y filtrado
6. **Exportación** de datos

### Casos de Prueba

- ✅ Autenticación exitosa
- ✅ Generación de contraseñas
- ✅ Cifrado/descifrado
- ✅ Gestión de sesiones
- ✅ Exportación de datos


## 📝 Changelog

### Versión 1.0.0
- ✅ Sistema de autenticación completo
- ✅ Generador de contraseñas
- ✅ Gestión de contraseñas cifradas
- ✅ Interfaz gráfica moderna
- ✅ Exportación a CSV
- ✅ Gestión de sesiones


## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [Ghambitho](https://github.com/Ghambitho)
- Email: Bel4ndria.d.jhon@gmail.com


- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Framework de interfaz gráfica
- [Cryptography](https://cryptography.io/) - Biblioteca de cifrado
- [SQLite](https://www.sqlite.org/) - Base de datos embebida

---

**¡Gracias por usar KeyPass! 🔐**

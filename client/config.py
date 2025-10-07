import os
from dotenv import load_dotenv
load_dotenv()

# API Backend
API_BASE_URL = os.getenv("API_BASE_URL", "https://keypass-yk6b.onrender.com")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

# UI
WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '900'))
WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
WINDOW_TITLE = os.getenv('WINDOW_TITLE', 'KeyPass - Gestor de Contraseñas')
ASSETS_PATH = os.getenv('ASSETS_PATH', 'assets/')

# Sesión local del cliente
DEFAULT_TTL_DAYS = int(os.getenv("SESSION_TTL_DAYS", "7"))
SESSION_FILE = os.getenv('SESSION_FILE', 'session.bin')

# Contraseñas
MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '6'))
MAX_PASSWORD_LENGTH = int(os.getenv('MAX_PASSWORD_LENGTH', '32'))
DEFAULT_PASSWORD_LENGTH = int(os.getenv('DEFAULT_PASSWORD_LENGTH', '14'))
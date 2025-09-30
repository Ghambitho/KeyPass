# -*- coding: utf-8 -*-
"""Script para probar el rendimiento de las optimizaciones"""
import time
import sys
from pathlib import Path

# Ajustar sys.path
BASE = Path(__file__).resolve().parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

import config
from Logic.session import load_session

def test_performance():
    """Prueba el rendimiento de las operaciones"""
    print("Iniciando pruebas de rendimiento...")
    
    # Verificar sesión activa
    session = load_session()
    if not session:
        print("No hay sesión activa. Por favor, inicia sesión primero.")
        return
    
    user_id = session['user']
    print(f"Usuario de prueba: {user_id}")
    
    # Importar módulos según configuración
    if config.USE_OPTIMIZED_MODULES:
        print("Usando módulos optimizados...")
        from Logic import storage_optimized as storage
        from Logic import login_optimized as login
    else:
        print("Usando módulos estándar...")
        from Logic import storage
        from Logic import login
    
    # Prueba 1: Cargar perfil del usuario
    print("\nPrueba 1: Cargar perfil del usuario")
    start_time = time.time()
    profile = login.get_user_profile(user_id)
    end_time = time.time()
    print(f"   Tiempo: {(end_time - start_time)*1000:.2f}ms")
    print(f"   Resultado: {profile}")
    
    # Prueba 2: Cargar contraseñas (primera vez)
    print("\nPrueba 2: Cargar contraseñas (primera vez)")
    start_time = time.time()
    passwords = storage._load_all_passwords(user_id)
    end_time = time.time()
    print(f"   Tiempo: {(end_time - start_time)*1000:.2f}ms")
    print(f"   Contraseñas cargadas: {len(passwords)}")
    
    # Prueba 3: Cargar contraseñas (segunda vez - debería usar caché)
    print("\nPrueba 3: Cargar contraseñas (segunda vez - caché)")
    start_time = time.time()
    passwords = storage._load_all_passwords(user_id)
    end_time = time.time()
    print(f"   Tiempo: {(end_time - start_time)*1000:.2f}ms")
    print(f"   Contraseñas cargadas: {len(passwords)}")
    
    # Prueba 4: Cargar perfil (segunda vez - debería usar caché)
    print("\nPrueba 4: Cargar perfil (segunda vez - caché)")
    start_time = time.time()
    profile = login.get_user_profile(user_id)
    end_time = time.time()
    print(f"   Tiempo: {(end_time - start_time)*1000:.2f}ms")
    print(f"   Resultado: {profile}")
    
    print("\nPruebas completadas!")
    print("\nConsejos de optimización:")
    print("   - Si los tiempos son > 1000ms, considera usar módulos optimizados")
    print("   - La segunda carga debería ser más rápida si el caché funciona")
    print("   - Para mejor rendimiento, usa USE_OPTIMIZED_MODULES=true en .env")

if __name__ == "__main__":
    test_performance()

# -*- coding: utf-8 -*-
"""Pool de conexiones para optimizar rendimiento"""
import psycopg2
from psycopg2 import pool
import config
import threading

class DatabasePool:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_pool = None
            self._initialized = True
    
    def get_pool(self):
        """Obtiene o crea el pool de conexiones"""
        if self.connection_pool is None:
            try:
                self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=10,
                    host=config.DB_HOST,
                    database=config.DB_NAME,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    port=config.DB_PORT,
                    sslmode='require'
                )
                print("Database connection pool created")
            except Exception as e:
                print(f"Error creating connection pool: {e}")
                return None
        return self.connection_pool
    
    def get_connection(self):
        """Obtiene una conexión del pool"""
        pool = self.get_pool()
        if pool:
            try:
                return pool.getconn()
            except Exception as e:
                print(f"Error getting connection from pool: {e}")
                return None
        return None
    
    def return_connection(self, conn):
        """Devuelve una conexión al pool"""
        if self.connection_pool and conn:
            try:
                self.connection_pool.putconn(conn)
            except Exception as e:
                print(f"Error returning connection to pool: {e}")
    
    def close_all(self):
        """Cierra todas las conexiones del pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
            self.connection_pool = None

# Instancia global del pool
db_pool = DatabasePool()

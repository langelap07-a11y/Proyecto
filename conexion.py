"""Conexión a la base de datos MySQL (XAMPP).

Los valores por defecto sirven para XAMPP (usuario root sin contraseña).
Si tu MySQL es distinto, define variables de entorno sin tocar el código:
DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME.
"""
import os

import pymysql
import pymysql.cursors

CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "rutas_basura"),
    "charset": "utf8mb4",
    # DictCursor: cada fila llega como diccionario (f["nombre"]) en vez de tupla.
    "cursorclass": pymysql.cursors.DictCursor,
}


class Conexion:
    """Fábrica de conexiones. Cada DAO abre una, la usa y la cierra."""

    @staticmethod
    def obtener():
        return pymysql.connect(**CONFIG)

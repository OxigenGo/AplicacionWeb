#-----------------------------------
#   © 2025 RRVV Systems. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 29 de octubre de 2025
#-----------------------------------
#   Fichero: db.py
#   Descripción: Modulo con utilidades para el acceso a la base de datos
#-----------------------------------

import os
import mysql.connector

#-----------------------------------
#   Función para conectar a la base de datos
#-----------------------------------

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "mydb")
    )
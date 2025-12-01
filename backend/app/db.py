#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 29 de octubre de 2025
#-----------------------------------
#   Fichero: db.py
#   Descripción: Modulo con utilidades para el acceso a la base de datos
#-----------------------------------

import os
import mysql.connector
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

if os.path.isfile(ENV_PATH):
    load_dotenv(ENV_PATH)

#-----------------------------------
#   Función para conectar a la base de datos
#-----------------------------------

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "mydb")
    )
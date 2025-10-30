#-----------------------------------
#   © 2025 RRVV Systems. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 30 de octubre de 2025
#-----------------------------------
#   Fichero: conftest.py
#   Descripción: Modulo para realizar sentencias SQL teniendo la garantía de poder anularlas al terminar
#-----------------------------------

import pytest
from backend.app.db import get_connection

#-----------------------------------
#   Fixture de pytest
#   Crea una funcion y la hace visible y disponible para todos los archivos de la carpeta
#   La funcion en sí crea una conexión y antes de cerrarla revierte todos los cambios
#-----------------------------------

@pytest.fixture(scope="function")
def db():
    conn = get_connection()
    conn.start_transaction()
    yield conn
    conn.rollback()
    conn.close()
#-----------------------------------
#   © 2025 RRVV Systems. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 30 de octubre de 2025
#-----------------------------------
#   Fichero: test_sensores.py
#   Descripción: Módulo para realizar tests de las operaciones con sensores (insertar medicion y vincular sensor)
#-----------------------------------

import pytest
from backend.app.sensores import bind_sensor_to_user, add_reading
from backend.app.core import insert_user

#-----------------------------------
#   Test de vinculación.
#   Registra un usuario e inserta un sensor asociado a él
#-----------------------------------

def test_bind_sensor_to_user(db):
    user = insert_user("sensoruser", "sensor@example.com", "password")["usuario"]
    user_id = user["id"]

    uuid = "sensor-1234"
    result = bind_sensor_to_user(user_id, uuid)
    assert result["status"] == "ok"
    assert result["sensor"]["uuid"] == uuid
    assert result["sensor"]["associated_user"] == user_id

    db.execute("SELECT * FROM SENSORES WHERE UUID=%s", (uuid,))
    sensor = db.fetchone()
    assert sensor is not None
    assert sensor["ASSOCIATED_USER"] == user_id

#-----------------------------------
#   Test de inserción de lectura.
#   Inserta un usuario, le vincula un sensor, y le añade una lectura a este
#-----------------------------------

def test_add_reading(db):
    user = insert_user("readinguser", "reading@example.com", "password")["usuario"]
    user_id = user["id"]
    uuid = "sensor-5678"
    bind_sensor_to_user(user_id, uuid)

    result = add_reading(uuid, gas_value=3.14, temperature_value=25.5, position="Lab")
    assert result["status"] == "ok"

    db.execute("SELECT * FROM MEDICIONES WHERE ASSOCIATED_UUID=%s", (uuid,))
    reading = db.fetchone()
    assert reading is not None
    assert reading["GAS_VALUE"] == 3.14
    assert reading["TEMPERATURE_VALUE"] == 25.5
    assert reading["POSITION"] == "Lab"

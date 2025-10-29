#-----------------------------------
#   © 2025 RRVV Systems. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 29 de octubre de 2025
#-----------------------------------
#   Fichero: sensores.py
#   Descripción: Funciones de la lógica de negocio que
#   manejan cualquier cosa relacionada a los sensores
#-----------------------------------

from datetime import datetime
from fastapi import HTTPException

from db import get_connection

#-----------------------------------
#   Crea un sensor y lo vincula a un usuario
#   N: user_id, String: email -> bind_sensor_to_user() -> 200 OK | Error
#-----------------------------------

def bind_sensor_to_user(user_id: int, uuid: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT ID FROM USUARIOS WHERE ID = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        last_active = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO SENSORES (UUID, ASSOCIATED_USER, LAST_ACTIVE) VALUES (%s, %s, %s)",
            (uuid, user_id, last_active)
        )
        conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        conn.close()

    return {
        "status": "ok",
        "mensaje": f"Sensor '{uuid}' vinculado exitosamente al usuario con ID {user_id}",
        "sensor": {
            "uuid": uuid,
            "associated_user": user_id,
            "last_active": last_active,
        }
    }
    
    
#-----------------------------------
#   Crea una medicion, la asocia a un sensor y actualiza su campo de última actividad
#   String: associated_uuid, float: gas_value, float: temperature_value, String|Null: posicion -> add_reading() -> 200 OK | Error
#-----------------------------------

def add_reading(associated_uuid: str, gas_value: float, temperature_value: float, position: str = None):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT UUID FROM SENSORES WHERE UUID = %s", (associated_uuid,))
        sensor = cursor.fetchone()
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")

        cursor.execute(
            "INSERT INTO MEDICIONES (ASSOCIATED_UUID, GAS_VALUE, TEMPERATURE_VALUE, POSITION)VALUES (%s, %s, %s, %s)"
            ,(associated_uuid, gas_value, temperature_value, position)
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE SENSORES SET LAST_ACTIVE = %s WHERE UUID = %s",(now, associated_uuid)
        )

        conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        conn.close()

    return {
        "status": "ok",
        "mensaje": f"Medición agregada exitosamente para el sensor '{associated_uuid}'"
    }

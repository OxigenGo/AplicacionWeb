#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
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

from .db import get_connection

#-----------------------------------
#   Crea un sensor y lo vincula a un usuario
#   N: user_id, String: email -> bind_sensor_to_user() -> 200 OK | Error
#-----------------------------------

def bind_sensor_to_user(user_id: int, uuid: str, conn=None):
    close_conn = False
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True
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

        if close_conn:
            conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        if close_conn:
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
#   Borra un sensor concreto o todos los sensores de un usuario
#   N: user_id, Bool: erase_all ,String: uuid -> delete_sensor_records() -> 200 OK | Error
#-----------------------------------

def delete_sensor_records(user_id: int, erase_all: bool, uuid: str = None, conn=None):
    close_conn = False
    cursor = None
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT ID FROM USUARIOS WHERE ID = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        cursor.execute("SELECT UUID FROM SENSORES WHERE ASSOCIATED_USER = %s", (user_id,))
        sensores = cursor.fetchall()

        if not sensores:
            raise HTTPException(status_code=404, detail="El usuario no tiene sensores asociados")

        if erase_all:
            cursor.execute("DELETE FROM SENSORES WHERE ASSOCIATED_USER = %s", (user_id,))
            message = f"Todos los sensores del usuario {user_id} han sido eliminados"

        else:
            if uuid is None:
                raise HTTPException(
                    status_code=400,
                    detail="Debe proporcionar un UUID para borrar un sensor específico"
                )

            cursor.execute(
                "SELECT UUID FROM SENSORES WHERE UUID = %s AND ASSOCIATED_USER = %s",
                (uuid, user_id)
            )
            sensor = cursor.fetchone()

            if not sensor:
                raise HTTPException(
                    status_code=404,
                    detail=f"El sensor '{uuid}' no está asociado al usuario {user_id}"
                )

            cursor.execute("DELETE FROM SENSORES WHERE UUID = %s", (uuid,))
            message = f"El sensor '{uuid}' ha sido eliminado del usuario {user_id}"

        if close_conn:
            conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if close_conn and conn:
            conn.close()

    return {
        "status": "ok",
        "mensaje": message,
        "usuario": user_id,
        "eliminado": "todos" if erase_all else uuid
    }
    
    
#-----------------------------------
#   Crea una medicion, la asocia a un sensor y actualiza su campo de última actividad
#   String: associated_uuid, float: gas_value, float: temperature_value, String|Null: posicion -> add_reading() -> 200 OK | Error
#-----------------------------------

def add_reading(associated_uuid: str, gas_value: float, temperature_value: float, position: str = None, conn=None):
    close_conn = False
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT UUID FROM SENSORES WHERE UUID = %s", (associated_uuid,))
        sensor = cursor.fetchone()
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO MEDICIONES (ASSOCIATED_UUID, DATE, GAS_VALUE, TEMPERATURE_VALUE, POSITION) "
            "VALUES (%s, %s, %s, %s, %s)",
            (associated_uuid, now, gas_value, temperature_value, position)
        )

        cursor.execute(
            "UPDATE SENSORES SET LAST_ACTIVE = %s WHERE UUID = %s",
            (now, associated_uuid)
        )

        if close_conn:
            conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        cursor.close()
        if close_conn:
            conn.close()

    return {
        "status": "ok",
        "mensaje": f"Medición agregada exitosamente para el sensor '{associated_uuid}'"
    }
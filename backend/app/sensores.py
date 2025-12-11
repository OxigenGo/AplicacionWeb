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

from datetime import datetime, timedelta
from fastapi import HTTPException
from .db import get_connection

#-----------------------------------
#   FUNCIONES DE GESTIÓN DE SENSORES
#-----------------------------------

def bind_sensor_to_user(user_id: int, uuid: str, conn=None):
    """
    @brief Vincula un sensor a un usuario en la base de datos.
    @param user_id ID del usuario.
    @param uuid Identificador único del sensor.
    @param conn Conexión opcional a la base de datos.
    @return dict Información del sensor vinculado.
    @throws HTTPException 404 si el usuario no existe.
    @throws HTTPException 500 si ocurre un error en la base de datos.
    """
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

def delete_sensor_records(user_id: int, erase_all: bool, uuid: str = None, conn=None):
    """
    @brief Borra uno o todos los sensores asociados a un usuario.
    @param user_id ID del usuario.
    @param erase_all Si True borra todos los sensores del usuario.
    @param uuid UUID del sensor específico a borrar (opcional si erase_all=True).
    @param conn Conexión opcional a la base de datos.
    @return dict Información sobre la eliminación.
    @throws HTTPException 404 si el usuario o sensor no existen.
    @throws HTTPException 400 si no se proporciona UUID al borrar uno específico.
    @throws HTTPException 500 si ocurre un error en la base de datos.
    """
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

def add_reading(associated_uuid: str, gas_type: str, gas_value: float, temperature_value: float, position: str = None, conn=None):
    """
    @brief Agrega una medición a un sensor y actualiza su última actividad.
    @param associated_uuid UUID del sensor.
    @param gas_type Tipo de gas medido.
    @param gas_value Valor del gas.
    @param temperature_value Valor de temperatura.
    @param position Posición o ubicación del sensor (opcional).
    @param conn Conexión opcional a la base de datos.
    @return dict Mensaje de éxito de la operación.
    @throws HTTPException 404 si el sensor no existe.
    @throws HTTPException 500 si ocurre un error en la base de datos.
    """
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
            "INSERT INTO MEDICIONES (ASSOCIATED_UUID, DATE, GAS_TYPE, GAS_VALUE, TEMPERATURE_VALUE, POSITION) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (associated_uuid, now, gas_type, gas_value, temperature_value, position)
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

def get_user_sensors(user_id: int, conn=None):
    """
    @brief Devuelve los sensores de un usuario y sus últimas 20 mediciones.
    @param user_id ID del usuario.
    @param conn Conexión opcional a la base de datos.
    @return dict Sensores y mediciones del usuario.
    @throws HTTPException 404 si el usuario o sensores no existen.
    @throws HTTPException 500 si ocurre un error en la base de datos.
    """
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

        cursor.execute("SELECT UUID, LAST_ACTIVE FROM SENSORES WHERE ASSOCIATED_USER = %s", (user_id,))
        sensores = cursor.fetchall()
        if not sensores:
            raise HTTPException(status_code=404, detail="El usuario no tiene sensores asociados")

        resultado = []
        for sensor in sensores:
            cursor.execute(
                "SELECT DATE, GAS_TYPE, GAS_VALUE, TEMPERATURE_VALUE, POSITION "
                "FROM MEDICIONES WHERE ASSOCIATED_UUID = %s "
                "ORDER BY DATE DESC LIMIT 20",
                (sensor["UUID"],)
            )
            mediciones = cursor.fetchall()
            resultado.append({
                "uuid": sensor["UUID"],
                "last_active": sensor["LAST_ACTIVE"],
                "mediciones": mediciones
            })

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
        "usuario": user_id,
        "sensores": resultado
    }

def get_all_sensors(conn=None):
    """
    @brief Devuelve una lista con todos los sensores de la base de datos.
    @param conn Conexión opcional a la base de datos.
    @return dict Lista de sensores y su última actividad.
    @throws HTTPException 500 si ocurre un error en la base de datos.
    """
    close_conn = False
    cursor = None
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT UUID, ASSOCIATED_USER, LAST_ACTIVE FROM SENSORES")
        sensors = cursor.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if close_conn and conn:
            conn.close()

    return {
        "status": "ok",
        "sensors": sensors
    }

def get_today_measurements_for_user(user_id: int, conn=None):
    """
    @brief Devuelve todas las mediciones del día actual de todos los sensores asociados a un usuario.
    @param user_id ID del usuario.
    @param conn Conexión opcional a la base de datos.
    @return dict con un listado de mediciones de hoy.
    @throws HTTPException 404 si el usuario no existe o no tiene sensores.
    @throws HTTPException 500 si ocurre un error en la base de datos.
    """
    close_conn = False
    cursor = None
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True
        cursor = conn.cursor(dictionary=True)

        # Verificar usuario
        cursor.execute("SELECT ID FROM USUARIOS WHERE ID = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Obtener UUID de todos los sensores del usuario
        cursor.execute("SELECT UUID FROM SENSORES WHERE ASSOCIATED_USER = %s", (user_id,))
        sensores = cursor.fetchall()
        if not sensores:
            raise HTTPException(status_code=404, detail="El usuario no tiene sensores asociados")

        # Obtener lista de UUIDs
        uuids = [s["UUID"] for s in sensores]

        today_str = datetime.now().strftime("%Y-%m-%d")

        # Traer todas las mediciones del día
        format_strings = ','.join(['%s'] * len(uuids))
        query = f"""
            SELECT ASSOCIATED_UUID, DATE, GAS_TYPE, GAS_VALUE, TEMPERATURE_VALUE, POSITION
            FROM MEDICIONES
            WHERE ASSOCIATED_UUID IN ({format_strings}) AND DATE(DATE) = %s
            ORDER BY DATE DESC
        """
        cursor.execute(query, (*uuids, today_str))
        mediciones = cursor.fetchall()

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
        "usuario": user_id,
        "mediciones": mediciones
    }
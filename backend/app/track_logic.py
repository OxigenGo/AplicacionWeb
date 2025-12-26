#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 23 de diciembre de 2025
#-----------------------------------
#   Fichero: track_logic.py
#   Descripción: Funciones de la lógica de negocio que manejan los recorridos
#-----------------------------------

from .db import get_connection
from datetime import datetime
import json


def create_track(user_id: int):
    """
    @brief Crea un nuevo recorrido asociado a un usuario existente.
    
    @param user_id ID del usuario al que pertenece el recorrido.
    
    @return Diccionario con:
        - id: ID del recorrido creado (si procede).
        - message: Mensaje de confirmación o error.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT 1 FROM USUARIOS WHERE ID = %s", (user_id,))
    user_exists = cursor.fetchone()

    if user_exists is None:
        cursor.close()
        conn.close()
        return {
            "id": None,
            "message": "User not found"
        }

    query = """
        INSERT INTO RECORRIDOS (
            USER_ID
        )
        VALUES (%s)
    """

    cursor.execute(query, (user_id,))
    conn.commit()

    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "id": new_id,
        "message": "Track created successfully"
    }


def delete_track(track_id: int):
    """
    @brief Elimina un recorrido existente de la base de datos.
    
    @param track_id ID del recorrido a eliminar.
    
    @return Diccionario indicando:
        - deleted: Número de filas eliminadas (0 o 1).
        - message: Mensaje indicando si se eliminó correctamente o no se encontró.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "DELETE FROM RECORRIDOS WHERE ID = %s"

    cursor.execute(query, (track_id,))
    conn.commit()

    deleted = cursor.rowcount

    cursor.close()
    conn.close()

    return {
        "deleted": deleted,
        "message": "Track deleted successfully" if deleted else "Track not found"
    }


def create_punto_recorrido(recorrido_id: int, location):
    """
    @brief Crea un nuevo punto asociado a un recorrido.
    
    @param recorrido_id ID del recorrido al que pertenece el punto.
    @param location Ubicación en formato GeoJSON (GeoJSONPoint Pydantic object).
    
    @return Diccionario con:
        - recorrido_id: ID del recorrido asociado
        - location: GeoJSON insertado
        - time: Hora local de inserción
        - message: Mensaje de confirmación o error
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("SELECT 1 FROM RECORRIDOS WHERE ID = %s", (recorrido_id,))
    recorrido_exists = cursor.fetchone()

    if recorrido_exists is None:
        cursor.close()
        conn.close()
        return {
            "message": "Track not found"
        }

    query = """
        INSERT INTO PUNTOS_RECORRIDO (
            RECORRIDO_ID,
            LOCATION,
            TIME
        )
        VALUES (%s, %s, %s)
    """

    now = datetime.now()

    location_json = json.dumps(location.dict())

    cursor.execute(query, (recorrido_id, location_json, now))
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "recorrido_id": recorrido_id,
        "location": location.dict(),
        "time": now,
        "message": "Punto de recorrido created successfully"
    }


def get_recorridos_by_user(user_id: int):
    """
    @brief Obtiene todos los recorridos asociados a un usuario.
    
    @param user_id ID del usuario.
    
    @return Lista de diccionarios con los recorridos del usuario.
            Cada diccionario contiene:
            - id: ID del recorrido
            - user_id: ID del usuario propietario
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM RECORRIDOS WHERE USER_ID = %s"
    cursor.execute(query, (user_id,))
    recorridos = cursor.fetchall()

    cursor.close()
    conn.close()

    return recorridos


def get_puntos_recorrido(recorrido_id: int):
    """
    @brief Obtiene todos los puntos asociados a un recorrido específico.
    
    @param recorrido_id ID del recorrido.
    
    @return Lista de diccionarios con cada punto:
            - location: GeoJSON (dict)
            - time: datetime
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT 1 FROM RECORRIDOS WHERE ID = %s", (recorrido_id,))
    recorrido_exists = cursor.fetchone()
    if not recorrido_exists:
        cursor.close()
        conn.close()
        return {"message": "Track not found"}


    cursor.execute(
        "SELECT LOCATION, TIME FROM PUNTOS_RECORRIDO WHERE RECORRIDO_ID = %s ORDER BY TIME ASC",
        (recorrido_id,)
    )
    puntos = cursor.fetchall()


    for punto in puntos:
        try:
            punto["location"] = json.loads(punto["LOCATION"])
        except (TypeError, json.JSONDecodeError):
            punto["location"] = None
        del punto["LOCATION"]

    cursor.close()
    conn.close()

    return puntos
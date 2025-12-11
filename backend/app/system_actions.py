#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 8 de diciembre de 2025
#-----------------------------------
#   Fichero: system_actions.py
#   Descripción: Funciones de la lógica de negocio que
#   manejan las incidencias
#-----------------------------------

from datetime import datetime
from .db import get_connection
from .schemas.system import (
    IncidentFilter, IncidentCreate, IncidentUpdate
    )

from .email_utils import (
    send_incident_created_email,
    send_incident_updated_email
)

def get_incidents(filters: IncidentFilter):
    """
    @brief Obtiene una lista de incidencias filtradas según los parámetros recibidos.
    
    @param filters Objeto IncidentFilter con los campos opcionales para filtrar.
        - id: Filtrar por ID de incidencia.
        - user_id: Filtrar por ID del usuario.
        - user_handled: Filtrar por usuario que gestiona la incidencia.
        - state: Filtrar por estado de la incidencia.
        - submit_date_from: Fecha mínima de creación.
        - submit_date_to: Fecha máxima de creación.
    
    @return Lista de diccionarios representando las incidencias obtenidas de la base de datos.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    base_query = "SELECT * FROM INCIDENCIAS"
    conditions = []
    params = []

    if filters is not None:

        if filters.id is not None:
            conditions.append("ID = %s")
            params.append(filters.id)

        if filters.user_id is not None:
            conditions.append("USER_ID = %s")
            params.append(filters.user_id)

        if filters.user_handled is not None:
            conditions.append("USER_HANDLED = %s")
            params.append(filters.user_handled)

        if filters.state is not None:
            conditions.append("STATE = %s")
            params.append(filters.state)

        if filters.submit_date_from is not None:
            conditions.append("SUBMIT_DATE >= %s")
            params.append(filters.submit_date_from)

        if filters.submit_date_to is not None:
            conditions.append("SUBMIT_DATE <= %s")
            params.append(filters.submit_date_to)

    if conditions:
        final_query = base_query + " WHERE " + " AND ".join(conditions)
    else:
        final_query = base_query

    cursor.execute(final_query, params)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def create_incident(incident: IncidentCreate):
    """
    @brief Crea una nueva incidencia en la base de datos.
    
    @param incident Objeto IncidentCreate con los datos de la nueva incidencia:
        - user_id: ID del usuario que la reporta.
        - subject: Asunto de la incidencia.
        - description: Descripción detallada.
        - user_handled: ID del usuario asignado (opcional).
        - state: Estado inicial de la incidencia.
    
    @return Diccionario con el ID de la incidencia creada y un mensaje de confirmación.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        INSERT INTO INCIDENCIAS (
            USER_ID,
            SUBJECT,
            DESCRIPTION,
            USER_HANDLED,
            STATE,
            SUBMIT_DATE,
            CHANGE_DATE
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    now = datetime.now()

    values = (
        incident.user_id,
        incident.subject,
        incident.description,
        incident.user_handled,
        incident.state,
        now,
        now
    )

    cursor.execute(query, values)
    conn.commit()

    new_id = cursor.lastrowid

    cursor.execute("SELECT EMAIL FROM USUARIOS WHERE ID = %s", (incident.user_id,))
    row = cursor.fetchone()
    user_email = row["EMAIL"] if row else None

    cursor.close()
    conn.close()

    if user_email:
        send_incident_created_email(
            to_email=user_email,
            incident_id=new_id,
            subject=incident.subject
        )

    return {"id": new_id, "message": "Incident created successfully"}


def update_incident(incident_id: int, incident: IncidentUpdate):
    """
    @brief Actualiza una incidencia existente en la base de datos.
    
    @param incident_id ID de la incidencia a actualizar.
    @param incident Objeto IncidentUpdate con los campos modificables:
        - subject: Nuevo asunto.
        - description: Nueva descripción.
        - user_handled: Nuevo usuario responsable.
        - state: Nuevo estado de la incidencia.
    
    @return Diccionario indicando:
        - updated: Numero de filas afectadas (0 o 1).
        - message: Mensaje indicando si se actualizó correctamente o no se encontró.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener datos originales antes de modificar
    cursor.execute("SELECT * FROM INCIDENCIAS WHERE ID = %s", (incident_id,))
    original = cursor.fetchone()

    if original is None:
        cursor.close()
        conn.close()
        return {"updated": 0, "message": "Incident not found"}

    # Detectar cambios
    changes = compute_incident_changes(original, incident)

    fields = []
    params = []

    if incident.subject is not None:
        fields.append("SUBJECT = %s")
        params.append(incident.subject)

    if incident.description is not None:
        fields.append("DESCRIPTION = %s")
        params.append(incident.description)

    if incident.user_handled is not None:
        fields.append("USER_HANDLED = %s")
        params.append(incident.user_handled)

    if incident.state is not None:
        fields.append("STATE = %s")
        params.append(incident.state)

    fields.append("CHANGE_DATE = %s")
    params.append(datetime.now())

    query = f"""
        UPDATE INCIDENCIAS
        SET {', '.join(fields)}
        WHERE ID = %s
    """

    params.append(incident_id)

    cursor.execute(query, params)
    conn.commit()

    updated = cursor.rowcount

    cursor.execute("SELECT EMAIL FROM USUARIOS WHERE ID = %s", (original["USER_ID"],))
    row = cursor.fetchone()
    user_email = row["EMAIL"] if row else None

    cursor.close()
    conn.close()

    if updated and user_email and changes:
        send_incident_updated_email(
            to_email=user_email,
            incident_id=incident_id,
            changes=changes
        )

    return {
        "updated": updated,
        "message": "Incident updated successfully" if updated else "Incident not found"
    }
    
# ============================================================
#   Función auxiliar: detectar cambios entre BD y lo nuevo
# ============================================================

def compute_incident_changes(old: dict, new: IncidentUpdate) -> dict:
    """
    @brief Compara los valores antiguos con los del update y retorna un diccionario
           con los cambios detectados.

    @param old Diccionario de la incidencia original sacada de la BD.
    @param new Objeto IncidentUpdate con los campos modificados.

    @return dict con formato:
            {
                "campo": ("antes", "después"),
                ...
            }
    """
    changes = {}

    if new.subject is not None and new.subject != old["SUBJECT"]:
        changes["subject"] = (old["SUBJECT"], new.subject)

    if new.description is not None and new.description != old["DESCRIPTION"]:
        changes["description"] = (old["DESCRIPTION"], new.description)

    if new.user_handled is not None and new.user_handled != old["USER_HANDLED"]:
        changes["user_handled"] = (old["USER_HANDLED"], new.user_handled)

    if new.state is not None and new.state != old["STATE"]:
        changes["state"] = (old["STATE"], new.state)

    return changes
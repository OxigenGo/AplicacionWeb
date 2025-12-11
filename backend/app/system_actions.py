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

def get_incidents(filters: IncidentFilter):
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
    conn = get_connection()
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

    return {"id": new_id, "message": "Incident created successfully"}

def update_incident(incident_id: int, incident: IncidentUpdate):
    conn = get_connection()
    cursor = conn.cursor()

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

    if not fields:
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

    cursor.close()
    conn.close()

    return {
        "updated": updated,
        "message": "Incident updated successfully" if updated else "Incident not found"
    }
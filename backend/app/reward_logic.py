#-----------------------------------
#   © 2026 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fedor Tikhomirov
#   Fecha: 14 de enero de 2026
#-----------------------------------
#   Fichero: reward_logic.py
#   Descripción: Funciones de la lógica de negocio que
#   manejan las recompensas del usuario
#-----------------------------------

from fastapi import HTTPException
from .db import get_connection

def get_user_rewards(user_id: int):
    """
    @brief Obtiene todas las recompensas asociadas a un usuario.

    @param user_id ID del usuario.

    @return Lista de diccionarios con las recompensas del usuario.
            Incluye tanto reclamadas como no reclamadas.
    """
    conn = None
    try:
        conn = get_connection()

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT ID, DESCRIPTION, STATE FROM RECOMPENSAS WHERE ASSOCIATED_USER = %s",
                (user_id,)
            )
            rewards = cursor.fetchall()

        return {
            "status": "ok",
            "rewards": rewards
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener recompensas: {e}")

    finally:
        if conn:
            conn.close()


def claim_reward(reward_id: int, user_id: int):
    """
    @brief Marca una recompensa como reclamada por su usuario.

    @param reward_id ID de la recompensa.
    @param user_id ID del usuario que intenta reclamarla.

    @return Diccionario indicando el resultado de la operación:
            - claimed: 0 o 1
            - message: Resultado de la operación
    """
    conn = None
    try:
        conn = get_connection()

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT ID, ASSOCIATED_USER, STATE FROM RECOMPENSAS WHERE ID = %s",
                (reward_id,)
            )
            reward = cursor.fetchone()

            if not reward:
                raise HTTPException(status_code=404, detail="Recompensa no encontrada")

            if reward["ASSOCIATED_USER"] != user_id:
                raise HTTPException(status_code=403, detail="La recompensa no pertenece a este usuario")

            if reward["STATE"] != "UNCLAIMED":
                raise HTTPException(status_code=400, detail="La recompensa ya ha sido reclamada")

            cursor.execute(
                "UPDATE RECOMPENSAS SET STATE = %s WHERE ID = %s",
                ("CLAIMED", reward_id)
            )

        conn.commit()

        return {
            "status": "ok",
            "mensaje": "Recompensa reclamada correctamente",
            "reward": {
                "id": reward_id,
                "state": "CLAIMED"
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al reclamar recompensa: {e}")
    finally:
        if conn:
            conn.close()

#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#-----------------------------------
#   Fichero: core.py
#   Descripción: Funciones de manejo de usuarios
#-----------------------------------

from datetime import datetime
from fastapi import HTTPException, Response
import bcrypt
import json

from .db import get_connection

#-----------------------------------
#   Inserta un nuevo usuario en la base de datos
#   String: username, String: email, String: pass -> insert_user() -> 200 OK | Error
#-----------------------------------
def insert_user(username: str, email: str, password: str, conn=None):
    close_conn = False
    user_id = None
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT ID FROM USUARIOS WHERE USERNAME = %s OR EMAIL = %s",
                (username, email)
            )
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El usuario o el correo ya existen")

            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            cursor.execute(
                "INSERT INTO USUARIOS (USERNAME, EMAIL, PASSWORD, REGISTER_DATE, LAST_LOGIN) VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, today, today)
            )

            user_id = cursor.lastrowid

        if close_conn:
            conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        if close_conn and conn:
            conn.close()

    return {"status": "ok", "mensaje": f"Usuario '{username}' creado exitosamente",
            "usuario": {"id": user_id, "username": username, "email": email}}

#-----------------------------------
#   Autentifica al usuario usando el correo o el nombre de usuario y la contraseña
#   String: user_or_email, String: pass -> login_user() -> JSON: user | HTTP Error
#-----------------------------------
def login_user(username_or_email: str, password: str, response: Response, conn=None):
    close_conn = False
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT ID, USERNAME, EMAIL, PASSWORD FROM USUARIOS WHERE USERNAME = %s OR EMAIL = %s",
                (username_or_email, username_or_email)
            )
            row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        user_id, username, email, stored_hash = row["ID"], row["USERNAME"], row["EMAIL"], row["PASSWORD"]
        
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        if password != stored_hash:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with conn.cursor() as cursor:
            cursor.execute("UPDATE USUARIOS SET LAST_LOGIN = %s WHERE ID = %s", (today, user_id))

        if close_conn:
            conn.commit()

        # Guarda los datos del usuario en una cookie
        cookie_data = {
            "id": user_id,
            "username": username,
            "email": email
        }

        response.set_cookie(
            key="user_data",
            value=json.dumps(cookie_data),
            httponly=False, # Desactivado para poder leerla despues desde JS
            secure=False,   # Desactivado porque el servidor no usan https
            samesite="Lax",
            max_age=60 * 60 * 24 # Duración de 1 día
        )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    finally:
        if close_conn and conn:
            conn.close()

    return {"status": "ok", "mensaje": "Inicio de sesión exitoso",
            "usuario": {"id": user_id, "username": username, "email": email}}

#-----------------------------------
#   Edita el usuario en la base de datos
#   String: username, String: email, String: pass, String: profilePicture -> update_user() -> JSON: user | HTTP Error
#-----------------------------------
def update_user(username: str, email: str, password: str, profilePicture: str, conn=None):
    close_conn = False
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT ID FROM USUARIOS WHERE USERNAME = %s OR EMAIL = %s", (username, email))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            user_id = user["ID"]
            updates, values = [], []

            if username:
                updates.append("USERNAME = %s")
                values.append(username)
            if email:
                updates.append("EMAIL = %s")
                values.append(email)
            if password:
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                updates.append("PASSWORD = %s")
                values.append(hashed_password)
            if profilePicture:
                updates.append("PROFILE_PICTURE = %s")
                values.append(profilePicture)

            if not updates:
                raise HTTPException(status_code=400, detail="No hay datos para actualizar")

            query = f"UPDATE USUARIOS SET {', '.join(updates)} WHERE ID = %s"
            values.append(user_id)
            cursor.execute(query, tuple(values))

            cursor.execute("SELECT ID, USERNAME, EMAIL, PROFILE_PICTURE, LAST_LOGIN FROM USUARIOS WHERE ID = %s", (user_id,))
            updated_user = cursor.fetchone()

        if close_conn:
            conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {e}")
    finally:
        if close_conn and conn:
            conn.close()

    return {"status": "ok", "mensaje": "Usuario actualizado correctamente", "usuario": updated_user}
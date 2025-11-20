#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#-----------------------------------
#   Fichero: core.py
#   Descripción: Funciones de manejo de usuarios
#-----------------------------------

import random
from datetime import datetime, timedelta
from fastapi import HTTPException, Response
from dataclasses import dataclass
import bcrypt
import json

from .db import get_connection
from .email_utils import send_confirmation_email


#-----------------------------------
#   Obtiene a todos los usuarios de la base de datos
#   get_all_users() -> Json: usuarios | Error
#-----------------------------------
def get_all_users():
    conn = None
    try:
        conn = get_connection()

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT ID, USERNAME, EMAIL, PROFILE_PICTURE, REGISTER_DATE, LAST_LOGIN FROM USUARIOS")
            users = cursor.fetchall()

        return {
            "status": "ok",
            "usuarios": users
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los usuarios: {e}")

    finally:
        if conn:
            conn.close()
    

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
#   Añade a la base de datos un usuario provisional y le envia el correo de verificacion
#   String: email, String: usernames, String: pass -> register_request() -> 200 OK | HTTP Error
#-----------------------------------
def register_request(email: str, username: str, password: str):
    conn = None
    try:
        conn = get_connection()

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT ID FROM USUARIOS WHERE EMAIL = %s",
                (email,)
            )
            row = cursor.fetchone()
            if row:
                raise HTTPException(status_code=400, detail="El usuario ya existe")

            cursor.execute(
                "SELECT 1 FROM CODIGOS WHERE EMAIL = %s",
                (email,)
            )
            pending = cursor.fetchone()

            if pending:
                cursor.execute(
                    "DELETE FROM CODIGOS WHERE EMAIL = %s",
                    (email,)
                )

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            code = str(random.randint(100000, 999999))
            expires = datetime.now() + timedelta(minutes=20)

            cursor.execute(
                "INSERT INTO CODIGOS (EMAIL, USERNAME, PASSWORD, CODE, EXPIRES) VALUES (%s, %s, %s, %s, %s)",
                (email, username, hashed_password, code, expires)
            )

        conn.commit()

        send_confirmation_email(email, code)

        return {
            "status": "ok",
            "mensaje": "Código de verificación enviado",
            "email": email
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar registro: {e}")
    finally:
        if conn:
            conn.close()

            
#-----------------------------------
#   Añade a la base de datos un usuario si el codigo de verificacion es correcto
#   String: email, R: code -> register_verify() -> 200 OK | HTTP Error
#-----------------------------------
def register_verify(email: str, code: int):
    conn = None
    try:
        conn = get_connection()

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT USERNAME, PASSWORD, CODE, EXPIRES FROM CODIGOS WHERE EMAIL = %s",
                (email,)
            )
            row = cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="No se encontró una solicitud de registro para este correo")

            if str(row["CODE"]) != str(code):
                raise HTTPException(status_code=400, detail="El código es incorrecto")

            if datetime.now() > row["EXPIRES"]:
                cursor.execute("DELETE FROM CODIGOS WHERE EMAIL = %s", (email,))
                conn.commit()
                raise HTTPException(status_code=400, detail="El código ha expirado")

            username = row["USERNAME"]
            hashed_password = row["PASSWORD"]

            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO USUARIOS (USERNAME, EMAIL, PASSWORD, REGISTER_DATE, LAST_LOGIN) "
                "VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, today, today)
            )

            user_id = cursor.lastrowid

            cursor.execute("DELETE FROM CODIGOS WHERE EMAIL = %s", (email,))

        conn.commit()

        return {
            "status": "ok",
            "mensaje": "Correo verificado y usuario creado exitosamente",
            "usuario": {
                "id": user_id,
                "username": username,
                "email": email
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar el código: {e}")
    finally:
        if conn:
            conn.close()


        
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

#-----------------------------------
#   Elimina un usuario de la BBDD
#   R: user_id, String: username, String: email -> delete_user() -> 200 OK | HTTP Error
#-----------------------------------
def delete_user(user_id: int = None, username: str = None, email: str = None, conn=None):
    if user_id is None and username is None and email is None:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un parámetro para eliminar al usuario")

    close_conn = False
    try:
        if conn is None:
            conn = get_connection()
            close_conn = True

        with conn.cursor(dictionary=True) as cursor:
            conditions, values = [], []
            if user_id is not None:
                conditions.append("ID = %s")
                values.append(user_id)
            if username is not None:
                conditions.append("USERNAME = %s")
                values.append(username)
            if email is not None:
                conditions.append("EMAIL = %s")
                values.append(email)

            where_clause = " OR ".join(conditions)

            cursor.execute(f"SELECT ID, USERNAME, EMAIL FROM USUARIOS WHERE {where_clause}", tuple(values))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            cursor.execute(f"DELETE FROM USUARIOS WHERE {where_clause}", tuple(values))

        if close_conn:
            conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {e}")
    finally:
        if close_conn and conn:
            conn.close()

    return {"status": "ok", "mensaje": "Usuario eliminado correctamente", "usuario": user}
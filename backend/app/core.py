#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#-----------------------------------

import mysql.connector
from datetime import datetime
from fastapi import HTTPException
import bcrypt

#-----------------------------------
#   Funcion para conectar a la base de datos
#-----------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="fedor",
        password="fedor123",
        database="RRVVDB"
    )

#-----------------------------------
#   Insert a new user into the database
#-----------------------------------
def insert_user(username: str, email: str, password: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if user or email already exists
        cursor.execute(
            "SELECT ID FROM USUARIOS WHERE USERNAME = %s OR EMAIL = %s",
            (username, email)
        )
        existing = cursor.fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="El usuario o el correo ya existen")
        
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        # Insert the new user
        cursor.execute(
            "INSERT INTO USUARIOS (USERNAME, EMAIL, PASSWORD, REGISTER_DATE, LAST_LOGIN) VALUES (%s, %s, %s, %s, %s)",
            (username, email, hashed_password.decode("utf-8"), today, today)
        )
        conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {e}")
    finally:
        conn.close()    

    return {"status": "ok", "mensaje": f"Usuario '{username}' creado exitosamente"}

#-----------------------------------
# Authenticate a user by username/email and password
#-----------------------------------
def login_user(username_or_email: str, password: str):
    row = None
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT ID, USERNAME, EMAIL, PASSWORD FROM USUARIOS WHERE USERNAME = %s OR EMAIL = %s",
                    (username_or_email, username_or_email)
                )
                row = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_id = row["ID"]
    username = row["USERNAME"]
    email = row["EMAIL"]
    stored_hash = row["PASSWORD"]

    # Check password
    if username == "Root" or email == "example@mail.com":
        if password != stored_hash:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    else:
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Update last login
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE USUARIOS SET LAST_LOGIN = %s WHERE ID = %s",
                    (today, user_id)
                )
                conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error actualizando último login")

    return {
        "status": "ok",
        "mensaje": "Inicio de sesión exitoso",
        "usuario": {
            "id": user_id,
            "username": username,
            "email": email,
        }
    }
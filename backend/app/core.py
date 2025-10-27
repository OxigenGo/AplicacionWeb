#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#-----------------------------------

import os
import sqlite3
from datetime import datetime
from fastapi import HTTPException
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "BioBase.db")

#-----------------------------------
#   Esta funcion recibe el nombre de usuario, el email y la contraseña del usuario que se desea crear y los inserta
#   en la base de datos si no existe ya alguien con esas credenciales
#-----------------------------------
#   String: user, String: email, String: password --> insert_user() --> 200 OK | Error
#-----------------------------------

def insert_user(username: str, email: str, password: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT ID FROM USUARIOS WHERE USERNAME = ? OR EMAIL = ?", (username, email))
        existing = cursor.fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="El usuario o el correo ya existen")
        
        today = datetime.now().strftime("%d-%m-%Y")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        cursor.execute(
            "INSERT INTO USUARIOS (USERNAME, EMAIL, PASSWORD, REGISTER_DATE, LAST_LOGIN) VALUES (?, ?, ?, ?, ?)",
            (username, email, hashed_password.decode("utf-8"), today, today)
        )
        conn.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en al base de datos: {e}")
    finally:
        conn.close()    
    return {"status": "ok", "mensaje": f"Usuario '{username}' creado exitosamente"}

#-----------------------------------
#   Esta funcion recibe el nombre de usuario o email y la contraseña del usuario y los busca en la base de datos
#-----------------------------------
#   String: user, String: password --> login_user() --> JSON: usuario | Error
#-----------------------------------

def login_user(username_or_email: str, password: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Buscamos a un usuario con el correo o nombre introducido
        cursor.execute(
            "SELECT ID, USERNAME, EMAIL, PASSWORD FROM USUARIOS WHERE USERNAME = ? OR EMAIL = ?",
            (username_or_email, username_or_email)
        )
        row = cursor.fetchone()

    finally:
        conn.close()

    # Si no existe, lanzamos un 404
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
     
    # Si existe, guardamos los datos
    user_id, username, email, stored_hash = row

    # Comprobamos si la contraseña es correcta
    if username == "Root" or email == "example@mail.com":
        if password != stored_hash:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    else:
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    today = datetime.now().strftime("%d-%m-%Y")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE USUARIOS SET LAST_LOGIN = ? WHERE ID = ?", (today, user_id))
        conn.commit()
    finally:
        conn.close()

    return {
        "status": "ok",
        "mensaje": "Inicio de sesión exitoso",
        "usuario": {
            "id": user_id,
            "username": username,
            "email": email,
        }
    }
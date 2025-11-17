#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 30 de octubre de 2025
#-----------------------------------
#   Fichero: test_core.py
#   Descripción: Módulo que realiza tests relacionados con la operación de usuarios
#   (registro, login y update) 
#-----------------------------------

import pytest
from backend.app.core import insert_user, login_user, update_user

#-----------------------------------
#   Test de registro de usuario.
#   Registra un usuario
#-----------------------------------

def test_insert_user(db):
    username = "testuser"
    email = "testuser@example.com"
    password = "testpass123"

    result = insert_user(username, email, password, conn=db)

    assert result["status"] == "ok"
    assert result["usuario"]["username"] == username
    assert result["usuario"]["email"] == email
    assert "id" in result["usuario"]
    
#-----------------------------------
#   Test de inicio de sesión.
#   Registra un usuario e inicia sesión con él
#-----------------------------------

def test_login_user(db):
    username = "testlogin"
    email = "testlogin@example.com"
    password = "secret123"

    insert_user(username, email, password, conn=db)

    # login_user espera el hash, no la contraseña cruda
    result = login_user(username, password, conn=db)

    assert result["status"] == "ok"
    assert result["usuario"]["username"] == username
    assert result["usuario"]["email"] == email
    assert "id" in result["usuario"]

#-----------------------------------
#   Test de edición de usuario.
#   Registra un usuario y lo actualiza
#-----------------------------------

def test_update_user(db):
    username = "updateuser"
    email = "updateuser@example.com"

    password = "mypassword"

    user = insert_user(username, email, password, conn=db)["usuario"]

    new_password = "newpassword"

    updated = update_user(username, email, new_password, None, conn=db)

    assert updated["status"] == "ok"
    assert updated["usuario"]["ID"] == user["id"]
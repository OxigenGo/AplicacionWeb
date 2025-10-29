#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#   Descripción: Endpoints de la API
#-----------------------------------

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .core import insert_user, login_user, update_user

app = FastAPI()

#-----------------------------------
#   Esquemas para valida datos JSON
#-----------------------------------

class RegistrationData(BaseModel):
    username: str
    email: str
    password: str
class LoginData(BaseModel):
    username_or_email: str
    password: str
class UpdateData(BaseModel):
    username: str
    email: str
    password: str
    profilePic: str

#-----------------------------------
#   POST /v1/users/register -> Registro / Crear nuevo usuario
#-----------------------------------

@app.post("/v1/users/register")
def create_user(user: RegistrationData):
    return insert_user(user.username, user.email, user.password)

#-----------------------------------
#   POST /v1/users/login -> Login
#-----------------------------------

@app.post("/v1/users/login")
def attempt_login(user: LoginData):
    return login_user(user.username_or_email, user.password)

#-----------------------------------
#   PUT /v1/users/update -> Edit user
#-----------------------------------

@app.put("/v1/users/update")
def attempt_update(user: UserCreate):
    return update_user(user.username, user.email, user.password, user.profilePic)

#-----------------------------------
#   SERVIR FICHEROS ESTATICOS
#-----------------------------------

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
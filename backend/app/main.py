#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#-----------------------------------

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .core import insert_user, login_user

app = FastAPI()

#-----------------------------------
#   Esquemas para valida datos JSON
#-----------------------------------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username_or_email: str
    password: str

#-----------------------------------
#   POST /v1/users -> Registro / Crear nuevo usuario
#-----------------------------------

@app.post("/v1/users")
def create_user(user: UserCreate):
    return insert_user(user.username, user.email, user.password)

#-----------------------------------
#   GET /v1/users -> Login
#-----------------------------------

@app.get("/v1/users")
def attempt_login(user: UserLogin):
    return login_user(user.username_or_email, user.password)

#-----------------------------------
#   SERVIR FICHEROS ESTATICOS
#-----------------------------------

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#-----------------------------------
#   Fichero: main.py
#   Descripción: Definicion de los modelos de datos y los endpoints de la APP Web
#-----------------------------------

import os
from typing import Optional
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .core import insert_user, login_user, update_user, register_request, register_verify, delete_user
from .sensores import bind_sensor_to_user, add_reading, delete_sensor_records, get_user_sensors

app = FastAPI()

#-----------------------------------
#   Esquemas para validar datos JSON
#-----------------------------------

class RegistrationData(BaseModel):
    username: str
    email: str
    password: str
    
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    
class VerifyRequest(BaseModel):
    email: str
    code: int
    
class LoginData(BaseModel):
    username_or_email: str
    password: str
    
class UpdateData(BaseModel):
    username: str
    email: str
    password: Optional[str]
    profilePic: Optional[str]
    
class UserDeletionData(BaseModel):
    user_id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    
class AssociationData(BaseModel):
    user_id: int
    uuid: str
    
class AssociationDeletionData(BaseModel):
    user_id: int
    erase_all: bool
    uuid: Optional[str]
    
class UserSensorList(BaseModel):
    user_id: int
    
class Reading(BaseModel):
    associated_uuid: str
    gas: float
    temperature: float
    position: Optional[str] = None

#-----------------------------------
#   POST /v1/users/register -> Registro / Crear nuevo usuario
#-----------------------------------

@app.post("/v1/users/register")
def attempt_create(user: RegistrationData):
    return insert_user(user.username, user.email, user.password)

#-----------------------------------
#   POST /v2/register/request -> Enviar código verificacion
#-----------------------------------

@app.post("/v2/register/request")
def attempt_register_request(request: RegisterRequest):
    return register_request(request.email, request.username, request.password)

#-----------------------------------
#   POST /v2/register/verify -> Verificar y crear usuario
#-----------------------------------

@app.post("/v2/register/verify")
def attempt_register_verify(request: VerifyRequest):
    return register_verify(request.email, request.code)

#-----------------------------------
#   POST /v1/users/login -> Iniciar sesión
#-----------------------------------

@app.post("/v1/users/login")
def attempt_login(user: LoginData, response: Response):
    return login_user(user.username_or_email, user.password, response)

#-----------------------------------
#   PUT /v1/users/update -> Editar usuario
#-----------------------------------

@app.put("/v1/users/update")
def attempt_update(user: UpdateData):
    return update_user(user.username, user.email, user.password, user.profilePic)

#-----------------------------------
#   DELETE /v1/users/update -> Eliminar usuario
#-----------------------------------

@app.delete("/v1/users/update")
def attempt_delete(user: UserDeletionData):
    return delete_user(user.user_id, user.username, user.email)


#-----------------------------------
#   POST /v1/data/bind -> Vincular sensor a usuario
#-----------------------------------

@app.post("/v1/data/bind")
def attempt_bind(user: AssociationData):
    return bind_sensor_to_user(user.user_id, user.uuid)

#-----------------------------------
#   DELETE /v1/data/bind -> Eliminar sensor o sensores de usuario
#-----------------------------------

@app.delete("/v1/data/bind")
def attempt_delete_bind(deletionData: AssociationDeletionData):
    return delete_sensor_records(deletionData.user_id, deletionData.erase_all, deletionData.uuid)

#-----------------------------------
#   POST /v1/data/user_sensors -> Obtener los sensores de un usuario y sus medidas
#-----------------------------------

@app.post("/v1/data/user_sensors")
def attempt_get_user_sensors(data: UserSensorList):
    return get_user_sensors(data.user_id)

#-----------------------------------
#   POST /v1/data/reading -> Añadir una medida de sensor
#-----------------------------------

@app.post("/v1/data/reading")
def attempt_register_reading(reading: Reading):
    return add_reading(reading.associated_uuid, reading.gas, reading.temperature, reading.position)

#-----------------------------------
#   SERVIR FICHEROS ESTATICOS
#-----------------------------------

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
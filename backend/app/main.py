#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 26 de octubre de 2025
#-----------------------------------
#   Fichero: main.py
#   Descripción: Definicion de los routers de la API
#-----------------------------------

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers.users import router as users_router
from .routers.register import router as register_router
from .routers.sensors import router as sensors_router
from .routers.system import router as system_router
from .routers.tracks import router as track_router
from .routers.rewards import router as reward_router

app = FastAPI()

# Routers
app.include_router(users_router)
app.include_router(register_router)
app.include_router(sensors_router)
app.include_router(system_router)
app.include_router(track_router)
app.include_router(reward_router)

# Montar frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
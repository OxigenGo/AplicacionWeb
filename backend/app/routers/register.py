#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 7 de diciembre de 2025
#-----------------------------------
#   Fichero: register.py
#   Descripción: Endpoints de registro de usuarios
#-----------------------------------

from fastapi import APIRouter
from ..schemas.register import (
    RegisterRequest, VerifyRequest
)
from ..user_actions import (
    register_request, register_verify
    )

router = APIRouter(prefix="/v2/register", tags=["Register"])


@router.post("/request")
def attempt_register_request(request: RegisterRequest):
    return register_request(request.email, request.username, request.password)


@router.post("/verify")
def attempt_register_verify(request: VerifyRequest):
    return register_verify(request.email, request.code)

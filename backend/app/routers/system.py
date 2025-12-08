from fastapi import APIRouter
from typing import Optional
from ..schemas.system import (
    IncidentFilter, IncidentCreate
)
from ..system_actions import (
    get_incidents, create_incident
)

router = APIRouter(prefix="/v1/system", tags=["System"])

@router.post("/incidents")
def attempt_get_all_incidents(filters: Optional[IncidentFilter] = None):
    return get_incidents(filters)

@router.post("/incidents/create")
def attempt_create_incident(incident: IncidentCreate):
    return create_incident(incident)
from fastapi import APIRouter, Response
from ..schemas.tracks import (
    CreateTrack, DeleteTrack, CreateTrackPoint,
    GetUserTracks, GetTrackPoints
)
from ..track_logic import (
    create_track, delete_track, create_punto_recorrido,
    get_recorridos_by_user, get_puntos_recorrido
)


router = APIRouter(prefix="/v1/recorridos", tags=["Recorridos"])


@router.post("")
def attempt_create_track(trackInfo: CreateTrack):
    return create_track(trackInfo.user_id)


@router.delete("")
def attempt_delete_track(trackInfo: DeleteTrack):
    return delete_track(trackInfo.track_id)


@router.post("/puntos")
def attempt_create_track_point(trackPointInfo: CreateTrackPoint):
    return create_punto_recorrido(trackPointInfo.track_id, trackPointInfo.position)


@router.post("/usuario")
def attempt_get_user_tracks(trackInfo: GetUserTracks):
    return get_recorridos_by_user(trackInfo.user_id)


@router.post("/puntos_recorrido")
def attempt_get_track_points(trackInfo: GetTrackPoints):
    return get_puntos_recorrido(trackInfo.track_id)
from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Union

#Validador de puntos GeoJSON 
class GeoJSONPoint(BaseModel):
    type: Literal["Point"]
    coordinates: List[float] = Field(..., min_items=2, max_items=2)
    
    
class CreateTrack(BaseModel):
    user_id: int


class DeleteTrack(BaseModel):
    track_id: int
    
    
class CreateTrackPoint(BaseModel):
    track_id: int
    position: GeoJSONPoint
    

class GetUserTracks(BaseModel):
    user_id: int
    
class GetTrackPoints(BaseModel):
    track_id: int
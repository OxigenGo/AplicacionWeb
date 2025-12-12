from fastapi import APIRouter
from ..schemas.sensors import (
    AssociationData, AssociationDeletionData,
    UserSensorList, Reading, MapReading, UserToday
)
from ..sensores import (
    bind_sensor_to_user, add_reading,
    delete_sensor_records, get_user_sensors,
    get_all_readings_for_datetime,
    get_today_measurements_for_user
)

router = APIRouter(prefix="/v1/data", tags=["Sensors"])

@router.post("/bind")
def attempt_bind(user: AssociationData):
    return bind_sensor_to_user(user.user_id, user.uuid)


@router.delete("/bind")
def attempt_delete_bind (deletionData: AssociationDeletionData):
    return delete_sensor_records(
        deletionData.user_id,
        deletionData.erase_all,
        deletionData.uuid
    )
    

@router.post("/user_sensors")
def attempt_get_user_sensors(data: UserSensorList):
    return get_user_sensors(data.user_id)


@router.post("/reading")
def attempt_register_reading(reading: Reading):
    return add_reading(
        reading.associated_uuid,
        reading.gasType,
        reading.gas,
        reading.temperature,
        reading.position
    )

@router.post("/map_readings")
def attempt_get_all_readings(selection: MapReading):
    return get_all_readings_for_datetime(selection.datetime, selection.gasType)
    
@router.post("/today")
def attempt_get_today_for_user(user: UserToday):
    return get_today_measurements_for_user(user.user_id)
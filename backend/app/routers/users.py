from fastapi import APIRouter, Response
from ..schemas.users import (
    RegistrationData, LoginData,
    UpdateData, UserDeletionData
)
from ..user_actions import (
    insert_user, login_user, update_user,
    delete_user, get_all_users
)

router = APIRouter(prefix="/v1/users", tags=["Users"])


@router.get("")
def attempt_get_all_users():
    return get_all_users()


@router.post("/register")
def attempt_create(user: RegistrationData):
    return insert_user(user.username, user.email, user.password)


@router.post("/login")
def attempt_login(user: LoginData, response: Response):
    return login_user(user.username_or_email, user.password, response)


@router.put("/update")
def attempt_update(user: UpdateData):
    return update_user(user.username, user.email, user.password, user.profilePic)


@router.delete("/update")
def attempt_delete(user: UserDeletionData):
    return delete_user(user.user_id, user.username, user.email)

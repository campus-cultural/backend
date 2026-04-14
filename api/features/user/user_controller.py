from __future__ import annotations

from fastapi import APIRouter, Response, status

from api.features.user.user_schemas import (
    UserCreateIn,
    UserCreateOut,
    UserReadOut,
    UserUpdateIn,
    UserUpdateOut,
)
from api.shared.dependencies import UserServiceDependency

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("", response_model=UserCreateOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateIn, service: UserServiceDependency) -> UserCreateOut:
    return UserCreateOut.model_validate(service.create(payload))


@router.get("", response_model=list[UserReadOut])
def list_users(service: UserServiceDependency) -> list[UserReadOut]:
    return [UserReadOut.model_validate(user) for user in service.list_all()]


@router.get("/{user_id}", response_model=UserReadOut)
def get_user(user_id: int, service: UserServiceDependency) -> UserReadOut:
    return UserReadOut.model_validate(service.get_by_id(user_id))


@router.put("/{user_id}", response_model=UserUpdateOut)
def update_user(
    user_id: int,
    payload: UserUpdateIn,
    service: UserServiceDependency,
) -> UserUpdateOut:
    return UserUpdateOut.model_validate(service.update(user_id, payload))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserServiceDependency) -> Response:
    service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

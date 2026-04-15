from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from api.features.user.user import User
from api.features.user.user_schemas import (
    UserCreateIn,
    UserCreateOut,
    UserReadOut,
    UserUpdateIn,
    UserUpdateOut,
)
from api.features.user.user_service import UserService
from api.shared.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserCreateOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateIn,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserCreateOut:
    return UserCreateOut.model_validate(await service.create(payload))


@router.get("", response_model=list[UserReadOut])
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
) -> list[UserReadOut]:
    users: list[User] = await service.list_all()
    users_dto = []
    for user in users:
        users_dto.append(UserReadOut.model_validate(user))
    return users_dto


@router.get("/{user_id}", response_model=UserReadOut)
async def get_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadOut:
    return UserReadOut.model_validate(await service.get_by_id(user_id))


@router.put("/{user_id}", response_model=UserUpdateOut)
async def update_user(
    user_id: int,
    payload: UserUpdateIn,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserUpdateOut:
    return UserUpdateOut.model_validate(await service.update(user_id, payload))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
) -> Response:
    await service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

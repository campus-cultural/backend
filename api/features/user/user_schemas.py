from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from api.features.user.user import UserTipo


class UserBaseSchema(BaseModel):
    tipo: UserTipo
    ra: str
    nome: str
    senha: str


class UserCreateIn(UserBaseSchema):
    pass


class UserCreateOut(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserReadOut(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdateIn(UserBaseSchema):
    pass


class UserUpdateOut(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

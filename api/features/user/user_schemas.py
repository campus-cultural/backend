from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserBaseSchema(BaseModel):
    tipo: Literal["aluno", "professor"]
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

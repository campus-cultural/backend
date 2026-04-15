from __future__ import annotations

from pydantic import BaseModel, ConfigDict, model_validator

from api.features.user.user import UserRole


class UserBaseSchema(BaseModel):
    role: UserRole
    email: str
    name: str
    is_active: bool
    ra: str | None = None

    @model_validator(mode="after")
    def validate_ra(self) -> UserBaseSchema:
        if self.role != UserRole.STUDENT and self.ra is not None:
            raise ValueError("ra must be null for non-student users")
        return self


class UserCreateIn(UserBaseSchema):
    password: str


class UserCreateOut(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserReadOut(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdateIn(UserBaseSchema):
    password: str


class UserUpdateOut(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

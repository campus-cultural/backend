from __future__ import annotations

from api.features.user.user_models import UserModel
from api.features.user.user_repository import UserRepository
from api.features.user.user_schemas import UserCreateIn, UserUpdateIn
from api.shared.exceptions import ResourceNotFoundError


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create(self, payload: UserCreateIn) -> UserModel:
        user = UserModel(**payload.model_dump())
        return self.repository.create(user)

    def list_all(self) -> list[UserModel]:
        return self.repository.list_all()

    def get_by_id(self, user_id: int) -> UserModel:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise ResourceNotFoundError(f"Usuario {user_id} nao encontrado")
        return user

    def update(self, user_id: int, payload: UserUpdateIn) -> UserModel:
        user = self.get_by_id(user_id)
        for field, value in payload.model_dump().items():
            setattr(user, field, value)
        return self.repository.update(user)

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.repository.delete(user)

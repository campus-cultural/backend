from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from api.features.user.user_models import UserModel


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def list_all(self) -> list[UserModel]:
        return list(self.session.scalars(select(UserModel).order_by(UserModel.id)))

    def get_by_id(self, user_id: int) -> UserModel | None:
        return self.session.get(UserModel, user_id)

    def get_by_ra(self, ra: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.ra == ra)
        return self.session.scalar(statement)

    def update(self, user: UserModel) -> UserModel:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: UserModel) -> None:
        self.session.delete(user)
        self.session.commit()

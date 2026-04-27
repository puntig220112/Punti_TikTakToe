from sqlalchemy import Engine
from sqlalchemy.orm import Session

from BACKEND_NAME_PLACEHOLDER.model import Entity, Person, User
from BACKEND_NAME_PLACEHOLDER.schema import EntityBase
from BACKEND_NAME_PLACEHOLDER.schema._user import UserCreate


class Crud:
    def __init__(self, engine: Engine):
        self._engine: Engine = engine

    def get_users(self) -> list[User]:
        with Session(self._engine) as db:
            users = db.query(User).all()
            for u in users:
                db.expunge(u)
            return users

    def create_user(self, user_data: UserCreate) -> User:
        with Session(self._engine) as db:
            new_person = Person(
                name=user_data.last_name,
                first_name=user_data.first_name,
                type="persons"
            )
            db.add(new_person)
            db.flush()


            new_user = User(
                user_name=user_data.user_name,
                password_hash=user_data.password,
                entity_id=new_person.id
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.expunge(new_user)
            return new_user

    def get_persons(self, filter: str | None = None) -> list[Person]:
        if not filter:
            return []
        return []

    def get_entities(self, filter: str | None = None) -> list[Entity]:
        if not filter:
            return []
        return []

    def create_entity(self, new_entity: EntityBase):
        with Session(self._engine) as session:
            assert new_entity
            assert session

from typing import Optional

from sqlalchemy.orm import Session

from .. import DeclarativeBase


class BaseRepository:
    _table: DeclarativeBase


class BaseCRUDRepository(BaseRepository):
    _table: DeclarativeBase

    @classmethod
    def search(cls, id: int, *, session: Session) -> Optional[DeclarativeBase]:
        return session.query(cls._table).get(id)

    @classmethod
    def insert(cls, *, session: Session, commit: bool, **kwargs) -> DeclarativeBase:
        record = cls._table(**kwargs)

        session.add(record)
        if commit:
            session.commit()
            session.flush()

        return record

    @classmethod
    def update(
        cls, record: DeclarativeBase, *, session: Session, commit: bool, exclude_none: bool = True, **kwargs
    ) -> DeclarativeBase:
        for col, value in kwargs.items():
            if not hasattr(record, col):
                raise TypeError(f"{record.__class__.__name__} as no column {col}")
            if exclude_none and value is None:
                continue
            setattr(record, col, value)

        if commit:
            session.commit()
            session.flush()

        return record

    @classmethod
    def delete(cls, record: DeclarativeBase, *, session: Session, commit: bool):
        session.delete(record)

        if commit:
            session.commit()
            session.flush()

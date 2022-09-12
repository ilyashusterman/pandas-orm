from abc import abstractmethod

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class BaseModelMixin:

    @classmethod
    @abstractmethod
    def get_constraint(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_static_columns(cls):
        raise NotImplementedError

    @classmethod
    def get_dynamic_columns(cls):
        return [
            col.name for col in cls.__table__.columns
            if col.name not in cls.get_static_columns() + ['id']
        ]

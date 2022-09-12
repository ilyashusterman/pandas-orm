from sqlalchemy import BigInteger, Column, String, UniqueConstraint, Index

from sqlalchemy_backend.models.base import Base


class Collaborator(Base):
    __tablename__ = 'collaborator'

    id = Column('id', BigInteger, primary_key=True)
    name = Column('name', String(200), nullable=False)
    first_name = Column('first_name', String(200), nullable=False)
    last_name = Column('last_name', String(200), nullable=False)
    email = Column('email', String(200), nullable=True)
    profile_link = Column('profile_link', String(250), nullable=True)
    image_url = Column('image_url', String(250), nullable=True)

    collaborator_unique_key = UniqueConstraint('email', 'name', name='collaborator_unique_key')
    collaborator_name_search_idx = Index('collaborator_name_search_idx', 'name', 'first_name', 'last_name')

    def __str__(self):
        return f'<<< Collaborator {self.name} >>> {self.email}'

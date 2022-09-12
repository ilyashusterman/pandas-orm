from dataclasses import dataclass

from sqlalchemy_backend.data_classes.base_data_class import BaseDataClass


@dataclass
class Collaborator(BaseDataClass):
    name: str
    email: str
    first_name: str = None
    last_name: str = None
    email: str = None
    profile_link: str = None
    image_url: str = None

    def __str__(self):
        return f'<<< Collaborator {self.name} >>> {self.email}'

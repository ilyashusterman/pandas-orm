import os

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
    try:
        from django.core.asgi import get_asgi_application

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')

        application = get_asgi_application()
        from pandas_orm.django.db import models
    except ModuleNotFoundError as e:
        raise e
except RuntimeError as e:
    pass

from .collaborator import Collaborator
from .auth import User
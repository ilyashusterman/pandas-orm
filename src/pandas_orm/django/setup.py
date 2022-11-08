from __future__ import annotations

from dataclasses import dataclass
from typing import Collection, Dict

from sqlalchemy.engine.url import make_url


def django_database(url: str, engine: str = 'django.db.backends.postgresql'):
    """
    :param url: Database string representation
    :param engine: database engine for django framework
    :return: Django Dict Database Representation
    """
    db_url = get_db_url(url)
    database_setup = {
        'ENGINE': engine,
        'NAME': db_url.database,
        'USER': db_url.username,
        'PASSWORD': db_url.password,
        'HOST': db_url.host,
        'PORT': db_url.port,
    }
    return database_setup


DJANGO_DATABASE_DEFAULT_KEY = 'default'


@dataclass
class DjangoDataBaseConf:
    engine: str
    url: str
    key: str = DJANGO_DATABASE_DEFAULT_KEY


def get_django_databases(configs: Dict | Collection[Dict]=None, BASE_DIR=None):
    """
    Initialize django database keys for settings.py
    :param configs:
    :param BASE_DIR: django base directory
    :return: django DATABASES Dict
    """
    if not configs:
        if not BASE_DIR:
            raise Exception('did not specified BASE_DIR for default sqlite3')
        return {
            DJANGO_DATABASE_DEFAULT_KEY:
                {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
        }
    if isinstance(configs, dict):
        configs = [configs]

    if not isinstance(configs[0], dict):
        raise Exception(f'Database config expected to be dictionary, got {type(configs[0])}')

    config_objs = [DjangoDataBaseConf(**conf) for conf in configs]
    return {
        django_db.key: django_database(django_db.url, django_db.engine)
        for django_db in config_objs
    }


def get_db_url(url):
    return make_url(url)

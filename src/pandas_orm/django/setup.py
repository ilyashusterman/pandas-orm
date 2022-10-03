from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.engine.url import make_url


def django_database(url: str, engine:str='django.db.backends.postgresql'):
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


@dataclass
class DjangoDataBaseConf:
    engine: str
    url: str
    key: str = 'default'


def get_django_databases(*configs):
    config_objs = configs
    if not config_objs:
        raise Exception('Empty domain urls')
    if isinstance(config_objs[0], dict):
        config_objs = [DjangoDataBaseConf(**conf) for conf in config_objs]
    """
    :param urls: 
    :return: django DATABASES Dict
    """
    return {
        django_db.key: django_database(django_db.url, django_db.engine)
        for django_db in config_objs
    }


def get_db_url(url):
    return make_url(url)

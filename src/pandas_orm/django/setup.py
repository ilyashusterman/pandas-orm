from sqlalchemy.engine.url import make_url


def get_django_db(url, engine='django.db.backends.postgresql'):
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


def get_db_url(url):
    return make_url(url)

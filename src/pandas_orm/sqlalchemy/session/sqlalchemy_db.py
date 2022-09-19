from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


databases = dict()


def get_global_instance_db(db_url):
    """
        modify global copy of databases for global instances usage
        to create only one instance per python interpreter usage
    :param db_url: str
    :return: DatabaseSession
    """
    global databases
    if db_url not in databases:
        databases[db_url] = DatabaseSession(db_url)
    return databases[db_url]


class DatabaseSession:
    """
    responsible to handle engine scope and session scope with sqlalchemy frameworke
    Usage:
    In [0]: db = DatabaseSession(url)
    In [1]: with db.session() as session:
       ...:     result = session.execute('select * from collaborator where id=144')
    In [2]: result.fetchall()
    Out[2]: [(1, u'name name', u'test test',...]
    """
    def __init__(self, url=None, session_scope_func=None, engine_scope_func=None):
        """
        :param url: url for the database
        :param session_scope_func: or session_scope to initialize sqlalchemy session
        :param engine_scope_func: or engine_scope to initialize sqlalchemy engine
        """
        self.url = url
        self.session_scope_func = session_scope_func
        self.engine_scope_func = engine_scope_func

    def session(self):
        """
        :return: session scope function context
        """
        if self.session_scope_func:
            return self.session_scope_func()
        return session_scope(self.url)

    def engine(self):
        """
        :return: engine scope function context
        """
        if self.engine_scope_func:
            return self.engine_scope_func()
        engine = engine_scope(self.url)
        return engine

    @classmethod
    def get_db_session(cls, url):
        """ initialize global variable singleton """
        return get_global_instance_db(url)


@contextmanager
def session_scope(db_url):
    """Provide a transactional scope around a series of operations."""
    engine, session = get_session_engine(db_url)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        engine.dispose()


@contextmanager
def engine_scope(db_url):
    """Provide a transactional scope around a series of operations."""
    engine, session = get_session_engine(db_url)
    try:
        yield engine
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        engine.dispose()


def get_session_engine(db_url):
    """
    configure Session class with desired options
    :param db_url: str connection for sqlalchemy_backend
    :return: engine, Session
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    conn = engine.connect()
    session = Session(bind=conn)
    return engine, session

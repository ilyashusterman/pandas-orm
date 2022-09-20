sqlalchemy usage
================

Sqlalchemy ORM Package Interfaces
---------------------------------

.. autofunction:: pandas_orm.sqlalchemy.query.query_to_dataframe
.. code-block:: console

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    from pandas_orm.sqlalchemy.query import query_to_dataframe

    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    conn = engine.connect()
    session = Session(bind=conn)

    dataframe = query_to_dataframe(session.query(Collaborator))

.. autofunction:: pandas_orm.sqlalchemy.query.to_dataframe
.. code-block:: console

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    from pandas_orm.sqlalchemy.query import to_dataframe

    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    conn = engine.connect()
    session = Session(bind=conn)

    @to_dataframe
    def get_all_objects():
        return session.query(Collaborator)

    df = get_all_objects()

Sqlalchemy ORM DataFrame
------------------------
.. autoclass:: pandas_orm.sqlalchemy.dataframe::DataFrame
   :members:

.. code-block:: console

    from pandas_orm.sqlalchemy.dataframe import DataFrame

    df_new = DataFrame([dict(
        name="test",
        email="test@test.test",
        last_name="test_dataframe_bulk_save"
    )], orm_model=Collaborator)
    saved_df = df_new.bulk_save(
        engine_context_func=engine_context,
        returning_id=True
    )
    saved_df.bulk_save() # or naive way id didn't specified unique_fields or update_fields


Sqlalchemy ORM Database Context
-------------------------------

you can use the ``from pandas_orm.sqlalchemy.model_manager import ModelManager`` class:

.. autoclass:: pandas_orm.sqlalchemy.model_manager::ModelManager
   :members:

.. code-block:: console

    from pandas_orm.sqlalchemy.model_manager import ModelManager

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


    def print_dataframe():
        # your database connection string
        url = 'postgresql://docker:localone@localhost:5432/local_database'
        model_manager = ModelManager(url=url, model=Collaborator)
        df = model_manager.all()
        assert isinstance(df, DataFrame)
        print(df.to_string())


.. autofunction:: pandas_orm.sqlalchemy.crud.save.bulk_save


Sqlalchemy Database Context
---------------------------
.. autoclass:: pandas_orm.sqlalchemy.session.sqlalchemy_db::DatabaseSession
   :members:
   :inherited-members:
   :private-members:

.. code-block:: console

    from pandas_orm.sqlalchemy.session.sqlalchemy_db import DatabaseSession

    In [0]: db = DatabaseSession(url)
    In [1]: with db.session() as session:
       ...:     result = session.execute('select * from collaborator where id=1')
    In [2]: result.fetchall()
    Out[2]: [(1, u'name name', u'test test',...]

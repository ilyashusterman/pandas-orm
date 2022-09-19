sqlalchemy usage
================

Sqlalchemy Package Interfaces
-----------------------------

.. autofunction:: pandas_orm.sqlalchemy.query.query_to_dataframe

you can use the ``from pandas_orm.sqlalchemy.model_manager import ModelManager`` class:

.. autoclass:: pandas_orm.sqlalchemy.model_manager::ModelManager
   :members:
   :inherited-members:

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





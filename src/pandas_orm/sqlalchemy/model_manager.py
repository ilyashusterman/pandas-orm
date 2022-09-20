from sqlalchemy.orm import declarative_base

from pandas_orm.sqlalchemy.crud.save import bulk_save
from pandas_orm.sqlalchemy.query import to_dataframe
from pandas_orm.sqlalchemy.dataframe import DataFrame, initialized_dataframe
from pandas_orm.sqlalchemy.session.sqlalchemy_db import DatabaseSession


class ModelManager(DatabaseSession):
    """
    Manage engine and session scopes to the database contexts
    """
    def __init__(self, url: str= None, model: declarative_base= None, *args, **kwargs):
        """
        :param url: str database connection string
        :param model: declarative_base Sqlalchemy Model
        :param args:
        :param kwargs:
        """
        super(__class__, self).__init__(url=url, *args, **kwargs)
        self.model = model

    @to_dataframe
    def all(self):
        with self.session() as session:
            return session.query(self.model)

    def delete(self, **kwargs):
        with self.session() as session:
            prepared_statement = session.query(self.model)
            for key, value in kwargs.items():
                prepared_statement = prepared_statement.filter(
                    getattr(self.model, key) == value
                )
            return prepared_statement.delete()

    @to_dataframe
    def get(self, **kwargs):
        with self.session() as session:
            prepared_statement = session.query(self.model)
            for key, value in kwargs.items():
                prepared_statement = prepared_statement.filter(
                    getattr(self.model, key) == value
                )
            return prepared_statement

    def bulk_save(self, records, unique_fields=None, update_fields=None, returning_id=False, model=None) -> DataFrame:
        model = model if model else self.model
        new_records = bulk_save(
            dataframe=records,
            model=model,
            unique_fields=unique_fields,
            update_fields=update_fields,
            returning_id=returning_id,
            engine_context_func=self.engine
        )
        return initialized_dataframe(new_records, self)







import time
import logging
from functools import wraps

from .exceptions import PandasDBAlchemyUpdateColumnsNotSupported

from .dataframe import DataFrame
from sqlalchemy.dialects.postgresql import insert


def execute_sql(func):
    """
    Reads the sql alchemy statement queryset as a dataframe
    :param func: function that returns statement, engine
    :return: DataFrame
    """
    logger = logging.getLogger('PandasDBLogger')
    logger.setLevel(logging.DEBUG)

    @wraps(func)
    def wrapper(*args, **kwargs):
        statement, engine = func(*args, **kwargs)
        time_started = time.time()
        records_size = kwargs['operate_df'].shape[0] if isinstance(
            kwargs['operate_df'], DataFrame) else len(kwargs['operate_df'])
        logger.debug('Method %s started ...' % func.__name__.title())
        result = engine.execute(
            statement
        )
        querying_time = time.time() - time_started
        logger.debug('Done Executing sql %s in %f seconds %s records' % (
            func.__name__, querying_time, records_size))
        return result

    return wrapper


class DataFrameExecuteSql:

    @classmethod
    @execute_sql
    def save_dataframe_to_sql_returning_id(cls, engine, operate_df, model,
                                           update_column, constraint):
        statement = cls.base_save_dataframe_to_sql(operate_df, model,
                                                   update_column, constraint)
        statement = statement.returning(model.id)
        return statement, engine

    @classmethod
    @execute_sql
    def save_dataframe_to_sql(cls, engine, operate_df, model, update_column,
                              constraint):
        statement = cls.base_save_dataframe_to_sql(operate_df, model,
                                                   update_column, constraint)
        return statement, engine

    @classmethod
    @execute_sql
    def save_dataframe_to_sqlite(cls, engine, operate_df, model,
                                 update_column, constraint):
        statement, record_columns = cls.get_insert_statement(model,
                                                             operate_df)
        return statement, engine

    @classmethod
    def base_save_dataframe_to_sql(cls, operate_df, model, update_column,
                                   constraint):
        statement, record_columns = cls.get_insert_statement(model,
                                                             operate_df)
        set_update_attributes = cls.get_save_attributes(statement,
                                                        update_column, model,
                                                        record_columns)
        if not set_update_attributes:
            statement = statement.on_conflict_do_nothing(
                constraint=constraint,
            )
        else:
            statement = statement.on_conflict_do_update(
                constraint=constraint,
                set_=set_update_attributes
            )
        return statement

    @classmethod
    @execute_sql
    def insert_dataframe_to_sql(cls, engine, operate_df, model,
                                update_column=None):
        statement, record_columns = cls.get_insert_statement(model,
                                                             operate_df)
        return statement, engine

    @classmethod
    def get_save_attributes(cls, statement, update_column, model,
                            record_columns=None):
        if isinstance(update_column, str):
            return {update_column: getattr(statement.excluded, update_column)}
        elif isinstance(update_column, tuple) or isinstance(update_column,
                                                            list):
            save_columns = {column: getattr(statement.excluded, column) for
                            column in update_column}
            if record_columns:
                save_columns = {column: value for column, value in
                                save_columns.items()
                                if column in record_columns}
            return save_columns
        else:
            raise PandasDBAlchemyUpdateColumnsNotSupported(model)

    @classmethod
    @execute_sql
    def insert_dataframe_to_sql(cls, engine, operate_df, model,
                                update_column=None):
        statement, record_columns = cls.get_insert_statement(model,
                                                             operate_df)
        return statement, engine

    @classmethod
    @execute_sql
    def insert_dataframe_to_sql_returning_ids(cls, engine, operate_df, model):
        statement, record_columns = cls.get_insert_statement(model,
                                                             operate_df)
        statement = statement.returning(model.id)
        return statement, engine

    @classmethod
    def get_insert_statement(cls, model, operate_df):
        records_rows = cls.get_records(operate_df)
        statement = cls.prepare_bulk_statement(model, records_rows)
        return statement, records_rows[0].keys()

    @classmethod
    def get_records(cls, operate_df):
        if isinstance(operate_df, DataFrame) or hasattr(operate_df, 'to_dict'):
            return operate_df.to_dict('records')
        elif isinstance(operate_df, dict):
            return [operate_df]
        assert isinstance(operate_df, list)
        return operate_df

    @classmethod
    def prepare_bulk_statement(cls, model, records_rows):
        return insert(model.__table__).values(records_rows)
import time
from functools import wraps

from pandas import DataFrame

from pandas_orm.base.log import get_logger
from pandas_orm.sqlalchemy.exceptions import AlchemyUpdateColumnsNotSupported

from sqlalchemy.dialects.postgresql import insert


def execute_sql(func):
    """
    Reads the sql alchemy statement queryset as a dataframe
    :param func: function that returns statement, engine
    :return: DataFrame
    """
    logger = get_logger()

    @wraps(func)
    def wrapper(*args, **kwargs):
        statement, engine = func(*args, **kwargs)
        time_started = time.time()
        records_size = kwargs['dataframe'].shape[0] if isinstance(
            kwargs['dataframe'], DataFrame) else len(kwargs['dataframe'])
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
    def save_dataframe_to_sql_returning_id(cls, engine, dataframe, model,
                                           update_column, constraint):
        statement = cls.base_save_dataframe_to_sql(dataframe, model,
                                                   update_column, constraint)
        statement = statement.returning(model.id)
        return statement, engine

    @classmethod
    @execute_sql
    def save_dataframe_to_sql(cls, engine, dataframe, model, update_column,
                              constraint):
        statement = cls.base_save_dataframe_to_sql(dataframe, model,
                                                   update_column, constraint)
        return statement, engine

    @classmethod
    @execute_sql
    def save_dataframe_to_sqlite(cls, engine, dataframe, model,
                                 update_column, constraint):
        statement, record_columns = cls.get_insert_statement(model,
                                                             dataframe)
        return statement, engine

    @classmethod
    def base_save_dataframe_to_sql(cls, dataframe, model, update_column,
                                   constraint):
        statement, record_columns = cls.get_insert_statement(model,
                                                             dataframe)
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
    def insert_dataframe_to_sql(cls, engine, dataframe, model,
                                update_column=None):
        statement, record_columns = cls.get_insert_statement(model,
                                                             dataframe)
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
            raise AlchemyUpdateColumnsNotSupported(model)

    @classmethod
    @execute_sql
    def insert_dataframe_to_sql(cls, engine, dataframe, model,
                                update_column=None):
        statement, record_columns = cls.get_insert_statement(model,
                                                             dataframe)
        return statement, engine

    @classmethod
    @execute_sql
    def insert_dataframe_to_sql_returning_ids(cls, engine, dataframe, model):
        statement, record_columns = cls.get_insert_statement(model,
                                                             dataframe)
        statement = statement.returning(model.id)
        return statement, engine

    @classmethod
    def get_insert_statement(cls, model, dataframe):
        records_rows = cls.get_records(dataframe)
        statement = cls.prepare_bulk_statement(model, records_rows)
        return statement, records_rows[0].keys()

    @classmethod
    def get_records(cls, dataframe):
        if isinstance(dataframe, DataFrame) or hasattr(dataframe, 'to_dict'):
            return dataframe.to_dict('records')
        elif isinstance(dataframe, dict):
            return [dataframe]
        assert isinstance(dataframe, list)
        return dataframe

    @classmethod
    def prepare_bulk_statement(cls, model, records_rows):
        return insert(model.__table__).values(records_rows)
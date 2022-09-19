import time
from functools import wraps

import sqlalchemy
from pandas import read_sql, concat
from sqlalchemy.orm import Query

from pandas_orm.base.log import get_logger
from pandas_orm.sqlalchemy.exceptions import ToDataFrameNotEmpty

from pandas_orm.sqlalchemy.dataframe import DataFrame
from pandas_orm.sqlalchemy.dataframe import is_dataframe


def to_dataframe_gen(func):
    """
    Annotation that wraps function that returns generator(sqlalchemy.orm.query.Query)
     reads it to a dataframe
    Reads the query statements as a dataframe
    :param func: function that returns generator/list sqlalchemy.Session.query
    :return: DataFrame
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        dataframes = []
        for result_query in gen:
            df = query_to_dataframe(result_query)
            dataframes.append(df)
        df_results = concat(dataframes)
        return df_results

    return wrapper


def to_dataframe(func):
    """
    Annotation that wraps function that returns sqlalchemy.orm.query.Query
     reads it to a dataframe
    :param func: function that returns sqlalchemy.Session.query
    :return: DataFrame
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        query = func(*args, **kwargs)
        df = query_to_dataframe(query)
        wrapped_df = DataFrame(df)
        if args and args[0].__class__.__name__ == 'ModelManager':
            wrapped_df.model_manager = args[0]
            wrapped_df.__model__ = wrapped_df.model_manager.model
        return wrapped_df

    return wrapper


def query_to_dataframe(query: sqlalchemy.orm.query.Query):
    """
    Return a DataFrame read from sqlalchemy.orm.query.Query
    :param query: : sqlalchemy.orm.query.Query
    :return: dataframe represent of the result
    :rtype: DataFrame
    """
    logger = get_logger()
    if query is None:
        return DataFrame([])
    if is_dataframe(query):
        if not query.empty:
            raise ToDataFrameNotEmpty(query)
        return query
    assert isinstance(query, Query)
    time_started = time.time()
    logger.debug('Querying started %s ...' % query.statement)
    result_dataframe = read_sql(query.statement,
                                query.session.bind)
    querying_time = time.time() - time_started
    logger.debug('Done Querying in %f seconds ' % querying_time)
    return result_dataframe

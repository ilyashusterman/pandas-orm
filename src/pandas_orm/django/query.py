import time
from functools import wraps

from django.db.models import QuerySet

from pandas_orm.base.log import get_logger
from pandas_orm.django.dataframe import DataFrame


def get_result_query_columns(result_query: QuerySet):
    """
    :param result_query: django.db.models.QuerySet
    :return: List[field_name] of the django model
    """
    return [field.name for field in result_query.model._meta.fields]


def query_to_dataframe(query: QuerySet):
    """
    :param query: django.db.models.QuerySet
    :return: DataFrame
    """
    logger = get_logger()
    columns = get_result_query_columns(query)
    if not query:
        df = DataFrame([], columns=columns)
        df.__model__ = query.model
        return df
    time_started = time.time()
    logger.debug('Querying started %s ...' % query.query)
    list_values = query.values_list(*columns)
    result_dataframe = DataFrame(list(list_values), columns=columns)
    result_dataframe.__model__ = query.model
    querying_time = time.time() - time_started
    logger.debug('Done Querying in %f seconds ' % querying_time)
    return result_dataframe


def to_dataframe(func):
    """
    Annotation that wraps django.db.models.QuerySet reads to a DataFrame
    :param func: function that returns django.db.models.QuerySet
    :return: DataFrame
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> DataFrame:
        result_query = func(*args, **kwargs)
        return query_to_dataframe(result_query)

    return wrapper


def django_dataframe_values(func):
    """
    Annotation that wraps django.db.models.QuerySet reads to a DataFrame
    as values attributes
    :param func: function that returns django.db.models.QuerySet
    :return: DataFrame
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> DataFrame:
        result_query = func(*args, **kwargs)
        logger = get_logger()
        columns = get_result_query_columns(result_query)
        if not result_query:
            return DataFrame([], columns=columns)
        time_started = time.time()
        logger.debug('Querying started %s ...' % result_query.query)
        result_dataframe = DataFrame(list(result_query))
        querying_time = time.time() - time_started
        logger.debug('Done Querying in %f seconds ' % querying_time)
        return result_dataframe

    return wrapper

import time
import logging
from functools import wraps

from django.db.models import QuerySet

from pandas_orm.django.dataframe import DataFrame


def get_result_query_columns(result_query: QuerySet):
    """
    :param result_query: django.db.models.QuerySet
    :return: List[field_name] of the django model
    """
    return [field.name for field in result_query.model._meta.fields]


def django_dataframe(func):
    """
    Annotation that wraps django.db.models.QuerySet reads to a DataFrame
    :param func: function that returns django.db.models.QuerySet
    :return: DataFrame
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> DataFrame:
        result_query = func(*args, **kwargs)
        columns = get_result_query_columns(result_query)
        if not result_query:
            df = DataFrame([], columns=columns)
            df.model = result_query.model
            return df
        time_started = time.time()
        logging.info('Querying started %s ...' % result_query.query)
        list_values = result_query.values_list(*columns)
        result_dataframe = DataFrame(list(list_values), columns=columns)
        result_dataframe.model = result_query.model
        querying_time = time.time() - time_started
        logging.info('Done Querying in %f seconds ' % querying_time)
        return result_dataframe

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
        columns = get_result_query_columns(result_query)
        if not result_query:
            return DataFrame([], columns=columns)
        time_started = time.time()
        logging.info('Querying started %s ...' % result_query.query)
        result_dataframe = DataFrame(list(result_query))
        querying_time = time.time() - time_started
        logging.info('Done Querying in %f seconds ' % querying_time)
        return result_dataframe

    return wrapper

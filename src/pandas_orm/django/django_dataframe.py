import time
import logging
from functools import wraps

from src.pandas_orm.dataframe import BaseDataFrame
from src.pandas_orm.exceptions import DataFrameModelNotSpecified


class DataFrame(BaseDataFrame):

    def bulk_update(self, fields, batch_size=None, model=None):
        model = self.get_model(model=model)
        if not model.objects.__class__.__name__ == 'DataFrameManager':
            raise DataFrameModelNotSpecified()
        if self.empty:
            return self
        return model.objects.bulk_update(self, fields, batch_size)

    def bulk_create(self, *args, model=None, **kwargs):
        model = self.get_model(model=model)
        if not model.objects.__class__.__name__ == 'DataFrameManager':
            raise DataFrameModelNotSpecified()
        if self.empty:
            return self
        return model.objects.bulk_create(self, *args, **kwargs)


def is_model_values(result_query):
    return 'django.db.models.query.QuerySet' not in str(type(result_query))


def get_model_dataframe(result_query):
    if not result_query:
        return DataFrame([], columns=get_result_query_columns(result_query))

    model_values = {key: value for key, value in result_query.__dict__.items()
                    if not key.startswith('_')}
    mode_dataframe = DataFrame([model_values],
                               columns=get_result_query_columns(result_query))
    return mode_dataframe


def get_result_query_columns(result_query):
    return [field.name for field in result_query.model._meta.fields]


def django_dataframe(func):
    """
    Reads the django queryset as a dataframe
    :param func: function that returns Django QuerySet
    :return: DataFrame
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> DataFrame:
        result_query = func(*args, **kwargs)
        # if is_model_values(result_query):
        #     mode_dataframe = get_model_dataframe(result_query)
        #     return mode_dataframe
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
    Reads the django queryset as a dataframe
    :param func: function that returns Django QuerySet
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

import time
import logging
from functools import wraps

from pandas import read_sql, concat
from sqlalchemy.orm import Query

from .exceptions import ToDataFrameNotEmpty
from .execute_sql import DataFrameExecuteSql
from .model_save_arguments import ModelSaveArguments
from .session.sqlalchemy_db import DatabaseSession

from .dataframe import DataFrame, is_dataframe, initialized_dataframe


def to_dataframe_multiple(func):
    """
    Reads the query statements as a dataframe
    :param func: function that returns generator/list sqlalchemy.Session.query
    :return: DataFrame
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        dataframes = []
        for result_query in gen:
            df = base_to_dataframe(result_query)
            dataframes.append(df)
        df_results = concat(dataframes)
        return df_results

    return wrapper


def to_dataframe(func):
    """
    Reads the query statement as a dataframe
    :param query : sqlalchemy.orm.query.Query
    :param func: function that returns sqlalchemy.Session.query
    :return: DataFrame
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        query = func(*args, **kwargs)
        df = base_to_dataframe(query)
        wrapped_df = DataFrame(df)
        if args and args[0].__class__.__name__ == 'ModelManager':
            wrapped_df.model_manager = args[0]
        return wrapped_df

    return wrapper


def base_to_dataframe(query):
    if query is None:
        return DataFrame([])
    if is_dataframe(query):
        if not query.empty:
            raise ToDataFrameNotEmpty(query)
        return query
    assert isinstance(query, Query)
    time_started = time.time()
    logging.debug('Querying started %s ...' % query.statement)
    result_dataframe = read_sql(query.statement,
                                query.session.bind)
    querying_time = time.time() - time_started
    logging.debug('Done Querying in %f seconds ' % querying_time)
    return result_dataframe


class BaseModelDataFrameManager(DatabaseSession):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

    def _bulk_save(self, records, model, unique_fields=None,
                   update_fields=None, returning_id=False):
        records = self._prepare_records(records)
        if records.empty:
            return records
        logging.info(f'Saving {records.shape[0]} {model.__name__} records')
        kwargs = ModelSaveArguments(model=model, records=records,
                                    unique_fields=unique_fields,
                                    update_fields=update_fields).get_args()
        with self.engine() as engine:
            kwargs['engine'] = engine
            new_records = records
            if returning_id:
                results = DataFrameExecuteSql.save_dataframe_to_sql_returning_id(
                    **kwargs)
                new_records = self._add_records_ids(results, records)
            else:
                DataFrameExecuteSql.save_dataframe_to_sql(**kwargs)

            return initialized_dataframe(new_records, self)


    def _add_records_ids(self, results, records):
        new_records = records
        new_ids = results.fetchall()
        if is_dataframe(records):
            df_ids = DataFrame(new_ids, columns=['id'])
            records['id'] = df_ids['id']
            new_records = records.to_dict('records')
        if isinstance(records, list):
            [record.update({'id': new_id[0]}) for record, new_id in
             zip(new_records, new_ids)]
        return new_records

    def _prepare_records(self, records) -> DataFrame:
        if is_dataframe(records):
            return records
        if isinstance(records, list):
            return DataFrame(records)

        raise NotImplementedError(type(records))

import logging

from pandas import DataFrame

from pandas_orm.base.dataframe import is_base_dataframe
from pandas_orm.sqlalchemy.execute_sql import DataFrameExecuteSql
from pandas_orm.sqlalchemy.crud.naive_save_arguments import NativeModelSaveArguments


class ModelDataFrameManager:

    @classmethod
    def bulk_save(cls, dataframe, model, engine_context_func, unique_fields=None,
                   update_fields=None, returning_id=False):
        """
        :param dataframe: DataFrame or collection
        :param model: sqlalchemy.orm.declarative_base
        :param engine_context_func: engine_scope context
        :param unique_fields: List[field..]
        :param update_fields: List[field..]
        :param returning_id: bool
        :return: saved DataFrame
        """
        records = cls._prepare_records(dataframe)
        if records.empty:
            return records
        logging.info(f'Saving {records.shape[0]} {model.__name__} records')
        kwargs = NativeModelSaveArguments(
            records=records,
            model=model,
            unique_fields=unique_fields,
            update_fields=update_fields).get_args()
        with engine_context_func() as engine:
            kwargs['engine'] = engine
            new_records = records
            if returning_id:
                results = DataFrameExecuteSql.save_dataframe_to_sql_returning_id(
                    **kwargs)
                new_records = cls._add_records_ids(results, records)
            else:
                DataFrameExecuteSql.save_dataframe_to_sql(**kwargs)

            return new_records

    @classmethod
    def _add_records_ids(cls, results, records):
        new_ids = results.fetchall()
        df_ids = DataFrame(new_ids, columns=['id'])
        if is_base_dataframe(records):
            records = cls.update_records_ids(df_ids, records)
        if isinstance(records, list):
            records = DataFrame(records)
            records = cls.update_records_ids(df_ids, records)
        return records

    @classmethod
    def update_records_ids(cls, df_ids, records):
        records['id'] = df_ids['id']
        records = records.to_dict('records')
        return records

    @classmethod
    def _prepare_records(cls, records) -> DataFrame:
        if issubclass(records.__class__, DataFrame):
            return records
        if isinstance(records, list):
            return DataFrame(records)

        raise NotImplementedError(type(records))


def bulk_save(dataframe, model, engine_context_func, unique_fields=None,
              update_fields=None, returning_id=False):
    """
    :param dataframe: DataFrame or collection
    :param model: sqlalchemy.orm.declarative_base
    :param engine_context_func: engine_scope context
    :param unique_fields: List[field..]
    :param update_fields: List[field..]
    :param returning_id: bool
    :return: saved DataFrame
    """
    return ModelDataFrameManager.bulk_save(
        dataframe=dataframe,
        model=model,
        engine_context_func=engine_context_func,
        unique_fields=unique_fields,
        update_fields=update_fields,
        returning_id=returning_id,
    )

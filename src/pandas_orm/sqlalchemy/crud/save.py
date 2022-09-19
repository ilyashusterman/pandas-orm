import logging

from pandas import DataFrame

from pandas_orm.sqlalchemy.execute_sql import DataFrameExecuteSql
from pandas_orm.sqlalchemy.crud.naive_save_arguments import NativeModelSaveArguments


class ModelDataFrameManager:

    @classmethod
    def bulk_save(cls, records, model, engine_context_func, unique_fields=None,
                   update_fields=None, returning_id=False):
        """
        :param records: DataFrame or collection
        :param model: sqlalchemy.orm.declarative_base
        :param engine_context_func: engine_scope context
        :param unique_fields: List[field..]
        :param update_fields: List[field..]
        :param returning_id: bool
        :return: saved DataFrame
        """
        records = cls._prepare_records(records)
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
        new_records = records
        new_ids = results.fetchall()
        if issubclass(records.__class__, DataFrame):
            df_ids = DataFrame(new_ids, columns=['id'])
            records['id'] = df_ids['id']
            new_records = records.to_dict('records')
        if isinstance(records, list):
            [record.update({'id': new_id[0]}) for record, new_id in
             zip(new_records, new_ids)]
        return new_records

    @classmethod
    def _prepare_records(cls, records) -> DataFrame:
        if issubclass(records.__class__, DataFrame):
            return records
        if isinstance(records, list):
            return DataFrame(records)

        raise NotImplementedError(type(records))



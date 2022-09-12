import logging

from pandas_orm.sqlalchemy.execute_sql import DataFrameExecuteSql
from pandas_orm.sqlalchemy.model_save_arguments import ModelSaveArguments
from pandas_orm.sqlalchemy.session.sqlalchemy_db import DatabaseSession

from pandas_orm.sqlalchemy.dataframe import DataFrame
from pandas_orm.sqlalchemy.dataframe import is_dataframe
from pandas_orm.sqlalchemy.dataframe import initialized_dataframe


class ModelDataFrameManager(DatabaseSession):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

    def _bulk_save(self, records, model, unique_fields=None,
                   update_fields=None, returning_id=False) -> DataFrame:
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

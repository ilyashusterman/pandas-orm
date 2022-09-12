from pandas import DataFrame as PDDataFrame
from src.pandas_orm.dataframe import BaseDataFrame
from src.pandas_orm.sqlalchemy.exceptions import \
    PandasDBAlchemyModelManagerNotInitialized


def is_dataframe(records):
    return isinstance(records, DataFrame) or isinstance(records, PDDataFrame)


class DataFrame(BaseDataFrame):
    model_manager = None

    def bulk_save(self, unique_fields=None, update_fields=None,
                  returning_id=False):
        if self.model_manager is None:
            raise PandasDBAlchemyModelManagerNotInitialized()
        return self.model_manager.bulk_save(
            self, unique_fields=unique_fields,
            update_fields=update_fields,
            returning_id=returning_id
        )


def initialized_dataframe(records, model_manager):
    if is_dataframe(records):
        df = records
    if isinstance(records, list):
        df = DataFrame(records)
    setattr(df, 'model_manager', model_manager)
    return df

from pandas import DataFrame as PDDataFrame
from pandas_orm.dataframe import BaseDataFrame
from pandas_orm.sqlalchemy.exceptions import \
    PandasDBAlchemyModelManagerNotInitialized


def is_dataframe(records):
    """
    :param records:
    :return: is the records of instance dataframe
    """
    return isinstance(records, DataFrame) or isinstance(records, PDDataFrame)


class DataFrame(BaseDataFrame):
    model_manager = None

    def bulk_save(self, unique_fields=None, update_fields=None,
                  returning_id=False):
        """
        :param unique_fields: unique List[field] of the table
        :param update_fields: update fields List[field] of the table
        :param returning_id: is returning id
        :return: pandas_orm.sqlalchemy.dataframe.DataFrame
        """
        if self.model_manager is None:
            raise PandasDBAlchemyModelManagerNotInitialized()
        return self.model_manager.bulk_save(
            self, unique_fields=unique_fields,
            update_fields=update_fields,
            returning_id=returning_id
        )


def initialized_dataframe(records, model_manager=None) -> DataFrame:
    """
    :param records: collection or DataFrame
    :param model_manager: ModelManager
    :return: pandas_orm.sqlalchemy.dataframe.DataFrame
    """
    if is_dataframe(records):
        df = records
    if isinstance(records, list):
        df = DataFrame(records)
    df = DataFrame(df)
    setattr(df, 'model_manager', model_manager)
    return df

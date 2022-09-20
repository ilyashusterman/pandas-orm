from sqlalchemy.orm import declarative_base

from pandas_orm.base.dataframe import BaseDataFrame, is_base_dataframe
from pandas_orm.base.describe import DescribeDataFrameTable
from pandas_orm.sqlalchemy.crud.save import bulk_save
from pandas_orm.sqlalchemy.exceptions import ModelIsMissing, \
    EngineScopeMissing
from pandas_orm.sqlalchemy.describe.model_describe import ModelDescribe


class DataFrame(BaseDataFrame):

    def __init__(self, *args, orm_model=None, model_manager=None, **kwargs):
        """
        :param args: default pandas.DataFrame args
        :param orm_model: declarative_base
        :param model_manager: pandas_orm.sqlalchemy.model_manager.ModelManager not required
        :param kwargs: default pandas.DataFrame kwargs
        """
        super(__class__, self).__init__(*args, **kwargs)
        self.__model__: declarative_base = orm_model
        self.model_manager = model_manager

    def get_model(self, model=None):
        if model:
            return model
        if self.model_manager:
            return self.model_manager.model
        return self.model

    def bulk_save(self, unique_fields=None, update_fields=None,
                  returning_id=False, engine_context_func=None, model=None):
        """
        :param unique_fields: unique List[field] of the table
        :param update_fields: update fields List[field] of the table
        :param returning_id: is returning id
        :return: pandas_orm.sqlalchemy.dataframe.DataFrame
        """
        model = self.get_model(model)
        if self.model_manager is None:
            if engine_context_func is None:
                raise EngineScopeMissing()
            if model is None:
                raise ModelIsMissing()
            df = bulk_save(
                dataframe=self,
                engine_context_func=engine_context_func,
                model=model,
                unique_fields=unique_fields,
                update_fields=update_fields,
                returning_id=returning_id,
            )
            return initialized_dataframe_model(df, model)
        return self.model_manager.bulk_create(
            self,
            unique_fields=unique_fields,
            update_fields=update_fields,
            returning_id=returning_id
        )

    def to_objects(self, model=None):
        model = model if model else self.model
        return [model(**record) for record in self.to_dict('records')]

    def describe_table(self):
        model = ModelDescribe(self.model)
        columns = model.describe_columns()
        df_cols = DataFrame(columns, orm_model=self.model)
        indexes = model.describe_indexes()
        df_indexes = DataFrame(indexes, orm_model=self.model)
        return DescribeDataFrameTable(
            name=model.name,
            columns=df_cols,
            indexes=df_indexes
        )




def initialized_dataframe(records, model_manager=None) -> DataFrame:
    """
    :param records: collection or DataFrame
    :param model_manager: ModelManager
    :return: pandas_orm.sqlalchemy.dataframe.DataFrame
    """
    if isinstance(records, list):
        records = DataFrame(records, orm_model=model_manager.model, model_manager=model_manager)
    if not is_dataframe(records):
        raise NotImplementedError(type(records))

    df = DataFrame(records, orm_model=model_manager.model, model_manager=model_manager)
    return df


def initialized_dataframe_model(records, model) -> DataFrame:
    """
    :param records: collection or DataFrame
    :param model: ModelManager
    :return: pandas_orm.sqlalchemy.dataframe.DataFrame
    """
    if isinstance(records, list):
        records = DataFrame(records)
    if not is_dataframe(records):
        raise NotImplementedError(type(records))
    df = DataFrame(records, orm_model=model)
    return df


def is_dataframe(records):
    """
    :param records:
    :return: is the records of instance dataframe
    """
    return isinstance(records, DataFrame) or is_base_dataframe(records)

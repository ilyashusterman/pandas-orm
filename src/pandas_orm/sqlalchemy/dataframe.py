from pandas import DataFrame as PDDataFrame
from sqlalchemy.orm import declarative_base

from pandas_orm.base.dataframe import BaseDataFrame
from pandas_orm.sqlalchemy.crud.save import ModelDataFrameManager
from pandas_orm.sqlalchemy.exceptions import ModelIsMissing, \
    EngineScopeMissing


def is_dataframe(records):
    """
    :param records:
    :return: is the records of instance dataframe
    """
    return isinstance(records, DataFrame) or isinstance(records, PDDataFrame)


class DataFrame(BaseDataFrame):
    __model__: declarative_base = None
    model_manager = None

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
            df = ModelDataFrameManager.bulk_save(
                self,
                engine_context_func=engine_context_func,
                model=model,
                unique_fields=unique_fields,
                update_fields=update_fields,
                returning_id=returning_id,
            )
            return initialized_dataframe_model(df, model)
        return self.model_manager.bulk_save(
            self,
            unique_fields=unique_fields,
            update_fields=update_fields,
            returning_id=returning_id
        )

    def to_objects(self, model=None):
        model = model if model else self.model
        return [model(**record) for record in self.to_dict('records')]


def initialized_dataframe(records, model_manager=None) -> DataFrame:
    """
    :param records: collection or DataFrame
    :param model_manager: ModelManager
    :return: pandas_orm.sqlalchemy.dataframe.DataFrame
    """
    if isinstance(records, list):
        records = DataFrame(records)
    if not is_dataframe(records):
        raise NotImplementedError(type(records))
    df = DataFrame(records)
    setattr(df, 'model_manager', model_manager)
    setattr(df, '__model__', model_manager.model)
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
    df = DataFrame(records)
    setattr(df, '__model__', model)
    return df

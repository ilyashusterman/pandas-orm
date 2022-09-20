from django.db.models import Model
from pandas import DataFrame as PDDataFrame
from pandas_orm.base.dataframe import BaseDataFrame
from pandas_orm.base.describe import DescribeDataFrameTable
from pandas_orm.base.exceptions import DataFrameModelNotSpecified
from pandas_orm.django.describe.model_describe import ModelDescribe


class DataFrame(BaseDataFrame):
    __model__: Model = None
    """
        declare
        :param __model__: pandas_orm.django.Model
    """

    def __init__(self, *args, orm_model=None, **kwargs):
        """
        :param args: default pandas.DataFrame args
        :param orm_model: pandas_orm.django.Model or from django.db.models import Model
        :param kwargs: default pandas.DataFrame kwargs
        """
        super(__class__, self).__init__(*args, **kwargs)
        self.__model__: Model = orm_model

    def to_objects(self):
        return [self.model(**record) for record in self.to_dict('records')]

    def bulk_update(self, fields=None, batch_size=None, model=None):
        """
        :param fields: List[str] fields to update for each records in the table
        :param batch_size: integer
        :param model: pandas_orm.django.Model
        :return:
        """
        model = self.validate_dataframe_orm(model)
        if self.empty:
            return self

        return self.model.objects.bulk_update(self, fields, batch_size,
                                              model=model)

    def bulk_create(self, *args, model=None, **kwargs):
        """
        :param args: extended bulk_create args
        :param kwargs: extended bulk_create kwargs
        :param model: pandas_orm.django.Model
        :return:
        """
        model = self.validate_dataframe_orm(model)
        if self.empty:
            return self
        return model.objects.bulk_create(self, *args, **kwargs)

    def validate_dataframe_orm(self, model=None):
        model = model if model else self.model
        if not model.objects.__class__.__name__ == 'DataFrameManager':
            raise DataFrameModelNotSpecified()
        return model

    def describe_table(self) -> DescribeDataFrameTable:
        model = ModelDescribe(self.model)
        columns = model.describe_columns()
        df_columns = DataFrame(columns)
        indexes = model.describe_indexes()
        df_indexes = DataFrame(indexes)
        return DescribeDataFrameTable(
            name=model.name,
            columns=df_columns,
            indexes=df_indexes
        )


def is_dataframe(records):
    """
    :param records:
    :return: is records of instance DataFrame
    """
    return isinstance(records, DataFrame) or isinstance(records, PDDataFrame)

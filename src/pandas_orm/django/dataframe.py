from django.db.models import Model
from pandas import DataFrame as PDDataFrame
from pandas_orm.base.dataframe import BaseDataFrame
from pandas_orm.base.exceptions import DataFrameModelNotSpecified


class DataFrame(BaseDataFrame):
    __model__: Model = None
    """
        declare
        :param __model__: pandas_orm.django.Model
    """

    def to_objects(self):
        return [self.model(**record) for record in self.to_dict('records')]

    def bulk_update(self, fields, batch_size=None, model=None):
        """
        :param fields: List[str] fields to update for each records in the table
        :param batch_size: integer
        :param model: pandas_orm.django.Model
        :return:
        """
        if not self.model.objects.__class__.__name__ == 'DataFrameManager':
            raise DataFrameModelNotSpecified()
        if self.empty:
            return self

        return self.model.objects.bulk_update(self, fields, batch_size, model=model)

    def bulk_create(self, *args, model=None, **kwargs):
        """
        :param args: extended bulk_create args
        :param kwargs: extended bulk_create kwargs
        :param model: pandas_orm.django.Model
        :return:
        """
        model = model if model else self.model
        if not model.objects.__class__.__name__ == 'DataFrameManager':
            raise DataFrameModelNotSpecified()
        if self.empty:
            return self
        return model.objects.bulk_create(self, *args, **kwargs)


def is_dataframe(records):
    """
    :param records:
    :return: is records of instance DataFrame
    """
    return isinstance(records, DataFrame) or isinstance(records, PDDataFrame)
from pandas import DataFrame as PDDataFrame
from pandas_orm.base.dataframe import BaseDataFrame
from pandas_orm.base.exceptions import DataFrameModelNotSpecified


class DataFrame(BaseDataFrame):

    def bulk_update(self, fields, batch_size=None, model=None):
        """
        :param fields: List[str] fields to update for each records in the table
        :param batch_size: integer
        :param model: pandas_orm.django.Model
        :return:
        """
        model = self.get_model(model=model)
        if not model.objects.__class__.__name__ == 'DataFrameManager':
            raise DataFrameModelNotSpecified()
        if self.empty:
            return self

        return model.objects.bulk_update(self, fields, batch_size)

    def bulk_create(self, *args, model=None, **kwargs):
        """
        :param args: extended bulk_create args
        :param kwargs: extended bulk_create kwargs
        :param model: pandas_orm.django.Model
        :return:
        """
        model = self.get_model(model=model)
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
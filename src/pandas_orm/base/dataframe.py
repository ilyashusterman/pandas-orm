from abc import abstractmethod

from pandas import DataFrame as PDDataFrame

from pandas_orm.base.describe import DescribeDataFrameTable
from pandas_orm.base.exceptions import DataFrameModelNotSpecified


class BaseDataFrame(PDDataFrame):

    def __init__(self, *args, orm_model=None, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.__model__ = orm_model

    @property
    def model(self):
        if self.__model__ is None:
            raise DataFrameModelNotSpecified()
        return self.__model__

    @abstractmethod
    def to_objects(self, *args, **kwargs):
        """
        :return: model objects list
        """
        raise NotImplementedError()

    @abstractmethod
    def describe_table(self, *args, **kwargs) -> DescribeDataFrameTable:
        """
        :return: description dataframes for table fields and index, constraints..
        """
        raise NotImplementedError()


def is_base_dataframe(records):
    """
    :param records:
    :return: is the records of instance dataframe
    """
    return isinstance(records, PDDataFrame) or \
           issubclass(records.__class__, BaseDataFrame)

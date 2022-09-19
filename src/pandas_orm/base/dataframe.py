from abc import abstractmethod

from pandas import DataFrame as PDDataFrame

from pandas_orm.base.exceptions import DataFrameModelNotSpecified


class BaseDataFrame(PDDataFrame):
    __model__ = None

    @property
    def model(self):
        if self.__model__ is None:
            raise DataFrameModelNotSpecified()
        return self.__model__

    @abstractmethod
    def to_objects(self, *args, **kwargs):
        raise NotImplementedError()

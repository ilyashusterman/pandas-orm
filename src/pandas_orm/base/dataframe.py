from pandas import DataFrame as PDDataFrame

from pandas_orm.base.exceptions import DataFrameModelNotSpecified


class BaseDataFrame(PDDataFrame):
    model = None

    def get_model(self, model=None):
        model = model if model else self.model
        if model is None:
            raise DataFrameModelNotSpecified()
        return model

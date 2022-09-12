from pandas import DataFrame as PDDataFrame

from src.pandas_orm.exceptions import DataFrameModelNotSpecified


class BaseDataFrame(PDDataFrame):
    model = None

    def get_model(self, model=None):
        model = model if model else self.model
        if model is None:
            raise DataFrameModelNotSpecified()
        return model

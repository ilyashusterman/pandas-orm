class PandasDBError(Exception):
    pass


class DataFrameSaveError(PandasDBError):

    def __init__(self, error=None, msg=None):
        self.error = error
        self.msg = msg
        super(__class__, self).__init__(msg)


class DataFrameModelNotSpecified(PandasDBError):
    pass

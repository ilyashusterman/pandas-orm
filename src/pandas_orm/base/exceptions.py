class PandasORMError(Exception):
    pass


class DataFrameSaveError(PandasORMError):

    def __init__(self, error=None, msg=None):
        self.error = error
        self.msg = msg
        super(__class__, self).__init__(msg)


class DataFrameModelNotSpecified(PandasORMError):
    pass

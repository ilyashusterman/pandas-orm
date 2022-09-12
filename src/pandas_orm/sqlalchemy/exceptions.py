from pandas_orm.base.exceptions import PandasDBError


class PandasDBAlchemyDataBaseError(PandasDBError):
    pass


class PandasDBAlchemySaveModelStatementError(PandasDBAlchemyDataBaseError):
    pass


class PandasDBAlchemyModelManagerNotInitialized(PandasDBAlchemyDataBaseError):
    pass


class PandasDBAlchemyUpdateColumnsNotSupported(PandasDBAlchemyDataBaseError):
    pass


class ToDataFrameNotEmpty(PandasDBAlchemyDataBaseError):
    pass

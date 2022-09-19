from pandas_orm.base.exceptions import PandasORMError


class AlchemyDataBaseError(PandasORMError):
    pass


class AlchemySaveModelStatementError(AlchemyDataBaseError):
    pass


class AlchemyModelManagerNotInitialized(AlchemyDataBaseError):
    pass


class AlchemyUpdateColumnsNotSupported(AlchemyDataBaseError):
    pass


class ToDataFrameNotEmpty(AlchemyDataBaseError):
    pass


class EngineScopeMissing(AlchemyDataBaseError):
    pass


class ModelIsMissing(AlchemyDataBaseError):
    pass

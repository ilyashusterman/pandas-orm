from pandas_orm.django.crud.naive_save_arguments import \
    NativeBulkCreateArguments
from pandas_orm.django.crud.naive_save_arguments import \
    NativeBulkUpdateArguments
from pandas_orm.django.dataframe import is_dataframe
from pandas_orm.django.mixins.dataframe_mixin import DjangoDataFrameMixin


def bulk_create(dataframe, model, func, args, kwargs):
    """
    :param dataframe: List[django.db.models.Model] or DataFrame with similar model as dictionary
    :param model: django.db.models.Model
    :param func: Model.objects.bulk_create or ModelManager func
    :param args: func args
    :param kwargs: func kwargs
    :return: created DataFrame
    """
    if not is_dataframe(dataframe):
        return func(dataframe, *args, **kwargs)
    if dataframe.empty:
        return dataframe

    records = DjangoDataFrameMixin.get_objs(dataframe, model)
    naive_args = NativeBulkCreateArguments(model=model, dataframe=dataframe)
    nargs, nkwargs = naive_args.get_args(*args, **kwargs)
    saved = func(records, *nargs, **nkwargs)
    DjangoDataFrameMixin.add_dataframe_ids(dataframe, saved)
    return dataframe


def bulk_update(dataframe, model, func, args, kwargs):
    """
    :param dataframe: List[django.db.models.Model] or DataFrame with similar model as dictionary
    :param model: django.db.models.Model
    :param func: Model.objects.bulk_update or ModelManager func
    :param args: func args
    :param kwargs: func kwargs
    :return: updated DataFrame
    """
    if not is_dataframe(dataframe):
        return func(dataframe, *args, **kwargs)
    if dataframe.empty:
        return dataframe

    records = DjangoDataFrameMixin.get_objs(dataframe, model)
    naive_args = NativeBulkUpdateArguments(model=model, dataframe=dataframe)
    nargs, nkwargs = naive_args.get_args(*args, **kwargs)
    saved = func(records, *nargs, **nkwargs)
    DjangoDataFrameMixin.add_dataframe_ids(dataframe, saved)
    return dataframe

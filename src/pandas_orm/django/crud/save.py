from pandas_orm.django.crud.naive_save_arguments import \
    NativeBulkCreateArguments
from pandas_orm.django.crud.naive_save_arguments import \
    NativeBulkUpdateArguments
from pandas_orm.django.dataframe import is_dataframe
from pandas_orm.django.mixins.dataframe_mixin import DjangoDataFrameMixin


FACTORY_OPERATE_SAVE_ARGUMENTS = {
    'create': NativeBulkCreateArguments,
    'update': NativeBulkUpdateArguments
}


def bulk_factory_operate(method, dataframe, model, func, args, kwargs):
    """
    :param method: 'update'|'create'
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
    cls_arguments = FACTORY_OPERATE_SAVE_ARGUMENTS[method]
    naive_args = cls_arguments(model=model, dataframe=dataframe)
    nargs, nkwargs = naive_args.get_args(*args, **kwargs)
    saved = func(records, *nargs, **nkwargs)
    DjangoDataFrameMixin.add_dataframe_ids(dataframe, saved)
    return dataframe


def bulk_create(dataframe, model, func, args, kwargs):
    """
    :param dataframe: List[django.db.models.Model] or DataFrame with similar model as dictionary
    :param model: django.db.models.Model
    :param func: Model.objects.bulk_create or ModelManager func
    :param args: Model.objects.bulk_create args
    :param kwargs: Model.objects.bulk_create kwargs
    :return: created DataFrame
    """
    return bulk_factory_operate(
        method='create',
        dataframe=dataframe,
        model=model,
        func=func,
        args=args,
        kwargs=kwargs,
    )


def bulk_update(dataframe, model, func, args, kwargs):
    """
    :param dataframe: List[django.db.models.Model] or DataFrame with similar model as dictionary
    :param model: django.db.models.Model
    :param func: Model.objects.bulk_update or ModelManager func
    :param args: func args
    :param kwargs: func kwargs
    :return: updated DataFrame
    """
    return bulk_factory_operate(
        method='update',
        dataframe=dataframe,
        model=model,
        func=func,
        args=args,
        kwargs=kwargs,
    )


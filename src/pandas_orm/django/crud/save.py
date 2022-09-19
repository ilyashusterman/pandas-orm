from pandas_orm.django.dataframe import is_dataframe
from pandas_orm.django.mixins.dataframe_mixin import DjangoDataFrameMixin


def bulk_save(dataframe, model, func, args, kwargs):
    if not is_dataframe(dataframe):
        return func(dataframe, *args, **kwargs)
    if dataframe.empty:
        return dataframe

    records = DjangoDataFrameMixin.get_objs(dataframe, model)
    saved = func(records, *args, **kwargs)
    DjangoDataFrameMixin.add_dataframe_ids(dataframe, saved)
    return dataframe


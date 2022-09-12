from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from pandas import DataFrame

from src.pandas_orm.django.mixins.dataframe_save import DataFrameSaveMixin

DJANGO_SUPPORTED_FIELDS = '_state'

try:
    from src.pandas_orm.django.django_dataframe import django_dataframe
    from src.pandas_orm.django.django_dataframe import django_dataframe_values


    class DjangoDFQuerySet(QuerySet):

        @django_dataframe
        def to_dataframe(self, *args, **kwargs):
            return self

        @django_dataframe_values
        def to_dataframe_values(self, *args, **kwargs):
            return self


    class DataFrameManager(BaseManager.from_queryset(DjangoDFQuerySet)):

        def bulk_create(self, objs, *args, **kwargs):
            df = objs
            if not isinstance(df, DataFrame):
                return super(__class__, self).bulk_create(*args, **kwargs)
            if df.empty:
                return df
            records = DataFrameSaveMixin.get_objs(df, self.model)
            saved = super(__class__, self).bulk_create(records, *args, **kwargs)
            DataFrameSaveMixin.add_dataframe_ids(df, saved)
            return df

        def bulk_update(self, objs, *args, **kwargs):
            df = objs
            if not isinstance(df, DataFrame):
                return super(__class__, self).bulk_update(objs, *args, **kwargs)
            if df.empty:
                return df
            records = DataFrameSaveMixin.get_objs(df, self.model)
            saved = super(__class__, self).bulk_update(records, *args, **kwargs)
            DataFrameSaveMixin.add_dataframe_ids(df, saved)
            return df


    class DjangoDFModel(models.Model):
        objects = DataFrameManager()

        def to_dict(self):
            return {
                key: value
                for key, value in
                self.__dict__.items()
                if key not in DJANGO_SUPPORTED_FIELDS
            }

        class Meta:
            abstract = True


except ModuleNotFoundError:
    pass

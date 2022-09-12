from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from pandas_orm.django.dataframe import is_dataframe
from pandas_orm.django.mixins.dataframe_save import DataFrameSaveMixin
from pandas_orm.django.django_dataframe import django_dataframe
from pandas_orm.django.django_dataframe import django_dataframe_values

DJANGO_SUPPORTED_FIELDS = '_state'


class DjangoDFQuerySet(QuerySet):
    @django_dataframe
    def to_dataframe(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: DataFrame representation for the queryset
        """
        return self

    @django_dataframe_values
    def to_dataframe_values(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: DataFrame representation for the queryset as values query
        """
        return self


class DataFrameManager(BaseManager.from_queryset(DjangoDFQuerySet)):

    def bulk_create(self, objs, *args, **kwargs):
        """
        bulk_create with DataFrame
        :param objs: List[django.db.models.Model] or DataFrame with similar model as dictionary
        :param args: extended bulk_create args
        :param kwargs: extended bulk_create kwargs
        :return:
        """
        df = objs
        if not is_dataframe(df):
            return super(__class__, self).bulk_create(*args, **kwargs)
        if df.empty:
            return df
        records = DataFrameSaveMixin.get_objs(df, self.model)
        saved = super(__class__, self).bulk_create(records, *args, **kwargs)
        DataFrameSaveMixin.add_dataframe_ids(df, saved)
        return df

    def bulk_update(self, objs, *args, **kwargs):
        """
        bulk_update with DataFrame
        :param objs: List[django.db.models.Model] or DataFrame with similar model as dictionary
        :param args: extended bulk_update args
        :param kwargs: extended bulk_update kwargs
        :return:
        """
        df = objs
        if not is_dataframe(df):
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
        """
        :return: Dict representation
        """
        return {
            key: value
            for key, value in
            self.__dict__.items()
            if key not in DJANGO_SUPPORTED_FIELDS
        }

    class Meta:
        abstract = True

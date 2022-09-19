from typing import List

from pandas import DataFrame

from pandas_orm.django.mixins.base_model_fields_mixin import BaseModelFieldsMixin


class DjangoDataFrameMixin:
    model_mixin = BaseModelFieldsMixin

    @classmethod
    def add_dataframe_ids(cls, df: DataFrame, saved):
        if isinstance(saved, int):
            return df
        ids = [obj.pk for obj in saved]
        df['id'] = ids
        return df

    @classmethod
    def get_objs(cls, df, model):
        report_records = [
            cls.get_object_model(model, **record) for record in df.to_dict('records')
        ]
        return report_records

    @classmethod
    def get_object_model(cls, model, id=None, pk=None, **kwargs):
        obj = model(**kwargs)
        obj.pk = id or pk
        return obj

    @classmethod
    def clean_records_columns(cls, df, model):
        fields = DjangoDataFrameMixin.get_model_fields(model)
        df = cls.fill_missing_columns(df, fields)

        columns = [col for col in df.columns if
                   col in col in fields.keys() and col != 'id']
        df_result = df[columns]
        return df_result

    @classmethod
    def get_model_fields(cls, model):
        return cls.model_mixin.get_model_raw_fields(model)

    @classmethod
    def fill_missing_columns(cls, df, fields: List[str]):
        fields_missing = [
            col for col, field_cls in fields.items()
            if
            col not in df.columns and not cls.is_relation_id_field(field_cls)
        ]
        for missing_field in fields_missing:
            df[missing_field] = None

        return df

    @classmethod
    def is_relation_id_field(cls, field_cls):
        return cls.model_mixin.is_foreign_key(field_cls) or \
               cls.model_mixin.is_reverse_relation_field(field_cls) or \
               field_cls.name == 'id'

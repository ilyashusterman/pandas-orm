from typing import Dict

from django.db.models import ManyToOneRel, ForeignKey
from django.db.models import OneToOneRel
from django.db.models import ManyToManyRel
from django.db.models import ForeignObjectRel

REVERSE_RELATIONS = [ManyToOneRel, OneToOneRel, ManyToManyRel, ForeignObjectRel]


class BaseModelFieldsMixin:

    @classmethod
    def get_model_fields(cls, model) -> Dict:
        return {field.name: field for field in model._meta.get_fields() if not cls.is_reverse_relation_field(field)}

    @classmethod
    def is_reverse_relation_field(cls, field):
        for rel_relation in REVERSE_RELATIONS:
            if isinstance(field, rel_relation):
                return True
        return False

    @classmethod
    def get_model_raw_fields(cls, model):
        fields = cls.get_model_fields(model)
        return {
            cls.get_raw_field(field): field for field in fields.values()
        }

    @classmethod
    def get_raw_field(cls, field):
        if cls.is_foreign_key(field):
            return f'{field.name}_id'

        return field.name

    @classmethod
    def is_foreign_key(cls, cls_field):
        return isinstance(cls_field, ForeignKey)

    @classmethod
    def get_non_id_fields(cls, model):
        fields = [
            field for field
            in cls.get_model_fields(model).keys()
            if 'id' != field
        ]
        return fields

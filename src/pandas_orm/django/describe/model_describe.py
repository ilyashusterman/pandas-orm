from django.db.models import Field, NOT_PROVIDED


class ModelDescribe:

    def __init__(self, model):
        self.model = model

    @property
    def name(self):
        return self.model._meta.model_name

    def get_constraints(self):
        return self.model._meta.constraints

    def get_columns(self):
        return self.model._meta.fields

    def describe_columns(self):
        return [
            self.describe_column(col) for col in self.get_columns()
        ]

    def describe_column(self, col: Field):
        """
        :param col: Field
        :return:
        """
        col_kwargs = {
            'Column': col.name,
            'Type': f'{type(col).__name__} {col.description % col.__dict__}',
            'Collation': None,
            'Nullable': None if col.null else 'not null',
            'Default': None if col.default is NOT_PROVIDED else col.default,
        }
        if col.primary_key:
            update_kwargs = self.get_primary_key_kwargs(col)
            col_kwargs.update(update_kwargs)
        return col_kwargs

    def get_primary_key_kwargs(self, col):
        return {
            'Default': 'Auto Increment'
        }

    def describe_indexes(self):
        indexes = self.model._meta.indexes
        constraints = self.get_constraints()
        pk_fields = [col for col in self.get_columns() if col.primary_key]

        return [
            self.describe_index(index_col) for index_col in indexes+constraints+pk_fields
        ]

    def describe_index(self, index_col):
        fields = index_col.name if hasattr(index_col, 'primary_key') else index_col.fields
        return {
            'Name': index_col.name,
            'Type': type(index_col).__name__,
            'Fields': fields,
        }
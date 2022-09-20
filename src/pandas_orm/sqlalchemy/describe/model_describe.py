from sqlalchemy import UniqueConstraint, Index, PrimaryKeyConstraint, Column, \
    Constraint


class ModelDescribe:

    def __init__(self, model):
        self.model = model

    @property
    def name(self):
        return self.model.__table__.name

    def get_columns(self):
        return self.model.__table__.columns

    def get_unique_constraints(self):
        constraints = [value for value in self.model.__dict__.values() if
                       isinstance(value, UniqueConstraint)]
        return constraints

    def get_indexes(self):
        return [item for item in self.model.__dict__.values() if
                isinstance(item, Index)]

    def get_pks(self):
        pks=  [item for item in self.model.__dict__.values() if
                isinstance(item, PrimaryKeyConstraint)]
        if not pks:
            return [col for col in self.get_columns() if col.primary_key]

    def describe_column(self, column: Column):
        kwargs_update = None
        if column.primary_key:
            kwargs_update = self.describe_primary(column)
        describe = {
            'Column': column.name,
            'Type': str(column.type),
            'Unique': 'Unique' if column.unique else None,
            'Collation': None,
            'Nullable': None if column.nullable else 'not null',
            'Default': column.default
        }
        if kwargs_update:
            describe.update(kwargs_update)
        return describe

    def describe_primary(self, column):
        return {
            'Default': f'{column.autoincrement} increment',
        }

    def describe_columns(self):
        return [
            self.describe_column(col) for col in self.get_columns()
        ]

    def describe_indexes(self):
        constraints = self.describe_constraints()
        indexes = self.get_indexes()
        primary_keys = self.get_pks()
        return [
            {
                'Name': col.name,
                'Type': self.get_index_column_type(col),
                'Fields': self.get_index_describe_fields(col),
            } for col in constraints + indexes + primary_keys
        ]

    def get_index_column_type(self, col):
        if hasattr(col, 'primary_key'):
            return PrimaryKeyConstraint.__name__
        return type(col).__name__

    def get_index_describe_fields(self, col):
        if hasattr(col, '_pending_colargs'):
            return col._pending_colargs
        return col.name

    def describe_constraints(self):
        return [item for item in self.model.__dict__.values() if
                issubclass(item.__class__, Constraint)]

from django.db.models import Model

from pandas_orm.django.describe.model_describe import ModelDescribe


class NaiveModelBulkArguments:
    def __init__(self, model: Model, dataframe):
        self.model = ModelDescribe(model)
        self.records = dataframe

    def get_update_fields(self, fields=None):
        if fields:
            return fields
        """
        update_fields=['last_name'], unique_fields=['name', 'email']
        """
        columns = []
        for column in self.model.get_columns():
            if column.primary_key:
                continue
            if column.unique:
                continue
            columns.append(column.name)
        return columns


class NativeBulkCreateArguments(NaiveModelBulkArguments):

    def get_args(self,
                 batch_size=None,
                 ignore_conflicts=None,
                 update_conflicts=None,
                 update_fields=None,
                 unique_fields=None, *args, **kwargs
                 ):
        naive_ignore_conflicts = self.get_ignore_conflicts(ignore_conflicts)
        naive_update_conflicts = self.get_update_conflicts(update_conflicts)
        naive_update_fields = self.get_update_fields(update_fields)
        naive_unique_fields = self.get_unique_fields(unique_fields)
        naive_kwargs = dict(
            ignore_conflicts=naive_ignore_conflicts,
            update_conflicts=naive_update_conflicts,
            update_fields=naive_update_fields,
            unique_fields=naive_unique_fields,
            batch_size=batch_size,
        )
        return (), {**naive_kwargs, **kwargs}

    def get_unique_fields(self, fields):
        if fields:
            return fields
        constraints = self.model.get_constraints()
        if constraints:
            return constraints[0].fields

        return []

    def get_update_conflicts(self, is_conflict):
        if is_conflict is not None:
            return is_conflict

        return True

    def get_ignore_conflicts(self, is_conflict):
        if is_conflict is not None:
            return is_conflict

        return False


class NativeBulkUpdateArguments(NaiveModelBulkArguments):

    def get_args(self, fields=None, batch_size=None):
        naive_fields = self.get_fields(fields)
        naive_kwargs = dict(
            fields=naive_fields,
            batch_size=batch_size,
        )
        return (), naive_kwargs

    def get_fields(self, fields):
        return self.get_update_fields(fields)

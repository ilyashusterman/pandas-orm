from typing import List

from pandas_orm.sqlalchemy.describe.model_describe import ModelDescribe


class NativeModelSaveArguments:

    def __init__(self, records, model, unique_fields=None, update_fields=None):
        self.model = ModelDescribe(model)
        self.records = records
        self.unique_fields = unique_fields
        self.update_fields = update_fields

    def get_args(self) -> dict:
        constraints = self.model.get_unique_constraints()
        constraints_names = self.get_constraints_names(constraints)
        constraint = constraints_names[0] if constraints_names else None
        constraints_values = self.get_constraint_fields(constraints)
        update_columns = self.get_update_fields(constraints_values)
        kwargs = dict(
            dataframe=self.records,
            model=self.model.model,
            update_column=update_columns,
            constraint=constraint)
        return kwargs

    def get_constraint_fields(self, constraints=None):
        if self.unique_fields:
            return self.update_fields
        return [col for con in constraints for col in
                con._pending_colargs]

    def get_constraints_names(self, constraints):
        return [value.name for value in constraints]

    def get_update_fields(self, unique_columns: List[str]):
        columns = []
        if self.update_fields:
            return self.update_fields
        for column in self.model.get_columns():
            if column.primary_key:
                continue
            if column.unique:
                continue
            if column.name in unique_columns:
                continue
            columns.append(column.name)

        return columns

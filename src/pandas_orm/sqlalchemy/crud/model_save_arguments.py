from typing import List
from sqlalchemy import UniqueConstraint


class ModelSaveArguments:

    def __init__(self, model, records, unique_fields=None, update_fields=None):
        self.model = model
        self.records = records
        self.unique_fields = unique_fields
        self.update_fields = update_fields

    def get_args(self) -> dict:
        constraints = self.get_unique_constraints()
        constraints_names = self.get_constraints_names(constraints)
        constraint = constraints_names[0] if constraints_names else None
        constraints_values = self.get_constrain_fields(constraints)
        update_columns = self.get_update_fields(constraints_values)
        kwargs = dict(
            dataframe=self.records,
            model=self.model,
            update_column=update_columns,
            constraint=constraint)
        return kwargs

    def get_constrain_fields(self, constraints=None):
        if self.unique_fields:
            return self.update_fields
        return [col for con in constraints for col in
                con._pending_colargs]

    def get_constraints_names(self, constraints):
        return [value.name for value in constraints]

    def get_unique_constraints(self):
        constraints = [value for value in self.model.__dict__.values() if
                       isinstance(value, UniqueConstraint)]
        return constraints

    def get_implementation_columns(self, models, exclude_columns):
        columns = []
        for table in models:
            columns += [
                col for col in table.__table__.columns if
                col.name not in exclude_columns
            ]
        return columns

    def get_update_fields(self, unique_columns: List[str]):
        columns = []
        if self.update_fields:
            return self.update_fields
        for column in self.model.__table__.columns:
            if column.primary_key:
                continue
            if column.unique:
                continue
            if column.name in unique_columns:
                continue
            columns.append(column.name)

        return columns

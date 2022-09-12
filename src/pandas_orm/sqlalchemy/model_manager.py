from .base_model_manager import to_dataframe, BaseModelDataFrameManager


class ModelManager(BaseModelDataFrameManager):

    def __init__(self, model, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.model = model

    @to_dataframe
    def all(self):
        with self.session() as session:
            return session.query(self.model)

    @to_dataframe
    def get(self, **kwargs):
        with self.session() as session:
            prepared_statement = session.query(self.model)
            for key, value in kwargs.items():
                prepared_statement = prepared_statement.filter(
                    getattr(self.model, key) == value
                )
            return prepared_statement

    def bulk_save(self, records, unique_fields=None, update_fields=None, returning_id=False):
        return self._bulk_save(
            records=records,
            model=self.model,
            unique_fields=unique_fields,
            update_fields=update_fields,
            returning_id=returning_id
        )







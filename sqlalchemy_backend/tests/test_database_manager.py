import logging
import unittest

from pandas_orm.sqlalchemy.dataframe import DataFrame
from pandas_orm.sqlalchemy.model_manager import ModelManager
from sqlalchemy_backend.config import DB_URL
from sqlalchemy_backend.models.collaborator import Collaborator


class TestDataBase(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.db = ModelManager(model=Collaborator, url=DB_URL)

    def test_all(self):
        df = self.db.all()
        self.assertIsInstance(df, DataFrame)

    def test_bulk_save(self):
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name="bulk_create_sqlalchemy"
        )])
        saved = self.db.bulk_save(df_new)
        df = self.db.all()
        self.assertEqual(saved['last_name'].iloc[0], df_new['last_name'].iloc[0])
        self.assertEqual(saved['last_name'].iloc[0], df['last_name'].iloc[0])
        df_new['last_name'] = 'bulk_create_sqlalchemy'

    def test_bulk_save_returning_id(self):
        df_before = self.db.all()
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name="bulk_create_sqlalchemy_returning_id"
        )])
        saved = self.db.bulk_save(df_new, returning_id=True)
        df = self.db.all()
        self.assertEqual(saved['last_name'].iloc[0], df_new['last_name'].iloc[0])
        self.assertEqual(saved['last_name'].iloc[0], df['last_name'].iloc[0])
        self.assertNotEqual(saved['id'].iloc[0], None)
        self.assertNotEqual(saved['id'].iloc[0], df_before['last_name'].iloc[0])

    def test_get(self):
        email = "test@test.test"
        entity = self.db.get(email=email)
        self.assertEqual(entity['email'].iloc[0], email)

    def test_to_objects(self):
        entities = self.db.all()
        objects = entities.to_objects()
        self.assertIsInstance(objects[0], Collaborator)
        self.assertEqual(objects[0].id, 1)

    def test_dataframe_bulk_save(self):
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name="test_dataframe_bulk_save"
        )])
        saved_df = df_new.bulk_save(
            model=Collaborator,
            engine_context_func=self.db.engine,
            returning_id=True
        )
        objects = saved_df.to_objects()
        self.assertEqual(objects[0].id, 1)


if __name__ == '__main__':
    unittest.main()

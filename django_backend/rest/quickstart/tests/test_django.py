import logging
import unittest

from pandas_orm.django.query import DataFrame

import rest.quickstart.models as models


class TestDjangoModelManager(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(level=logging.DEBUG)

    def test_user_query_dataframe(self):
        users = models.User.objects.all()
        df = users.to_dataframe()
        self.assertIsInstance(df, DataFrame)

    def test_collaborator_query_dataframe(self):
        collaborators = models.Collaborator.objects.all()
        df = collaborators.to_dataframe()
        self.assertIsInstance(df, DataFrame)

    def test_collaborator_bulk_create(self):
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name="bulk_create"
        )], orm_model=models.Collaborator)
        models.Collaborator.objects.bulk_create(df_new, update_conflicts=True, update_fields=['last_name'], unique_fields=['name', 'email'])

    def test_collaborator_bulk_create_with_conflict(self):
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name="create_with_conflict"
        )])
        models.Collaborator.objects.bulk_create(df_new, update_conflicts=True, update_fields=['last_name'], unique_fields=['name', 'email'])

    def test_collaborator_bulk_update(self):
        df_new = DataFrame([dict(
            pk=1,
            name="test",
            email="test@test.test",
            last_name='bulk_update'
        )])
        models.Collaborator.objects.bulk_update(df_new, fields=['last_name'])

    def test_collaborator_bulk_update_dataframe(self):
        collaborators = models.Collaborator.objects.all()
        df = collaborators.to_dataframe()
        self.assertIsInstance(df, DataFrame)
        df['last_name'] = 'update_dataframe'
        df.bulk_update(fields=['last_name'])

    def test_dataframe_to_objects(self):
        collaborators = models.Collaborator.objects.all()
        df = collaborators.to_dataframe()
        objects = df.to_objects()
        self.assertIsInstance(objects[0], models.Collaborator)
        self.assertEqual(objects[0].pk, 1)

    def test_collaborator_bulk_create_with_specified_model(self):
        last_name = "collaborator_bulk_create_with_specified_model"
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name=last_name
        )], orm_model=models.Collaborator)
        saved = df_new.bulk_create(update_conflicts=True, update_fields=['last_name'], unique_fields=['name', 'email'])
        self.assertEqual(saved.iloc[0]['last_name'], last_name)

    def test_collaborator_bulk_create_with_no_arguments_native(self):
        last_name = "collaborator_bulk_create_with_specified_model_naive_2"
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name=last_name
        )], orm_model=models.Collaborator)
        saved = df_new.bulk_create()
        self.assertEqual(saved.iloc[0]['last_name'], last_name)
        objs = models.Collaborator.objects.all()
        df = objs.to_dataframe()
        self.assertEqual(df.iloc[0]['last_name'], last_name)

    def test_collaborator_bulk_update_with_no_arguments_native(self):
        last_name = "collaborator_bulk_update_with_specified_model_naive_4"
        objs = models.Collaborator.objects.all()
        df_update = objs.to_dataframe()
        df_update['last_name'] = last_name
        saved = df_update.bulk_update()
        self.assertEqual(saved.iloc[0]['last_name'], last_name)
        objs = models.Collaborator.objects.all()
        df = objs.to_dataframe()
        self.assertEqual(df.iloc[0]['last_name'], last_name)

    def test_describe_table(self):
        objs = models.Collaborator.objects.all()
        df = objs.to_dataframe()
        describe = df.describe_table()
        print(describe)


if __name__ == '__main__':
    unittest.main()

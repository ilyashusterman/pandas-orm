import unittest

from pandas_orm.django.query import DataFrame

import models as test_models


class TestAdminUser(unittest.TestCase):

    def test_user_query_dataframe(self):
        users = test_models.User.objects.all()
        df = users.to_dataframe()
        self.assertIsInstance(df, DataFrame)

    def test_collaborator_query_dataframe(self):
        collaborators = test_models.Collaborator.objects.all()
        df = collaborators.to_dataframe()
        self.assertIsInstance(df, DataFrame)

    def test_collaborator_bulk_create(self):
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name="bulk_create"
        )])
        test_models.Collaborator.objects.bulk_create(df_new,
                                                     update_conflicts=True,
                                                     update_fields=[
                                                         'last_name'],
                                                     unique_fields=['name',
                                                                    'email'])

    def test_collaborator_bulk_create_with_conflict(self):
        df_new = DataFrame([dict(
            name="test",
            email="test@test.test",
            last_name="create_with_conflict"
        )])
        test_models.Collaborator.objects.bulk_create(df_new,
                                                     update_conflicts=True,
                                                     update_fields=[
                                                         'last_name'],
                                                     unique_fields=['name',
                                                                    'email'])

    def test_collaborator_bulk_update(self):
        df_new = DataFrame([dict(
            pk=1,
            name="test",
            email="test@test.test",
            last_name='bulk_update'
        )])
        test_models.Collaborator.objects.bulk_update(df_new,
                                                     fields=['last_name'])

    def test_collaborator_bulk_update_dataframe(self):
        collaborators = test_models.Collaborator.objects.all()
        df = collaborators.to_dataframe()
        self.assertIsInstance(df, DataFrame)
        df['last_name'] = 'update_dataframe'
        df.bulk_update(fields=['last_name'])


if __name__ == '__main__':
    unittest.main()

from django.contrib.auth.models import User as DJUser

from pandas_orm.django.model import DataFrameManager


class User(DJUser):
    objects = DataFrameManager()
    class Meta:
        app_label = 'rest.quickstart'
        proxy = True
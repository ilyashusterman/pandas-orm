from django.db import models
from pandas_orm.django.db import Model


class Collaborator(Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_link = models.CharField(max_length=250, null=True)
    image_url = models.CharField(max_length=250, null=True)

    class Meta:
        db_table = 'collaborator'
        app_label = 'rest.quickstart'
        constraints = [
            models.UniqueConstraint(fields=['name', 'email'], name='collaborator_unique_key'),
        ]
        indexes = [
            models.Index(fields=['name', 'first_name', 'last_name'], name='collaborator_name_search_idx')
        ]

    def __str__(self):
        return f'<<< Collaborator {self.name} >>> {self.email}'

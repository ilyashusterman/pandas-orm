Django usage
============

Django Package Interfaces
-----------------------------

.. autofunction:: pandas_orm.django.query.query_to_dataframe

you can use the ``from pandas_orm.django.db import Model`` class:

.. autoclass:: pandas_orm.django.db::Model
   :members:
   :inherited-members:

.. code-block:: console

    from django.db import models
    from pandas_orm.django.db import Model


    class Collaborator(Model):
        name = models.CharField(max_length=200)
        first_name = models.CharField(max_length=200, null=True)
        last_name = models.CharField(max_length=200, null=True)
        email = models.CharField(max_length=200)
        profile_link = models.CharField(max_length=250, null=True)
        image_url = models.CharField(max_length=250, null=True)

    collaborators = test_models.Collaborator.objects.all()
    df = collaborators.to_dataframe()





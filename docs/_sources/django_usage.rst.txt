Django usage
============

Django Package Interfaces
-------------------------

.. autofunction:: pandas_orm.django.query.query_to_dataframe
.. code-block:: console

    from pandas_orm.django.query import query_to_dataframe

    @to_dataframe
    def get_queryset()
        return Collaborator.objects.all()

    df = get_queryset()


.. autofunction:: pandas_orm.django.query.to_dataframe
.. code-block:: console

    from pandas_orm.django.query import to_dataframe
    df = query_to_dataframe(Collaborator.objects.all())


Django Package Models
---------------------

you can use the ``from pandas_orm.django.db import Model`` class:

.. autoclass:: pandas_orm.django.db::Model
   :members:

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
    df['last_name'] = 'test'
    test_models.Collaborator.bulk_update(df, fields=['last_name'])
    # or naive way
    test_models.Collaborator.bulk_update(df)

Django Package DataFrame & QuerySet
------------------------------------

you can use the ``from pandas_orm.django.dataframe import DataFrame`` class:

.. autoclass:: pandas_orm.django.dataframe::DataFrame
   :members:


.. code-block:: console

    from pandas_orm.django.dataframe import DataFrame

    last_name = "collaborator_bulk_create_with_specified_model_naive"
    df_new = DataFrame([dict(
        name="myname",
        email="test@test.test",
        last_name=last_name
    )], orm_model=models.Collaborator)
    ###################
    ### bulk_create ###
    ###################
    created = df_new.bulk_create()

    objs = models.Collaborator.objects.all()
    df_update = objs.to_dataframe()
    df_update['last_name'] = last_name
    ###################
    ### bulk_update ###
    ###################
    updated = df_update.bulk_update()

Django Package bulk operations
------------------------------

.. autofunction:: pandas_orm.django.crud.save.bulk_create

.. autofunction:: pandas_orm.django.crud.save.bulk_update
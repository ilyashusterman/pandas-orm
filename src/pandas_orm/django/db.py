from django.db import models as django_models

from pandas_orm.django.model import DjangoDFModel as Model
from pandas_orm.django.model import DataFrameManager

models = django_models
models.Model = Model
models.manager.BaseManager = DataFrameManager
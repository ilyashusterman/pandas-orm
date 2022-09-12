from django.db import models as django_models

from .model import DjangoDFModel, DataFrameManager

models = django_models
models.Model = DjangoDFModel
models.manager.BaseManager = DataFrameManager

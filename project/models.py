from django.db import models

from organization.models import Organization


# Create your models here.
class Project(models.Model):
    """プロジェクトのモデル"""
    name = models.CharField(max_length=256, verbose_name='プロジェクト名')
    detail = models.CharField(max_length=1000, verbose_name='詳細')

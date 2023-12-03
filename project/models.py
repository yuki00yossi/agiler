from django.db import models

from organization.models import Organization


# Create your models here.
class Project(models.Model):
    """プロジェクトのモデル"""
    name = models.CharField(max_length=256, verbose_name='プロジェクト名')
    detail = models.CharField(max_length=1000, verbose_name='プロジェクト詳細')
    organization = models.ForeignKey(
        Organization,
        verbose_name='組織',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    REQUIRE_FIELDS = [
        'name', 'detail', 'organization',
    ]

    class Meta:
        db_table_comment='プロジェクトテーブル'
        verbose_name = 'プロジェクト'
        verbose_name_plural = 'プロジェクト'

    def __str__(self):
        return self.name

from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Organization(models.Model):
    """ 組織クラス """
    plan_choices = (
        (1, '無料プラン'),
        (2, 'スタンダード'),
        (3, 'エンタープライズ')
    )

    status_choices = (
        (1, 'アクティブ'),
        (2, '非アクティブ'),
        (99, '利用停止'),
    )
    name = models.CharField(verbose_name='組織名', max_length=256)
    post_code = models.CharField(verbose_name='郵便番号', max_length=20)
    prefecture = models.CharField(verbose_name='都道府県', max_length=256)
    city = models.CharField(verbose_name='市区町村', max_length=56)
    address = models.CharField(verbose_name='住所(市区町村以下)', max_length=256)
    tel_number = models.CharField(verbose_name='代表電話番号', max_length=20)
    manager_name = models.CharField(verbose_name='担当者名', max_length=256)
    plans = models.IntegerField(verbose_name='利用プランID', choices=plan_choices)
    status = models.IntegerField(
        verbose_name='ステータス', default=2, choices=status_choices
    )
    members = models.ManyToManyField(
        get_user_model(),
        through='OrganizationUser',
        through_fields=('organization', 'user')
    )
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    REQUIRED_FIELDS = [
        'name', 'post_code', 'prefecture',
        'city', 'address', 'tel_number', 'manager_name',
    ]

    class Meta:
        db_table_comment = '組織テーブル'
        verbose_name = '組織'
        verbose_name_plural = '組織'

    def __str__(self):
        return self.name


class OrganizationUser(models.Model):
    """ 組織とユーザーの中間テーブル """
    # メンバーステータスの選択肢
    status_choices = (
        (1, 'active'),
        (2, '招待中（参加待ち）'),
        (99, '停止'),
    )

    organization = models.ForeignKey(
        Organization,
        verbose_name='所属組織',
        on_delete=models.CASCADE,
        db_comment='所属組織のID'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )
    invited_at = models.DateTimeField(verbose_name='招待日', auto_now_add=True)
    joined_at = models.DateTimeField(verbose_name='参加日', null=True)
    status = models.IntegerField(verbose_name='ステータス', choices=status_choices)

    class Meta:
        db_table = 'organization_users'
        db_table_comment = '組織とユーザーの中間テーブル'
        verbose_name = 'メンバー'
        verbose_name_plural = 'メンバー'
        ordering = ('-organization', 'status')

    def __str__(self):
        return self.organization.name + ': ' + self.user.get_username()

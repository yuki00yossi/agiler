# Generated by Django 4.2.5 on 2023-10-29 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invited_at', models.DateTimeField(auto_now_add=True, verbose_name='招待日')),
                ('joined_at', models.DateTimeField(null=True, verbose_name='参加日')),
                ('status', models.IntegerField(choices=[(1, 'active'), (2, '招待中（参加待ち）'), (3, '停止')], verbose_name='ステータス')),
            ],
            options={
                'db_table_comment': '組織とユーザーの中間テーブル',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='組織名')),
                ('post_code', models.CharField(max_length=20, verbose_name='郵便番号')),
                ('prefecture', models.CharField(max_length=256, verbose_name='都道府県')),
                ('city', models.CharField(max_length=56, verbose_name='市区町村')),
                ('address', models.CharField(max_length=256, verbose_name='住所(市区町村以下)')),
                ('tel_number', models.CharField(max_length=20, verbose_name='代表電話番号')),
                ('manager_name', models.CharField(max_length=256, verbose_name='担当者名')),
                ('plans', models.IntegerField(verbose_name='利用プランID')),
                ('status', models.IntegerField(default=1, verbose_name='ステータス')),
                ('members', models.ManyToManyField(through='organization.Member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='organization',
            field=models.ForeignKey(db_comment='所属組織のID', on_delete=django.db.models.deletion.CASCADE, to='organization.organization', verbose_name='所属組織'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
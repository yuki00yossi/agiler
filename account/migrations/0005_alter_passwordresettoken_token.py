# Generated by Django 4.2.5 on 2023-11-23 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_passwordresettoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='token',
            field=models.CharField(default='3Sew-7eJa9nX3v1eUlDQ5TNQ4ayLhZOLYEuMr6Ok_tY', max_length=256, verbose_name='パスワードリセットトークン'),
        ),
    ]
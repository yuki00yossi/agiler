# Generated by Django 4.2.5 on 2023-11-22 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_passwordresettoken_is_used_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='token',
            field=models.CharField(default='VPnR8G5Upkhi0qvL-L2-u1uDabT139OjvESGT_rM8yY', max_length=256, verbose_name='パスワードリセットトークン'),
        ),
    ]
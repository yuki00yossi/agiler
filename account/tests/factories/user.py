from datetime import datetime, timedelta

from factory import Faker, PostGenerationMethodCall, Sequence
from factory.django import DjangoModelFactory, Password

from django.contrib.auth import get_user_model

Faker._DEFAULT_LOCALE = 'ja_JP'


class UserFactory(DjangoModelFactory):
    """ ユーザーのテスト用ダミーデータ """
    class Meta:
        model = get_user_model()

    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    profile_text = Faker('text')
    password = Password('password')
    is_staff = False
    is_active = True
    is_superuser = False

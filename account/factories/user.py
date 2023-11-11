import factory
from factory import Faker
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

    @classmethod
    def seed_user(cls, user_num=50, staff_num=10, super_num=5):
        """ユーザーのダミーデータを挿入する

        Args:
            user_num (int, optional): 追加する通常ユーザー数 Defaults to 100.
            staff_num (int, optional): 追加するスタッフ権限ユーザー数. Defaults to 10.
            super_num (int, optional): 追加するスーパーユーザー数. Defaults to 5.
        """
        # 通常ユーザーを作成
        cls.create_batch(
            user_num,
            email=factory.Sequence(lambda n: 'user{0}@example.com'.format(n)),
        )
        # スタッフユーザーを作成
        cls.create_batch(
            staff_num,
            email=factory.Sequence(lambda n: 'staff{0}@example.com'.format(n)),
            is_staff=True
        )
        # スーパーユーザーを作成
        cls.create_batch(
            super_num,
            email=factory.Sequence(lambda n: 'super{0}@example.com'.format(n)),
            is_staff=True,
            is_superuser=True
        )

from factory import Faker
from factory.django import DjangoModelFactory

from account.models import User
from organization.models import Organization

import random


Faker._DEFAULT_LOCALE = 'ja_JP'


class OrganizationFactory(DjangoModelFactory):
    """ ユーザーのテスト用ダミーデータ """
    class Meta:
        model = Organization

    name = Faker('company')
    post_code = Faker('postcode')
    prefecture = Faker('prefecture')
    city = Faker('city')
    address = Faker('town')
    tel_number = Faker('phone_number')
    manager_name = Faker('name')
    plans = random.choice(Organization.plan_choices)[0]
    status = random.choice(Organization.status_choices)[0]
    created_at = Faker('date_time')
    updated_at = Faker('date_time')

    @classmethod
    def seed_organization(cls, insert_num=10):
        """組織のダミーデータを挿入する

        Args:
            insert_num (int, optional): 挿入するレコード数. Defaults to 10.
        """
        cls.create_batch(insert_num,  status=1)

    @classmethod
    def seed_organization_member(cls):
        """組織にメンバーをランダムに追加する"""

        users = User.objects.filter(is_staff=False)
        if not users:
            raise Exception('組織に追加する為のユーザーが見つかりません。')

        organizations = Organization.objects.filter(status=1)
        if not organizations:
            raise Exception('組織のレコードが見つかりません。')
        if len(users) < len(organizations):
            raise Exception('ユーザー数が組織数より少ないため実行できません。')

        remainder = len(users) % len(organizations)
        avg_user = len(users) // len(organizations)

        itr_ctr = 0
        for organization in organizations:
            # ユーザー数が組織数で綺麗に割り切れない場合は最初の組織に余ったユーザーを追加する
            add_user_num = avg_user + remainder if itr_ctr == 0 else avg_user

            for i in range(add_user_num):
                organization.members.add(
                    users[itr_ctr],
                    through_defaults={'status': True}
                )
                itr_ctr += 1

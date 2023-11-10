from factory import Faker
from factory.django import DjangoModelFactory

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
    status = random.choice(Organization.status_coices)[0]
    created_at = Faker('date_time')
    updated_at = Faker('date_time')

from datetime import datetime, timedelta

from factory import Faker, PostGenerationMethodCall, Sequence
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model


# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = get_user_model()

#     email = Faker('email')
#     first_name = models.CharField(_('first name'), max_length=64)
#     last_name = models.CharField(_('last_name'), max_length=64)
#     profile_text = models.CharField(
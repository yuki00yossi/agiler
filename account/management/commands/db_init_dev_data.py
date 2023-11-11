
import factory

from django.core.management.base import BaseCommand

from account.models import User, UserActivationToken
from organization.models import Organization, OrganizationUser
from account.factories.user import UserFactory
from organization.factories.organization import OrganizationFactory


class Command(BaseCommand):
    help = '開発環境用のテストデータを作成する'

    def handle(self, *args, **options):
        # まずはスーパーユーザーを作成
        UserFactory.seed_user()
        OrganizationFactory.seed_organization()
        OrganizationFactory.seed_organization_member()

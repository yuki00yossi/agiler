from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from account.factories.user import UserFactory
from organization.models import Organization


User = get_user_model()


class AddOrganizationTest(TestCase):
    """組織追加APIのシナリオテスト"""
    def setUp(self) -> None:
        # テスト用ユーザー
        self.user = UserFactory()
        self.post_data = {
            'name': 'テスト組織',
            'post_code': 1111111,
            'prefecture': '東京都',
            'city': '港区',
            'address': '1-1-1',
            'tel_number': '01234567890',
            'manager_name': self.user.get_full_name(),
            'plans': 1,
            'status': 1,
        }
        self.client = APIClient()

    def test_can_add_org_with_auth(self):
        """認証済ユーザーが新規組織作成が可能なこと"""
        # まずは組織テーブルが空であること
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # ログインして組織作成APIを叩く
        self.client.force_authenticate(user=self.user)
        res = self.client.post(reverse('organization:org-list'), data=self.post_data)
        # 201 Createdが返っていること
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # DBに値が作成されていること
        org = Organization.objects.all()
        self.assertEqual(len(org), 1)
        # DBの値が正しいこと
        self.assertEqual(org[0].name, self.post_data['name'])
        self.assertEqual(org[0].post_code, str(self.post_data['post_code']))
        self.assertEqual(org[0].prefecture, self.post_data['prefecture'])
        self.assertEqual(org[0].city, self.post_data['city'])
        self.assertEqual(org[0].address, self.post_data['address'])
        self.assertEqual(org[0].manager_name, self.post_data['manager_name'])
        self.assertEqual(org[0].plans, self.post_data['plans'])
        self.assertEqual(org[0].status, self.post_data['status'])

    def test_cannot_add_without_auth(self):
        """未認証のユーザーは組織の作成ができないこと"""
        # まずは組織テーブルが空であること
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        res = self.client.post(reverse('organization:org-list'), data=self.post_data)
        # 403が返ってくること
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_name(self):
        """名前がないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('name')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['name'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_post_code(self):
        """郵便番号がないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('post_code')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['post_code'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_prefecture(self):
        """都道府県がないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('prefecture')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['prefecture'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_city(self):
        """市区町村がないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('city')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['city'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_address(self):
        """市区町村以下の住所がないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('address')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['address'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_tel_number(self):
        """電話番号がないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('tel_number')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['tel_number'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_manager_name(self):
        """管理者名がないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('manager_name')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['manager_name'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

    def test_validation_require_plan(self):
        """プランがないと組織作成ができないこと"""
        # まずは組織テーブルが空であること
        self.client.force_authenticate(user=self.user)
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)
        # 未ログインのままで組織作成APIを叩く
        data = self.post_data
        data.pop('plans')
        res = self.client.post(reverse('organization:org-list'), data=data)
        # 400が返ってくること
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['plans'][0], 'この項目は必須です。')
        # DBに値が保存されていないこと
        org = Organization.objects.all()
        self.assertEqual(len(org), 0)

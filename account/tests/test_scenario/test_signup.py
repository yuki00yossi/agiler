import re

from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


# Create your tests here.
class signupTestCase(TestCase):
    """新規ユーザー登録のシナリオテスト"""

    def test_signup_and_activate(self):
        """会員登録～アクティベートまで（正常系）"""
        client = APIClient()
        param = {
            'email': 'signup@example.com',
            'password': 'adlkfjalig',
            'first_name': 'サンプル',
            'last_name': '太郎',
            'profile_text': '',
        }
        url = reverse('account:user-list')
        res = client.post(url, param)
        # ステータスコードの確認
        self.assertEqual(res.status_code, 201)
        # レスポンスJSONの確認
        self.assertEqual(res.data['email'], param['email'])
        self.assertEqual(res.data['first_name'], param['first_name'])
        self.assertEqual(res.data['last_name'], param['last_name'])
        self.assertEqual(res.data['is_active'], False)
        # 仮登録メールが送信されていることを確認
        self.assertEqual(len(mail.outbox[0].to), 1)
        # メールの送信先確認
        self.assertEqual(mail.outbox[0].to[0], param['email'])
        # メールタイトルの確認
        self.assertEqual(
            mail.outbox[0].subject,
            'Please Activate Your Account'
        )
        # メールに記載のURLを叩く
        pattern = 'http.*'
        result = re.search(pattern, mail.outbox[0].body, re.S)
        url = result.group()
        result = client.get(url)
        self.assertEqual(result.status_code, 200)
        # is_activeがTrueになっていることを確認
        user_model = get_user_model()
        user = user_model.objects.get(pk=res.data['id'])
        self.assertEqual(user.is_active, True)

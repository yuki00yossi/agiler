import re

from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from account.factories.user import UserFactory
from account.models import PasswordResetToken


User = get_user_model()


# Create your tests here.
class ResetPasswordTest(TestCase):
    """パスワードリセットのテストケース"""
    def setUp(self) -> None:
        # テストユーザーに登録するパスワード
        self.password = 'password'
        # テスト用ユーザー
        self.user = UserFactory(password=self.password)

    def test_reset_password_without_login(self):
        """登録メアドに送信される確認コードを用いて、非ログイン状態でパスワードを更新するテスト"""
        user = User.objects.get(pk=1)
        # まずは初期状態のパスワードを確認
        self.assertTrue(user.check_password(self.password))
        # 初期状態ではパスワードリセットコードは生成されていないこと
        self.assertEqual(len(PasswordResetToken.objects.all()), 0)
        # メールボックスが空であること
        self.assertEqual(len(mail.outbox), 0)
        client = APIClient()
        # パスワードリセット用確認コード生成APIを叩く
        send_mail_api_result = client.post(
            reverse('account:user-send-mail-password-change'),
            {'email': user.email}
        )
        # 200OKが返ってくること
        self.assertEqual(send_mail_api_result.status_code, status.HTTP_200_OK)
        # 確認コードが生成されていること
        tokens = PasswordResetToken.objects.all()
        self.assertEqual(len(tokens), 1)
        token = tokens[0]
        # 発行されたコードの各種情報が正しいこと
        self.assertEqual(token.user.pk, user.pk)  # 対象ユーザー
        self.assertFalse(token.is_used)  # 使用済みフラグ
        # 確認コードが記載されたメールが飛んでいること
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'パスワード変更用URLのお知らせ')
        # メール本文からリセットコードを抜き出して取得
        code = re.search('パスワードリセットコード:.*', mail.outbox[0].body).group()
        code = code.replace('パスワードリセットコード: ', '')
        # メールに記載されているコードが正しいこと
        self.assertEqual(code, token.token)
        new_password = 'newpassword1234'
        param = {
            'password': new_password,
            'token': code,
        }
        url = reverse(
            'account:user-change-password-with-token',  args=[user.pk])
        # パスワード変更実行APIを叩く
        reset_api_result = client.post(url, param)
        self.assertEqual(reset_api_result.status_code, status.HTTP_200_OK)
        new_pass_user = User.objects.get(pk=user.pk)
        # パスワードが変更されていること
        self.assertTrue(new_pass_user.check_password(new_password))
        # トークンが使用済みになっていること
        token = PasswordResetToken.objects.get(pk=token.pk)
        self.assertTrue(token.is_used)

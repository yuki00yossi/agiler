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

    def test_change_password_autorized_user(self):
        """認証済みユーザー用のパスワード変更APIテスト"""
        client = APIClient()
        client.force_authenticate(user=self.user)
        param = {
            'password': 'fakjdfagkalj'
        }
        res = client.post(
            reverse('account:user-change-password', args=[self.user.pk]),
            data=param)
        # HTTPレスポンスのチェック
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['msg'], 'パスワードを更新しました。')
        # パスワードが更新されているチェック
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password(param['password']))

    def test_api_change_password_for_auth_user_failed(self):
        """認証済みユーザー用のパスワード変更APIに認証情報無しで実行出来ないテスト"""
        client = APIClient()
        param = {
            'password': 'dlkfjaljf'
        }
        res = client.post(
            reverse('account:user-change-password', args=[self.user.pk]),
            data=param
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # 実際にパスワードが更新されていないことを確認
        user = User.objects.get(pk=self.user.pk)
        self.assertFalse(user.check_password(param['password']))

    def test_api_change_password_for_auth_user_cannot_other_user_password(self):
        """認証済みユーザーが他のユーザーのパスワードを変更することが出来ないテスト"""
        client = APIClient()
        auth_user = UserFactory()
        client.force_authenticate(user=auth_user)
        param = {
            'password': 'newpasswordlkfll',
        }
        # 別ユーザーのPKを指定してPOST
        res = client.post(
            reverse('account:user-change-password', args=[self.user.pk]),
            data=param
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # リクエストユーザーとPOSTで指定されたユーザーのいずれもパスワードが変更されないこと
        user = User.objects.get(pk=self.user.pk)
        self.assertFalse(user.check_password(param['password']))
        auth_user2 = User.objects.get(pk=auth_user.pk)
        self.assertFalse(auth_user2.check_password(param['password']))

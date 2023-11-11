from datetime import datetime

from django.test import TestCase
from account.factories.user import UserFactory
from account.models import User
from account.serializer import UserSerializer


class UserSerializerTest(TestCase):
    """UserSerializerのテスト"""
    def setUp(self):
        self.test_user = UserFactory()
        self.expected_fields = [
            'id', 'email', 'first_name', 'last_name',
            'profile_text', 'is_active', 'created_at', 'updated_at',
        ]
        self.datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
        self.test_param = {
            'email': 'hoge@example.com',
            'password': 'dlkfjalgaifalk',
            'profile_text': 'this is profile text',
            'last_name': '佐藤',
            'first_name': '太郎',
        }

    def test_contains_expected_fields(self):
        """返されるデータフィールドが想定と一致すること"""
        serializer = UserSerializer(instance=self.test_user)
        self.assertEqual(
            set(self.expected_fields),
            set(serializer.data.keys())
        )

    def test_data_equals_record(self):
        """シリアライザーのデータがDBのレコードと一致すること"""
        record = User.objects.get(pk=self.test_user.pk)
        serializer = UserSerializer(instance=self.test_user)

        for key, val in serializer.data.items():
            if key not in ['created_at', 'updated_at']:
                self.assertEqual(record.__getattribute__(key), val)
                continue
            self.assertEqual(
                record.__getattribute__(key),
                datetime.strptime(val, self.datetime_format)
            )

    def test_validated_data_expect_validated_data(self):
        """初期データに不要な値が入って来てもバリデーション後には消えていること"""
        data = self.test_param
        data['hoge'] = 'fuga'
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        validated = serializer.validated_data

        self.assertEqual('hoge' not in list(validated.keys()), True)

    def test_create_record_success(self):
        """下記５つの項目で保存が成功すること
        - email
        - password
        - profile_text
        - last_name
        - first_name
        """
        serializer = UserSerializer(data=self.test_param)
        serializer.is_valid()
        save_result = serializer.save()

        # DBに保存されたデータと一致すること
        user = User.objects.get(pk=save_result.pk)
        self.assertEqual(save_result, user)
        # デフォルトではis_active=Falseであること
        self.assertEqual(user.is_active, False)

    def test_validate_email_empty_not_allow(self):
        """メールアドレスのバリデーション確認（必須チェック１）"""
        data = self.test_param.copy()
        data['email'] = ''
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_email_required(self):
        """メールアドレスのバリデーション確認（必須チェック２）"""
        data = self.test_param.copy()
        del data['email']
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_email_failure(self):
        """メールアドレスのバリデーション確認（失敗パターン１）"""
        data = self.test_param.copy()
        data['email'] = 'hogehoge'
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_email_failure2(self):
        """メールアドレスのバリデーション確認（失敗パターン２）"""
        data = self.test_param.copy()
        data['email'] = 'hogehoge@example'
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_email_success(self):
        """メールアドレスのバリデーション確認(正常)"""
        data = self.test_param.copy()
        data['email'] = 'hogehoge@example.com'
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, True)

    def test_validate_password_empty_not_allow(self):
        """パスワードのバリデーション確認(必須チェック１)"""
        data = self.test_param
        data['password'] = ''
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_password_required(self):
        """パスワードのバリデーション確認(必須チェック２)"""
        data = self.test_param
        del data['password']
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_password_failure_7_word(self):
        """パスワードのバリデーション確認(8文字以下は却下)"""
        data = self.test_param
        data['password'] = 'sk6dilj'
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_password_success_8_word(self):
        """パスワードのバリデーション確認(8文字以上はOK)"""
        data = self.test_param
        data['password'] = 'sk6diljs'
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, True)

    def test_validate_first_name_failure_empty_not_allow(self):
        """first_nameのバリデーション確認(空はNG)"""
        data = self.test_param
        data['first_name'] = ''
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_first_name_failure_required(self):
        """first_nameのバリデーション確認(要素が無いとNG)"""
        data = self.test_param
        del data['first_name']
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_last_name_failure_empty_not_allow(self):
        """last_nameのバリデーション確認(空はNG)"""
        data = self.test_param
        data['last_name'] = ''
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_validate_last_name_failure_required(self):
        """last_nameのバリデーション確認(要素が無いとNG)"""
        data = self.test_param
        del data['last_name']
        serializer = UserSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

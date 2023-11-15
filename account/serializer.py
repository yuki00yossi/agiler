from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from organization.serializer import OrganizationSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name',
            'profile_text', 'is_active', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'is_active', 'created_at', 'updated_at',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """新規ユーザー登録"""
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_text=validated_data['profile_text']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """ユーザー情報アップデート"""
        if ('email' in validated_data):
            # メールアドレス変更は専用のMailSerializerで行うため削除
            del validated_data['email']
        if ('password' in validated_data):
            # パスワード変更は専用のPasswordSerializerで行うため削除
            del validated_data['password']

        return super().update(instance, validated_data)

    def validate_password(self, value):
        validate_password(value)
        return value


class PasswordSerializer(serializers.Serializer):
    """パスワードを扱うシリアライザー"""
    password = serializers.CharField()

    def validate_password(self, value):
        validate_password(value)
        return value


class PasswordSerializerWithToken(PasswordSerializer):
    """トークンを使用してのパスワード更新API専用シリアライザー"""
    password = serializers.CharField()
    token = serializers.CharField()

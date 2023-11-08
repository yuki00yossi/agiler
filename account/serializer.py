from rest_framework import serializers
from django.contrib.auth import get_user_model
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
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_text=validated_data['profile_text']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

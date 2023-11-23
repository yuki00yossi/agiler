from rest_framework import serializers
from account.serializer import UserSerializer
from organization.models import Organization, OrganizationUser


class OrganizationSerializer(serializers.ModelSerializer):
    # Members = UserSerializer(many=True)

    class Meta:
        model = Organization
        fields = (
            'id', 'name', 'post_code', 'prefecture', 'city',
            'address', 'tel_number', 'manager_name', 'plans', 'status',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at',)

    def create(self, validated_data):
        return Organization.objects.create(**validated_data)


class MemberSerializer(serializers.ModelSerializer):
    """組織に所属しているユーザーに関するシリアライザー"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = (
            'id', 'user', 'invited_at', 'status',
            'joined_at',
        )

from rest_framework import permissions

from organization.models import OrganizationUser


class OrganizationIsAdminOrCreate(permissions.BasePermission):
    """組織のパーミッション

    - スタッフ権限からのリクエストはTrue
    - 組織作成はログイン中のユーザーなら誰でもTrue
    - それ以外は組織にログイン中かつ、所属しているかつ、管理者権限がないとFalse
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if view.action == 'create':
            return True
        try:
            OrganizationUser.objects.get(
                user=request.user, status=1, role=1, organization=obj)
            return True
        except OrganizationUser.DoesNotExist:
            return False


class OrganizationReadOnly(permissions.BasePermission):
    """組織の情報閲覧用パーミッション

    - スタッフ権限からのリクエストはTrue
    - その組織のアクティブなメンバーであればTrue
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        try:
            OrganizationUser.objects.get(
                user=request.user, organization=obj, status=1)
            return True
        except OrganizationUser.DoesNotExist:
            return False
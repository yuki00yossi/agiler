from rest_framework import permissions


class UserViewSetPermission(permissions.BasePermission):
    """ユーザーのパーミッション設定

    - スタッフ権限ユーザーからのリクエスト全て許可。
    - 下記APIへのアクセスは誰でも許可
        - 新規登録API
        - パスワードリセットメール送信API
        - パスワードリセット実行API
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        if view.action in ['create', 'reset_password_mail', 'reset_password']:
            return True
        elif not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_staff:
            return True

        return obj.pk == request.user.pk

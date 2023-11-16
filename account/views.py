import datetime

from django.conf import settings
from django.utils import timezone
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from account.models import PasswordResetToken, User, UserActivationToken
from .permissions import UserViewsetsPermission
from .serializer import (
    UserSerializer,
    PasswordSerializer,
    PasswordSerializerWithToken
)


# Create your views here.
class UserViewsets(viewsets.ModelViewSet):
    """ユーザービュー"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (UserViewsetsPermission,)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.AllowAny])
    def send_mail_password_change(self, request):
        """パスワード変更用URLが記載されたメールを送信するAPI"""
        if request.user.is_authenticated:
            user = request.user
        else:
            try:
                user = User.objects.get(email=request.POST['email'])
            except KeyError:
                return Response(
                    {
                        'errors': {'email': 'メールアドレスが必要です。', },
                    },
                    status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user = None
        if user:
            token_expired = timezone.now() + datetime.timedelta(
                minutes=settings.PASSWORD_RESET_TOKEN_EXPIRED_MIN
            )
            # 過去の発行済トークンは使用済みにする
            PasswordResetToken.objects.filter(
                user__exact=user.pk,
                is_used__exact=False
            ).update(is_used=True)
            PasswordResetToken.objects.create(
                user=user, expired_at=token_expired
            )
        return Response(
            {'message': 'パスワード変更用URLの発行を受け付けました。'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """ログイン中のユーザーがパスワード更新を実行するAPI"""
        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'msg': 'パスワードを更新しました。'}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.AllowAny])
    def change_password_with_token(self, request, pk=None):
        """トークンを使用して未ログイン状態でパスワード更新するAPI"""
        serializer = PasswordSerializerWithToken(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        token = PasswordResetToken.objects.filter(
                user__exact=user.pk,
                token__exact=serializer.validated_data['token'],
                is_used__exact=False,
                expired_at__gt=timezone.now()
        )
        if token.first() is None:
            # 対象ユーザーの発行済トークンが取れなかった場合
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        # パスワード変更実施
        user.set_password(serializer.validated_data['password'])
        user.save()
        token[0].is_used = True
        token[0].save()
        return Response({'msg': 'パスワードを変更しました。'}, status=status.HTTP_200_OK)


def activate_user(request, token):
    """ユーザーをアクティベートするAPI

    Args:
        request (_type_):
        token (str): アクティベーショントークン

    Returns:
        JsonResponse: JsonResponse。
            成功時のステータスコードは200。失敗時は400
    """
    result = UserActivationToken.objects.activate_user(token)
    if result:
        return JsonResponse({}, status=200)
    return JsonResponse({}, status=400)


# ここから下はデバッグTrueの時だけのデバッグ用View
def debug_login(request):
    """APIデバッグ時にログインする為のページ

    Args:
        request (_type_): リクエスト情報
    """
    print(request.method)
    if request.method == 'GET':
        return render(request, 'account/debug_login.html', {})
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('loged in!')

    return HttpResponse('ng')


def debug_logout(request):
    """APIデバッグログアウト用

    Args:
        request (_type_): リクエスト情報
    """
    logout(request)
    return HttpResponse('logout!')

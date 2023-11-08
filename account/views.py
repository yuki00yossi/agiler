from django.http.response import JsonResponse
# from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from account.models import UserActivationToken
from .serializer import UserSerializer


# Create your views here.
class SignUpView(generics.CreateAPIView):
    """新規会員登録API"""
    permission_classes = [permissions.AllowAny,]
    serializer_class = UserSerializer


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

from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, viewsets
from rest_framework import permissions

from account.models import User, UserActivationToken
from .permissions import UserViewsetsPermission
from .serializer import UserSerializer


# Create your views here.
class SignUpView(generics.CreateAPIView):
    """新規会員登録API"""
    permission_classes = [permissions.AllowAny,]
    serializer_class = UserSerializer


class UserViewsets(viewsets.ModelViewSet):
    """ユーザービュー"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (UserViewsetsPermission,)


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

from django.http.response import JsonResponse
# from django.shortcuts import render

from account.models import UserActivationToken


# Create your views here.
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

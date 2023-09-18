from django.shortcuts import render

from account.models import UserActivationToken


# Create your views here.
def activate_user(request, token):
    result = UserActivationToken.objects.activate_user(token)
    return render(
        request,
        'account/activate_user.html',
        {'result': result, }
    )

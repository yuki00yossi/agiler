from django.conf import settings
from django.urls import path
from rest_framework import routers

from account import views


app_name = 'account'
urlpatterns = [
    # path('add/', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:token>/', views.activate_user, name='activate'),
]

router = routers.DefaultRouter()
router.register('account', views.UserViewSet, 'user')
urlpatterns += router.urls

# デバッグ用URL
if settings.DEBUG:
    urlpatterns += [
        path('debug/login', views.debug_login),
        path('debug/logout', views.logout),
    ]

import pprint
pprint.pprint(urlpatterns)
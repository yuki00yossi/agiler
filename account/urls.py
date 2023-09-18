from django.urls import path


from account import views

app_name = 'account'
urlpatterns = [
    path('activate/<str:token>/', views.activate_user, name='user_activate'),
]

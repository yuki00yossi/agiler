from django.urls import path


from account import views

app_name = 'account'
urlpatterns = [
    path('add/', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:token>/', views.activate_user, name='activate'),
]

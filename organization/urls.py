from django.urls import path


from organization import views

app_name = 'organization'
urlpatterns = [
    path(
        'joined/',
        views.OrganizationListJoined.as_view(),
        name='org_joined'
    ),
]

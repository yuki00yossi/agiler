from django.urls import path
from organization import views
from rest_framework import routers

app_name = 'organization'
urlpatterns = [
    path(
        'joined/',
        views.OrganizationListJoined.as_view(),
        name='org_joined'
    ),
]

router = routers.DefaultRouter()
router.register('organization', views.OrganizationViewSet, 'org')
urlpatterns += router.urls

from pprint import pprint
pprint(urlpatterns)

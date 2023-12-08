from django.urls import path
from organization import views
from rest_framework import routers


app_name = 'project'
urlpatterns = []

router = routers.DefaultRouter()
router.register('project', views.OrganizationViewSet, 'pj')
urlpatterns += router.urls

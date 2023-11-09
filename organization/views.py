# from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets

from .serializer import OrganizationSerializer
from .models import Organization


# Create your views here.
class OrganizationViewsets(viewsets.ModelViewSet):
    """ 組織のビュー """
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.filter(status=1)


class OrganizationListJoined(generics.ListAPIView):
    """ ユーザーが所属している組織一覧を取得 """
    def get_queryset(self):
        return Organization.objects.filter(
            members__user=self.request.user.pk)

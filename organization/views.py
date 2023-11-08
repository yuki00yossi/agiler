# from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions


# Create your views here.
class Organization(generics.ListAPIView):
    """ 組織のビュー """
    def get(self, request, format=None):
        # organizations = Organization.objects.all()
        # organization = OrganizationSerializer(organizations, many=True)
        return True


class OrganizationListJoined(generics.ListAPIView):
    """ ユーザーが所属している組織一覧を取得 """
    def get_queryset(self):
        return Organization.objects.filter(
            members__user=self.request.user.pk)

# from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import OrganizationSerializer, MemberSerializer
from .models import Organization, OrganizationUser
from .permissions import OrganizationIsAdminOrCreate, OrganizationReadOnly


# Create your views here.
class OrganizationViewSet(viewsets.ModelViewSet):
    """ 組織のビュー """
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.filter(status=1)
    permission_classes = (OrganizationIsAdminOrCreate,)

    @action(
        detail=True,
        methods=['get'],
        permission_classes=(OrganizationReadOnly,)
    )
    def members(self, request, pk=None):
        """所属メンバー（ユーザー）一覧を取得するAPI"""
        obj = self.get_object()
        self.check_object_permissions(self.request, obj)
        query_set = OrganizationUser.objects.prefetch_related('user').filter(
            organization=obj)
        serializer = MemberSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationListJoined(generics.ListAPIView):
    """ ユーザーが所属している組織一覧を取得 """
    def get_queryset(self):
        return Organization.objects.filter(
            members__user=self.request.user.pk)

# from django.shortcuts import render
from pprint import pprint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from account.serializer import UserSerializer
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
        self.check_object_permissions(request, obj)
        query_set = OrganizationUser.objects.prefetch_related('user').filter(
            organization=obj)
        serializer = MemberSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(OrganizationIsAdminOrCreate,)
    )
    def add_member(self, request, pk=None):
        """組織にメンバーを追加するAPI"""
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        User = get_user_model()
        # 追加するユーザーが登録済かどうかのフラグ
        user_flg = 0
        law_password = ''
        try:
            user = User.objects.get(email=request.data['email'])
            user_flg = 1
        except User.DoesNotExist:
            """ユーザーがいない場合は作成"""
            data = request.data
            law_password = User.get_random_password()
            data['password'] = law_password
            data['profile_text'] = ''
            serializer = UserSerializer(data=data)
            if not serializer.is_valid():
                return Response({serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.create(serializer.validated_data)
        try:
            invitation_info = OrganizationUser.objects.get(user=user, organization=obj)
            if invitation_info.status == OrganizationUser.STATUS_ACTIVE:
                return Response({'msg': 'このユーザーはすでに参加しています。'}, status=status.HTTP_400_BAD_REQUEST)
            elif invitation_info.status == OrganizationUser.STATUS_DROPPED:
                invitation_info.status = OrganizationUser.STATUS_INVITATION
                invitation_info.save()
        except OrganizationUser.DoesNotExist:
            OrganizationUser.objects.create(
                user=user, organization=obj, role=request.data['role'], status=OrganizationUser.STATUS_INVITATION)

        self.send_invite_mail(user, password=law_password)
        return Response({'msg': '招待メールを送信しました。'}, status.HTTP_200_OK)

    def send_invite_mail(self, user, password=''):
        """ユーザーに招待メールを送信する"""
        mail_context = {
            'user': user,
            'organization': self.get_object(),
            'site_name': settings.SITE_NAME,
            'user_flg': password == '',
            'password': password
        }
        user.email_user(
            subject='【重要なお知らせ】組織への招待が届いています。',
            message=render_to_string(
                'organization/mail/invitation_mail.txt',
                context=mail_context),
        )


class OrganizationListJoined(generics.ListAPIView):
    """ ユーザーが所属している組織一覧を取得 """
    def get_queryset(self):
        return Organization.objects.filter(
            members__user=self.request.user.pk)

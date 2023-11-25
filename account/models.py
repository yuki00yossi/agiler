import secrets
import uuid

from datetime import timedelta
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    """ カスタムユーザーマネージャー """
    use_in_migrations = True

    def _create_user(
            self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The given email must be set'))
        if not first_name:
            raise ValueError(_('The given first name must be set'))
        if not last_name:
            raise ValueError(_('The given last name must be set'))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
            self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )

    def create_superuser(
            self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    """ カスタムユーザーモデル """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=64)
    last_name = models.CharField(_('last_name'), max_length=64)
    profile_text = models.CharField(
        _('profile text'), max_length=256, blank=True, null=True)

    is_active = models.BooleanField(
        _('is active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('last updated'), auto_now=True)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """ first_nameとlast_nameを半角スペースでつなげた文字列を返す """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name

    def email_user(
            self, subject, message,
            from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @classmethod
    def get_random_password(cls):
        return secrets.token_urlsafe(16)



class UserActivationTokenManager(models.Manager):
    """ ユーザーアクティベーション関連のマネージャー """

    def activate_user(self, post_token):
        """ユーザーをアクティベートする

        Args:
            post_token (string): アクティベーショントークン

        Returns:
            Bool: 成否
        """
        saved_token = self.filter(
            token=post_token,
            expired_at__gte=timezone.now()
        ).first()

        if hasattr(saved_token, 'user'):
            user = saved_token.user
            user.is_active = True
            user.save()

            return True

        return False

    def generate(self, user: User):
        """
        ユーザーアクティベーショントークンを生成する。
        （デリートインサート）

        Args:
            user (User): ユーザーインスタンス

        Returns:
            UserActivationToken: UserActivationTokenインスタンス
        """
        self.filter(user=user).delete()
        token = self.model(
            user=user,
            expired_at=timezone.now()+timedelta(
                minutes=settings.USER_ACTIVATION_EXPIRED_MIN)
        )
        token.save()

        return token


class UserActivationToken(models.Model):
    """ ユーザーアクティベーションコードを保存するモデル """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    expired_at = models.DateTimeField()

    objects = UserActivationTokenManager()


class PasswordResetToken(models.Model):
    """パスワードリセット用のトークンを発行する"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(
        verbose_name='パスワードリセットトークン',
        max_length=256,
        default=secrets.token_urlsafe(32)
    )
    is_used = models.BooleanField(verbose_name='使用済みフラグ', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    expired_at = models.DateTimeField(verbose_name='トークン有効期限')

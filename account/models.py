from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
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

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

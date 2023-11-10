from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from account.models import User, UserActivationToken


@receiver(post_save, sender=User)
def send_user_activation_mail(sender, instance, created, **kwargs):
    """ ユーザーアクティベーション用URLを記載したメールを送信する """
    if not created:
        return
    if instance.is_active:
        return
    token = UserActivationToken.objects.generate(instance)
    subject = 'Please Activate Your Account'
    activation_url = settings.SITE_URL_ROOT
    activation_url += reverse('account:activate', args=[token.token])
    context = {
        'user': instance,
        'activation_url': activation_url,
        'url_expiration_min': settings.USER_ACTIVATION_EXPIRED_MIN
    }
    instance.email_user(
        subject=subject,
        message=render_to_string(
            'mail/user_activation_mail.txt',
            context=context
        ),
    )

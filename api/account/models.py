from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


UserModel = get_user_model()


class UserProfile(models.Model):
    last_request = models.DateTimeField(
        blank=True,
        verbose_name=_('Last request')
    )
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )

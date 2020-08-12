from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


UserModel = get_user_model()


class PostModel(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name=_('Title')
    )
    body = models.TextField(
        verbose_name=_('Body')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )
    user = models.ForeignKey(
        UserModel,
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )

    def __str__(self):
        str_repr = f'Title: {self.title}\n'
        str_repr += f'\tId: {self.id}'
        str_repr += f'\tUser: {self.user}'
        return str_repr


class LikeModel(models.Model):
    post = models.ForeignKey(
        PostModel,
        related_name='likes',
        on_delete=models.CASCADE,
        verbose_name=_('Post')
    )
    user = models.ForeignKey(
        UserModel,
        related_name='likes',
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )

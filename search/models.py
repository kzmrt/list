from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username + ":" + self.email


class Post(models.Model):
    """投稿モデル"""
    class Meta:
        db_table = 'post'

    title = models.CharField(verbose_name='タイトル', max_length=255)
    text = models.CharField(verbose_name='内容', max_length=255, default='', blank=True)
    author = models.ForeignKey(
        'search.CustomUser',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.title + ',' + self.text

    @staticmethod
    def get_absolute_url(self):
        return reverse('search:index')
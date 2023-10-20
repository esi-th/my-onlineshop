from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils.translation import gettext as _


class Post(models.Model):
    POST_STATUS = [
        ('pub', _('Published')),
        ('drf', _('Draft')),
    ]
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Post Author'))
    title = models.CharField(_('Post Title'), max_length=250)
    text = RichTextField(_('Post Description'))
    status = models.CharField(_('Post Status'), max_length=3, choices=POST_STATUS, blank=True)
    cover = models.ImageField(_('Post Cover'), upload_to='post_covers/', blank=True)
    datetime_created = models.DateTimeField(_('Post Date Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('Post Date Modified'), auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Comment Author'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'), related_name='comments')
    body = models.TextField(_('Comment Text'))
    active = models.BooleanField(_('Comment Status'), default=True)
    datetime_created = models.DateTimeField(_('Post Date Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('Post Date Modified'), auto_now=True)

    def __str__(self):
        return f'Author: {self.author} In "{self.post.title}" Post'

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.post.id])

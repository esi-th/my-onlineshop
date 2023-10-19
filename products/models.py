from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.conf import settings


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    datetime_created = models.DateTimeField(_('Created Date'), auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    short_description = models.TextField(_('Product Description'))
    description = models.TextField('Product Short Description')
    price = models.PositiveIntegerField(_('Price'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Category'))
    cover = models.ImageField(_('Product Cover'), upload_to='covers/product_covers/')
    active = models.BooleanField(_('Show Product'), default=True)
    datetime_created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('Modified Date'), auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]
    body = models.CharField(_('Comment Text'), max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name=_('Comment Author'), related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'), related_name='comments')
    stars = models.CharField(_('Product Stars'), max_length=10, choices=PRODUCT_STARS)
    datetime_created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('Modified Date'), auto_now=True)
    active = models.BooleanField(_('Show Comment'), default=True)

    def __str__(self):
        return f'Comment for {self.product}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])

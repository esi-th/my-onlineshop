from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    is_paid = models.BooleanField(_('Paid?'), default=False)

    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    phone_number = models.CharField(_('Phone Number'), max_length=13)
    address = models.CharField(_('Address'), max_length=500)

    order_note = models.CharField(_('Order Note'), max_length=500, blank=True)

    zarinpal_authority = models.CharField(_('Zarinpal Authority'), max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(_('Zarinpal Ref ID'), max_length=150, blank=True)
    zarinpal_text = models.TextField(_('Zarinpal Response Data'), max_length=700, blank=True)

    datetime_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('Date Modified'), auto_now=True)

    def __str__(self):
        return f'Order: {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE,
                                related_name='order_items', verbose_name=_('Order Items'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    price = models.PositiveIntegerField(_('Price'))

    datetime_created = models.DateTimeField(_('Date Created'), auto_now_add=True)

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} x {self.quantity} (price:{self.price}'

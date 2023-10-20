from django.db import models
from django.utils.translation import gettext as _


class Contact(models.Model):
    first_name_last_name = models.CharField(_('Name'), max_length=100)
    phone_number = models.CharField(_('Phone Number'), max_length=15)
    email = models.EmailField(_('Email'))
    contact_note = models.CharField(_('Contact Note'), max_length=1000)

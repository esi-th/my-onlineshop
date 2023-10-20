from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['first_name_last_name', 'phone_number', 'email', ]

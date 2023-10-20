from django import forms
from .models import Contact


class ContactUsFrom(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name_last_name', 'phone_number', 'email', 'contact_note', ]

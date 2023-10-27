from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['username', 'email']
    add_fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture',)}),
    )

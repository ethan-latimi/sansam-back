from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        ("description", {"fields": ("gender", "bio",)}),
    )
